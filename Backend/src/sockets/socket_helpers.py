"""
Author: Joshua Ferguson

Implementation of helper functions for socket operations.

This module provides the following functions:

# Authentication Helpers

- `auth_connecting_user()`: Authenticates a user based on their JWT token.
- `authenticated_only()`: Decorator to ensure a user is authenticated.

# Room Management Helpers

- `standardize_room_name()`: Adds a prefix to a room name.
- `gen_match_room_name()`: Generates a match room name.
- `gen_game_room_name()`: Generates a game room name.
- `gen_notification_room_name()`: Generates a notification room name.

# User Status Helpers

- `cache_user_status()`: Caches a user's online status.
- `is_user_online()`: Checks if a user is online.
"""

from functools import wraps
from flask import request
from flask_socketio import disconnect, emit

from Backend.src.services.auth_service import get_user_from_token
from Backend.src.extensions import redis_client

# Constants
ROOM_PREFIX_MATCH = "match_"
EVENT_STATUS = "status"
EVENT_ERROR = "error"
USER_STATUS_TTL = 3600  # 1 Hour in Seconds

def auth_connecting_user(token):
    """
    Authenticate a user based on their JWT token.
    
    Args:
       token (str): JWT token
        
    Returns:
        str: The user ID if authentication is successful, None otherwise
    """
    
    if not token:
        print("Missing Token. Connection refused.")
        return None
    try:

        # Extract Bearer Token
        user = get_user_from_token(token)
        if user is None:
            raise Exception("User not found or Invalid Token. Connection refused.")

        return user.id

    except Exception as e:
        print(f"Error authenticating user: {str(e)}")
        return None

def authenticated_only(f):
    """
    Decorator to ensure a user is authenticated.
    
    Args:
        f (function): The function to decorate
        
    Returns:
        function: The decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Get user ID from the namespace
            user_id = args[0].user_id if args else None
            
            if not user_id:
                raise Exception("User is not authenticated")
                
            return f(*args, **kwargs)
            
        except Exception as e:
            print(f"Error in authenticated_only decorator: {str(e)}")
            emit(EVENT_ERROR, {"message": "Authentication error"}, room=request.sid)
            disconnect()
            return
            
    return decorated_function

def standardize_room_name(room_name, prefix):
    """
    Add a prefix to a room name.
    
    Args:
        room_name (str): The room name
        prefix (str): The prefix to add
        
    Returns:
        str: The standardized room name
    """
    try:
        if not room_name:
            return None
            
        if room_name.startswith(prefix):
            return room_name
            
        return f"{prefix}{room_name}"
        
    except Exception as e:
        print(f"Error standardizing room name: {str(e)}")
        return None

def gen_match_room_name(match_id):
    """
    Generate a match room name.
    
    Args:
        match_id (str): The match ID
        
    Returns:
        str: The match room name
    """
    try:
        if not match_id:
            return None
            
        return standardize_room_name(match_id, ROOM_PREFIX_MATCH)
        
    except Exception as e:
        print(f"Error generating match room name: {str(e)}")
        return None

def cache_user_status(user_id, is_online):
    """
    Cache a user's online status.
    
    Args:
        user_id (str): The user ID
        is_online (bool): Whether the user is online
    """
    try:
        if not user_id:
            return
            
        cache_key = f"user:{user_id}:status"
        
        if is_online:
            redis_client.setex(cache_key, USER_STATUS_TTL, "online")
        else:
            redis_client.delete(cache_key)
            
    except Exception as e:
        print(f"Error caching user status: {str(e)}")

def is_user_online(user_id):
    """
    Check if a user is online.
    
    Args:
        user_id (str): The user ID
        
    Returns:
        bool: True if the user is online, False otherwise
    """
    try:
        if not user_id:
            return False
            
        cache_key = f"user:{user_id}:status"
        status = redis_client.get(cache_key)
        
        return status is not None and status.decode('utf-8') == "online"
        
    except Exception as e:
        print(f"Error checking user status: {str(e)}")
        return False