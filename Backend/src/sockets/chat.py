"""
Author: Joshua Ferguson

Implementation of the `ChatNamespace` class, which handles chat socket events for real-time messaging.

The `ChatNamespace` class provides the following methods:

# Main WebSocket Event Handlers

- `on_connect()`: Authenticates the user via JWT when they connect and auto-joins match rooms.
- `on_join(data)`: User joins a chat room (f"match_<match_id>" used as room identifier).
- `on_message(data)`: Handles message sending and Saving to DB
- `on_leave(data)`: User leaves a chat room.
- `on_disconnect()`: Handles user disconnection and removes them from any match rooms.

# Custom Methods and Helpers

- `get_user_match_rooms()`: Retrieves all match rooms where this user is involved.
- `auto_join_match_rooms()`: Retrieves and joins all match rooms where this user is not joined.
- `auto_leave_match_rooms()`: Leaves all match rooms where this user is joined.

"""  
import json
from flask import request
from flask_socketio import Namespace, emit, join_room, leave_room, disconnect, rooms

from Backend.src.models.model_helpers import MatchModelHelper
import Backend.src.models as models
from Backend.src.services.auth_service import get_user_from_token
from Backend.src.sockets.socket_helpers import (
    auth_connecting_user, 
    gen_match_room_name, 
    authenticated_only,
    cache_user_status,
    EVENT_STATUS,
    EVENT_ERROR
)
from Backend.src.extensions import redis_client


# Constants
EVENT_CHAT_HISTORY = "chat_history"
EVENT_MESSAGE = "message"
MESSAGE_HISTORY_LIMIT = 10

# TODO: #5 Handle Emit and Buffering of Messages for Offline Users
# TODO: Implement Redis Pub/Sub for Offline User Messages

