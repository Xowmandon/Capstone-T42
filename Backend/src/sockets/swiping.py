# Author: Joshua Ferguson

from flask import Flask, request
from flask_socketio import SocketIO, Namespace, disconnect, emit, join_room, leave_room, send
from flask_jwt_extended import JWTManager, decode_token
import redis
from functools import wraps
import json
from datetime import datetime

from Backend.src.extensions import db, redis_client
import Backend.src.models as models

from Backend.src.sockets.socket_helpers import (
    auth_connecting_user,
    authenticated_only,
    cache_user_status,
    EVENT_STATUS,
    EVENT_ERROR
)

# Constants
SWIPE_RESULTS = ['PENDING', 'ACCEPTED', 'REJECTED']
EVENT_SUCCESSFUL_MATCH = 'successful_match'
EVENT_MATCH_CREATION_FAILED = 'match_creation_failed'
EVENT_SWIPE_RESULT = "swipe_result"
MATCH_TTL = 86400  # 24 hours in seconds

# TODO: #4 Handle Emit and Buffering/Caching of Successful Matches for Offline Users
# TODO: Implement Redis Pub/Sub for Offline User Successful Match 


def authenticated_only(f):
    """
    Decorator to ensure a user is authenticated before processing socket events.
    
    Args:
        f: The function to wrap
        
    Returns:
        The wrapped function that checks authentication
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not hasattr(args[0], 'user_id') or args[0].user_id is None:
            print("Unauthenticated user attempted to access protected event")
            return
        return f(*args, **kwargs)
    return wrapped


class SwipeNamespace(Namespace):
    """
    Handles swiping socket events for real-time user interactions.
    
    This namespace manages swiping interactions between users, including:
    - User authentication via JWT
    - Processing swipes
    - Creating matches
    - Handling disconnections
    """

    def __init__(self, namespace=None):
        """
        Initialize the SwipeNamespace.
        
        Args:
            namespace (str, optional): The namespace identifier. Defaults to None.
        """
        super().__init__(namespace)
        self.user_id = None
        self.redis_client = redis_client

    # -----------------Main Websocket Events---------------------

    def on_connect(self):
        """
        Authenticate user via JWT when they connect.
        
        This method:
        1. Extracts the JWT token from request headers
        2. Validates the token and retrieves the user
        3. Caches the user's online status
        
        Returns:
            None
        """
        try:
            token = request.headers.get("X-Authorization")
            user_id = auth_connecting_user(token)
            if user_id is None:
                disconnect()
                return
            
            self.user_id = user_id
            
            # Cache user's online status
            cache_user_status(self.user_id, True)
            
            print(f"User {self.user_id} connected to /Swiping namespace!")
            
            # Deliver any cached matches
            self._deliver_cached_matches()
            
        except Exception as e:
            print(f"Error during connection: {str(e)}")
            disconnect()
            return False

    @authenticated_only
    def on_swipe(self, data):
        """
        Handle a user's swipe action.
        
        Args:
            data (dict): Contains swipee_id and swipe_result
            
        This method:
        1. Validates the swipe data
        2. Processes the swipe
        3. Creates a match if both users swiped right
        4. Caches the match for offline users
        """
        try:
            swipee_id = data.get("swipee_id")
            swipe_result = data.get("swipe_result")
            
            if not all([swipee_id, swipe_result]):
                print("Invalid swipe data. Ignored.")
                return
                
            if swipe_result not in ["ACCEPTED", "REJECTED"]:
                print(f"Invalid swipe result: {swipe_result}. Ignored.")
                return
                
            print(f"User {self.user_id} swiped {swipe_result} on user {swipee_id}")
            
            # Process the swipe
    
            processed_swipe = models.swipe.SwipeProcessor.process_new_swipe(
                swiper_id=self.user_id,
                swipee_id=swipee_id,
                swipe_result=swipe_result
            )
            
            if not processed_swipe:
                print(f"Failed to process swipe: {json.dumps(processed_swipe)}")
                emit(EVENT_ERROR, {"message": "Failed to process swipe"}, room=self.user_id)
                return
                
            if processed_swipe.swipe_result == "ACCEPTED":
                print(f"New Match Detected: {processed_swipe}")
                self.process_new_match(swipee_id)
                
        except Exception as e:
            print(f"Error processing swipe: {str(e)}")
            emit(EVENT_ERROR, {"message": "Failed to process swipe"}, room=self.user_id)

    def on_disconnect(self):
        """
        Handle user disconnection.
        
        This method:
        1. Updates the user's online status
        2. Notifies the user of disconnection
        """
        try:
            if self.user_id is None:
                print("User is not authenticated. Disconnect event ignored.")
                return
        
            # Update user's online status
            cache_user_status(self.user_id, False)
            
            # Emit Disconnect Status Message to User
            emit(EVENT_STATUS, {"msg": f"User {self.user_id} disconnected"}, room=self.user_id)
            print(f"User {self.user_id} disconnected from /Swiping namespace!")
            
        except Exception as e:
            print(f"Error during disconnection: {str(e)}")

    # -----------------Custom/Helper Methods & Events---------------------

    def process_new_match(self, matched_user_id):
        """
        Process a new match between users.
        
        Args:
            matched_user_id (str): The ID of the matched user
            
        This method:
        1. Creates a match in the database
        2. Notifies both users of the match
        3. Caches the match for offline users
        """
        try:
            # Create match in database
            match = models.Match.create_match(self.user_id, matched_user_id)
            if not match:
                print("Failed to create match in database")
                return False
                
            match_data = match.to_dict()
            
            from Backend.src.sockets.socket_helpers import is_user_online
            
             # Check if matched user is online
            if is_user_online(matched_user_id):
                
                # Send match notification to matched user
                emit(EVENT_MATCH, match_data, room=matched_user_id)
                print(f"Match notification sent to user {matched_user_id}")
                
                # Join the match room and Namespaces
                join_room(match_data.get("id"),sid=matched_user_id, namespace="/chat")
                
            else:
                # Cache match for offline user
                self._cache_match_for_offline_user(matched_user_id, match_data)
                print(f"Match cached for offline user {matched_user_id}")
                
            # Send match notification to current user
            emit(EVENT_MATCH, match_data, room=self.user_id)
            print(f"Match notification sent to user {self.user_id}")
            
            # Join the match room and Namespaces for current user
            join_room(match_data.get("id"),sid=self.user_id, namespace="/chat")
            
            return True
            
        except Exception as e:
            print(f"Error processing new match: {str(e)}")

    def _cache_match_for_offline_user(self, user_id, match_data):
        """
        Cache a match for an offline user.
        
        Args:
            user_id (str): The ID of the offline user
            match_data (dict): The match data to cache
        """
        try:
            cache_key = f"user:{user_id}:matches"
            
            # Get existing matches
            matches = self._get_cached_matches(user_id)
            
            # Add new match
            matches.append(match_data)
            
            # Update matches in Redis
            self.redis_client.setex(
                cache_key,
                MATCH_TTL,
                json.dumps(matches)
            )
            
        except Exception as e:
            print(f"Error caching match for offline user: {str(e)}")

    def _get_cached_matches(self, user_id):
        """
        Get cached matches for a user.
        
        Args:
            user_id (str): The ID of the user
            
        Returns:
            list: List of matches
        """
        try:
            cache_key = f"user:{user_id}:matches"
            cached_data = self.redis_client.get(cache_key)
            
            if cached_data:
                return json.loads(cached_data.decode('utf-8'))
            return []
            
        except Exception as e:
            print(f"Error getting cached matches: {str(e)}")
            return []

    def _deliver_cached_matches(self):
        """
        Deliver cached matches to the user.
        
        This method:
        1. Retrieves all matches from Redis
        2. Sends them to the user
        3. Clears the matches from Redis
        """
        try:
            matches = self._get_cached_matches(self.user_id)
            
            if matches:
                # Send matches to the user
                for match in matches:
                    emit(EVENT_MATCH, match, room=self.user_id)
                    
                print(f"Delivered {len(matches)} cached matches to user {self.user_id}")
                
                # Clear matches from Redis
                cache_key = f"user:{self.user_id}:matches"
                self.redis_client.delete(cache_key)
                
        except Exception as e:
            print(f"Error delivering cached matches: {str(e)}")

# Register the swiping namespace (Currently in App.py)
#socketio.on_namespace(SwipeNamespace("/swiping"))

