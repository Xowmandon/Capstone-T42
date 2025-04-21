"""
Author: Joshua Ferguson

Implementation of the `NotificationNamespace` class, which handles real-time notifications.

The `NotificationNamespace` class provides the following methods:

# Main WebSocket Event Handlers

- `on_connect()`: Authenticates the user via JWT when they connect.
- `on_disconnect()`: Handles user disconnection.

# Custom Methods and Helpers

- `send_notification()`: Sends a notification to a specific user.
- `broadcast_notification()`: Broadcasts a notification to all users.
- `get_user_notifications()`: Retrieves all notifications for a user.
- `mark_notification_read()`: Marks a notification as read.
"""

import json
from flask import request
from flask_socketio import Namespace, emit, disconnect

from Backend.src.sockets.socket_helpers import (
    auth_connecting_user,
    authenticated_only,
    cache_user_status,
    EVENT_STATUS,
    EVENT_ERROR
)
from Backend.src.extensions import redis_client

# Constants
EVENT_NOTIFICATION = "notification"
EVENT_NOTIFICATIONS = "notifications"
NOTIFICATION_TTL = 86400  # 24 hours in seconds

class NotificationNamespace(Namespace):
    """
    Handles real-time notifications for users.
    
    This namespace manages notification interactions, including:
    - User authentication via JWT
    - Sending and receiving notifications
    - Managing notification status (read/unread)
    - Handling disconnections
    """

    def __init__(self, namespace=None):
        """
        Initialize the NotificationNamespace.
        
        Args:
            namespace (str, optional): The namespace identifier. Defaults to None.
        """
        super().__init__(namespace)
        self.user_id = None
        self.redis_client = redis_client

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
            auth_header = request.headers.get("X-Authorization")
            user_id = auth_connecting_user(auth_header)
            if user_id is None:
                disconnect()
                return
            
            self.user_id = user_id
            
            # Cache user's online status
            cache_user_status(self.user_id, True)
            
            print(f"User {self.user_id} connected to /Notifications namespace!")
            
            # Send any pending notifications
            self._send_pending_notifications()
            
        except Exception as e:
            print(f"Error during connection: {str(e)}")
            disconnect()
            return False

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
            print(f"User {self.user_id} disconnected from /Notifications namespace!")
            
        except Exception as e:
            print(f"Error during disconnection: {str(e)}")

    @authenticated_only
    def send_notification(self, data):
        """
        Send a notification to a specific user.
        
        Args:
            data (dict): Contains recipient_id, notification_type, and message
            
        This method:
        1. Validates the notification data
        2. Creates the notification
        3. Sends it to the recipient if online, or caches it if offline
        """
        try:
            recipient_id = data.get("recipient_id")
            notification_type = data.get("notification_type")
            message = data.get("message")
            
            if not all([recipient_id, notification_type, message]):
                print("Invalid notification data. Ignored.")
                return
                
            notification_data = {
                "sender_id": self.user_id,
                "recipient_id": recipient_id,
                "type": notification_type,
                "message": message,
                "timestamp": None,  # Will be set when delivered
                "read": False
            }
            
            # Check if recipient is online
            from Backend.src.sockets.socket_helpers import is_user_online
            if is_user_online(recipient_id):
                # Send notification immediately
                emit(EVENT_NOTIFICATION, notification_data, room=recipient_id)
                print(f"Notification sent to user {recipient_id}")
            else:
                # Cache notification for offline user
                self._cache_notification(recipient_id, notification_data)
                print(f"Notification cached for offline user {recipient_id}")
                
        except Exception as e:
            print(f"Error sending notification: {str(e)}")
            emit(EVENT_ERROR, {"message": "Failed to send notification"}, room=self.user_id)

    @authenticated_only
    def broadcast_notification(self, data):
        """
        Broadcast a notification to all users.
        
        Args:
            data (dict): Contains notification_type and message
            
        This method:
        1. Validates the notification data
        2. Creates the notification
        3. Broadcasts it to all users
        """
        try:
            notification_type = data.get("notification_type")
            message = data.get("message")
            
            if not all([notification_type, message]):
                print("Invalid notification data. Ignored.")
                return
                
            notification_data = {
                "sender_id": self.user_id,
                "type": notification_type,
                "message": message,
                "timestamp": None,  # Will be set when delivered
                "read": False
            }
            
            # Broadcast to all users
            emit(EVENT_NOTIFICATION, notification_data, broadcast=True)
            print("Notification broadcasted to all users")
            
        except Exception as e:
            print(f"Error broadcasting notification: {str(e)}")
            emit(EVENT_ERROR, {"message": "Failed to broadcast notification"}, room=self.user_id)

    @authenticated_only
    def get_user_notifications(self):
        """
        Retrieve all notifications for the current user.
        
        This method:
        1. Retrieves all notifications from Redis
        2. Sends them to the user
        """
        try:
            # Get all notifications for the user
            notifications = self._get_cached_notifications(self.user_id)
            
            # Send notifications to the user
            emit(EVENT_NOTIFICATIONS, {"notifications": notifications}, room=self.user_id)
            print(f"Sent {len(notifications)} notifications to user {self.user_id}")
            
        except Exception as e:
            print(f"Error getting user notifications: {str(e)}")
            emit(EVENT_ERROR, {"message": "Failed to get notifications"}, room=self.user_id)

    @authenticated_only
    def mark_notification_read(self, data):
        """
        Mark a notification as read.
        
        Args:
            data (dict): Contains notification_id
            
        This method:
        1. Validates the notification ID
        2. Marks the notification as read in Redis
        """
        try:
            notification_id = data.get("notification_id")
            
            if not notification_id:
                print("Invalid notification ID. Ignored.")
                return
                
            # Mark notification as read in Redis
            cache_key = f"user:{self.user_id}:notifications"
            notifications = self._get_cached_notifications(self.user_id)
            
            for notification in notifications:
                if notification.get("id") == notification_id:
                    notification["read"] = True
                    break
                    
            # Update notifications in Redis
            self.redis_client.setex(
                cache_key,
                NOTIFICATION_TTL,
                json.dumps(notifications)
            )
            
            print(f"Marked notification {notification_id} as read for user {self.user_id}")
            
        except Exception as e:
            print(f"Error marking notification as read: {str(e)}")
            emit(EVENT_ERROR, {"message": "Failed to mark notification as read"}, room=self.user_id)

    def _cache_notification(self, recipient_id, notification_data):
        """
        Cache a notification for an offline user.
        
        Args:
            recipient_id (str): The ID of the recipient
            notification_data (dict): The notification data to cache
        """
        try:
            cache_key = f"user:{recipient_id}:notifications"
            
            # Get existing notifications
            notifications = self._get_cached_notifications(recipient_id)
            
            # Add new notification
            notifications.append(notification_data)
            
            # Update notifications in Redis
            self.redis_client.setex(
                cache_key,
                NOTIFICATION_TTL,
                json.dumps(notifications)
            )
            
        except Exception as e:
            print(f"Error caching notification: {str(e)}")

    def _get_cached_notifications(self, user_id):
        """
        Get cached notifications for a user.
        
        Args:
            user_id (str): The ID of the user
            
        Returns:
            list: List of notifications
        """
        try:
            cache_key = f"user:{user_id}:notifications"
            cached_data = self.redis_client.get(cache_key)
            
            if cached_data:
                return json.loads(cached_data.decode('utf-8'))
            return []
            
        except Exception as e:
            print(f"Error getting cached notifications: {str(e)}")
            return []

    def _send_pending_notifications(self):
        """
        Send any pending notifications to the user.
        
        This method:
        1. Retrieves all notifications from Redis
        2. Sends them to the user
        3. Clears the notifications from Redis
        """
        try:
            notifications = self._get_cached_notifications(self.user_id)
            
            if notifications:
                # Send notifications to the user
                emit(EVENT_NOTIFICATIONS, {"notifications": notifications}, room=self.user_id)
                print(f"Sent {len(notifications)} pending notifications to user {self.user_id}")
                
                # Clear notifications from Redis
                cache_key = f"user:{self.user_id}:notifications"
                self.redis_client.delete(cache_key)
                
        except Exception as e:
            print(f"Error sending pending notifications: {str(e)}")

# Register the notifications namespace (Currently in App.py)
#socketio.on_namespace(NotificationNamespace("/notifications"))