class ChatNamespace(Namespace):
    """
    Handles chat socket events for real-time messaging.
    
    This namespace manages real-time chat interactions between users, including:
    - User authentication via JWT
    - Joining and leaving chat rooms
    - Sending and receiving messages
    - Retrieving chat history
    - Handling disconnections
    """

    def __init__(self, namespace="/chat"):
        """
        Initialize the ChatNamespace.
        
        Args:
            namespace (str, optional): The namespace identifier. Defaults to None.
        """
        super().__init__(namespace)
        self.user_id = None  # Initialize user_id as None
        self.redis_client = redis_client  # Redis client for caching and pub/sub

    # --------------------Standard SocketIO Methods ----------------------------------------------

    def on_connect(self):
        """
        Authenticate user via JWT when they connect and auto-join match rooms.
        
        This method:
        1. Extracts the JWT token from request headers
        2. Validates the token and retrieves the user
        3. Auto-joins the user to their match rooms
        
        Returns:
            None
        """
        try:
            auth_header = request.headers.get("X-Authorization")
            user_id = auth_connecting_user(auth_header)
            if user_id is None:
                disconnect()
                return
            
            self.user_id = user_id
            
            # Cache user's online status
            cache_user_status(self.user_id, True)
            
            print(f"User {self.user_id} connected to /Chat namespace!")

            # Auto-Join all match rooms of the user
            self.auto_join_match_rooms()
            
        except Exception as e:
            print(f"Error during connection: {str(e)}")
            disconnect()
            return False

    @authenticated_only
    def on_join(self, data):
        """
        User joins a chat room (match_id used as room identifier).
        
        Args:
            data (dict): Contains match_id for the room to join
            
        This method:
        1. Validates the match_id
        2. Joins the user to the specified room
        3. Retrieves and sends recent chat history
        """
        try:
            match_id = data.get("match_id")
            match_room = gen_match_room_name(match_id)
            
            if not match_id:
                print("Missing room_id/match_id. Join request ignored.")
                return

            # Join the chat room for match_id
            join_room(match_room)
            print(f"User {self.user_id} joined Match-Chat {match_room}")
            
            # Emit status message to all users in the chat room that the user has joined
            emit(EVENT_STATUS, {"msg": f"User {self.user_id} joined"}, room=match_room)
            
            # Get recent messages from Postgres 
            MatchHelper = MatchModelHelper(match_id=match_id)
            recent_messages = MatchHelper.get_messages(
                limit=MESSAGE_HISTORY_LIMIT, 
                page=1, 
                get_all_messages=False
            )
            
            # Emit Recent Messages to User
            emit(EVENT_CHAT_HISTORY, {
                "match_id": match_id, 
                "messages": recent_messages
            }, room=self.user_id)
            
            # Check for any cached messages for this user in this match
            self._deliver_cached_messages(match_id)
            
        except Exception as e:
            print(f"Error joining chat room: {str(e)}")
            emit(EVENT_ERROR, {"message": "Failed to join chat room"}, room=self.user_id)

    @authenticated_only
    def on_message(self, data):
        """
        Handle message sending.
        
        Args:
            data (dict): Contains match_id and message_content
            
        This method:
        1. Validates the message data
        2. Saves the message to the database
        3. Broadcasts the message to all users in the room
        4. Caches the message for offline users
        """
        try:
            match_id = data.get("match_id")
            message_content = data.get("message_content")
            
            match_room = gen_match_room_name(match_id)

            if not match_id or not message_content:
                print("Invalid message data. Ignored.")
                return

            print(f"User {self.user_id} sent message '{message_content}' in Match-Chat {match_room}")

            # Save message to Postgres - Persisting the Message
            MatchHelper = MatchModelHelper(match_id=match_id)
            saved_message = MatchHelper.save_message_to_match_chat(
                self.user_id, 
                message_content=message_content
            )

            if not saved_message:
                print(f"Failed to save message to DB: {json.dumps(saved_message)}")
                emit(EVENT_ERROR, {"message": "Failed to save message"}, room=self.user_id)
                return
        
            # Create message data for broadcasting
            message_data = {
                "sender": self.user_id, 
                "message": message_content,
                "timestamp": saved_message.created_at.isoformat() if hasattr(saved_message, 'created_at') else None
            }
            
            # Broadcast message to all users in the Match chat room
            emit(EVENT_MESSAGE, message_data, room=match_room)
            
            # Cache message for offline users
            self._cache_message_for_offline_users(match_id, message_data)
            
            # TODO - Broadcast Message to Notification Namespace for Push Notification Service
            
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            emit(EVENT_ERROR, {"message": "Failed to send message"}, room=self.user_id)

    @authenticated_only
    def on_leave(self, data):
        """
        User leaves a chat room.
        
        Args:
            data (dict): Contains match_id for the room to leave
            
        This method:
        1. Validates the match_id
        2. Removes the user from the specified room
        3. Notifies other users in the room
        """
        try:
            match_id = data.get("match_id")
            match_room = gen_match_room_name(match_id)
            
            if not match_id:
                print("Missing match_id. Leave request ignored.")
                return

            leave_room(match_room)
            print(f"User {self.user_id} left Match-Chat {match_room}")

            emit(EVENT_STATUS, {"msg": f"User {self.user_id} left"}, room=match_room)
            
        except Exception as e:
            print(f"Error leaving chat room: {str(e)}")
            emit(EVENT_ERROR, {"message": "Failed to leave chat room"}, room=self.user_id)

    def on_disconnect(self):
        """
        Handle user disconnection and remove them from any match rooms.
        
        This method:
        1. Removes the user from all match rooms
        2. Updates the user's online status
        3. Notifies the user of disconnection
        """
        try:
            if self.user_id is None:
                print("User is not authenticated. Disconnect event ignored.")
                return
        
            # Update user's online status
            cache_user_status(self.user_id, False)
            
            # Auto-leave all match rooms
            self.auto_leave_match_rooms()

            # Emit Disconnect Status Message to User
            emit(EVENT_STATUS, {"msg": f"User {self.user_id} disconnected"}, room=self.user_id)
            print(f"User {self.user_id} disconnected from /Chat namespace!")
            
        except Exception as e:
            print(f"Error during disconnection: {str(e)}")
        
    # --------------------Custom Methods ----------------------------------------------
        
    @authenticated_only
    def get_user_match_rooms(self):
        """
        Retrieve all match rooms where this user is involved.
        
        Returns:
            list: List of match room IDs
        """
        try:
            user = models.User.query.get(self.user_id)
            # Retrieve all match IDs where the user is involved
            match_ids = user.get_match_ids()
            # Generate room IDs for each match - Standardize Room Names "match_<match_id>"
            match_room_ids = [gen_match_room_name(match_id) for match_id in match_ids]
            return match_room_ids
        except Exception as e:
            print(f"Error getting user match rooms: {str(e)}")
            return []
    
    @authenticated_only
    def auto_join_match_rooms(self):
        """
        Retrieve and join all match rooms where this user is Not Joined.
        
        This method:
        1. Gets all match rooms for the user
        2. Joins each room the user is not already in
        3. Notifies the user of auto-joining
        """
        try:
            match_room_ids = self.get_user_match_rooms()
           
            # Join each match room
            for room_id in match_room_ids:
                
                # Join the room if the user is not already in it
                if room_id not in rooms(self.user_id):
                    join_room(room_id)
                    print(f"User {self.user_id} auto-joined Match-Chat {room_id}")
                else:
                    print(f"User {self.user_id} is already in Match-Chat {room_id}")

            emit(EVENT_STATUS, {"msg": f"User {self.user_id} auto-joined Match-Chats on Connection"}, room=self.user_id)
            
        except Exception as e:
            print(f"Error auto-joining match rooms: {str(e)}")
            emit(EVENT_ERROR, {"message": "Failed to auto-join match rooms"}, room=self.user_id)

    @authenticated_only
    def auto_leave_match_rooms(self):
        """
        Leave all match rooms where this user is Joined.
        
        This method:
        1. Gets all match rooms for the user
        2. Leaves each room the user is in
        3. Notifies the user of auto-leaving
        """
        try:
            match_room_ids = self.get_user_match_rooms()
            
            # Leave each match room
            for room_id in match_room_ids:
                if room_id in rooms(self.user_id):
                    leave_room(room_id, sid=self.user_id)
                    print(f"User {self.user_id} auto-left Match-Chat {room_id}")
                else:
                    print(f"User {self.user_id} is not in Match-Chat {room_id}")
                    
            emit(EVENT_STATUS, {"msg": f"User {self.user_id} auto-left Match-Chats on Disconnection"}, room=self.user_id)
            
        except Exception as e:
            print(f"Error auto-leaving match rooms: {str(e)}")
    
    def _cache_message_for_offline_users(self, match_id, message_data):
        """
        Cache message for offline users.
        
        Args:
            match_id (str): The ID of the match
            message_data (dict): The message data to cache
        """
        try:
            # Get the match to find the other user
            match = models.Match.query.get(match_id)
            if not match:
                return
                
            # Determine the other user in the match
            other_user_id = match.matchee_id if match.matcher_id == self.user_id else match.matcher_id
            
            # Check if the other user is offline
            from Backend.src.sockets.socket_helpers import is_user_online
            if not is_user_online(other_user_id):
                # Store message in a list for the offline user
                cache_key = f"user:{other_user_id}:match:{match_id}:messages"
                self.redis_client.rpush(cache_key, json.dumps(message_data))
                self.redis_client.expire(cache_key, 86400)  # Expire after 24 hours
                print(f"Cached message for offline user {other_user_id} in match {match_id}")
                
        except Exception as e:
            print(f"Error caching message for offline user: {str(e)}")
            
    def _deliver_cached_messages(self, match_id):
        """
        Deliver cached messages to a user who just joined a chat room.
        
        Args:
            match_id (str): The ID of the match
        """
        try:
            # Check if there are any cached messages for this user in this match
            cache_key = f"user:{self.user_id}:match:{match_id}:messages"
            cached_messages = self.redis_client.lrange(cache_key, 0, -1)
            
            if cached_messages:
                # Convert cached messages from bytes to dict
                messages = [json.loads(msg.decode('utf-8')) for msg in cached_messages]
                
                # Emit cached messages to the user
                for message in messages:
                    emit(EVENT_MESSAGE, message, room=self.user_id)
                    
                # Clear the cache
                self.redis_client.delete(cache_key)
                print(f"Delivered {len(messages)} cached messages to user {self.user_id} for match {match_id}")
                
        except Exception as e:
            print(f"Error delivering cached messages: {str(e)}")
            
# Register the chat namespace (Currently in App.py)
#socketio.on_namespace(ChatNamespace("/chat"))
