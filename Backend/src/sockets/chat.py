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
from flask import  request
from flask_socketio import Namespace, emit, join_room, leave_room, disconnect, rooms

from Backend.src.models.model_helpers import MatchModelHelper
import Backend.src.models as models
from Backend.src.services.auth_service import get_user_from_token
from Backend.src.sockets.socket_helpers import auth_connecting_user, gen_match_room_name
from Backend.src.extensions import redis_client


# TODO: Handle Emit and Buffering of Messages  for Offline Users
# TODO: Implement Redis Pub/Sub for Offline User Messages

class ChatNamespace(Namespace):
    """Handles chat socket events for real-time messaging."""

    # --------------------Standard SocketIO Methods ----------------------------------------------

    def on_connect(self):
        """Authenticate user via JWT when they connect and auto-join match rooms."""
        
        auth_header = request.headers.get("Authorization")
        user_id = auth_connecting_user(auth_header)
        if user_id is None:
            disconnect()
            return
        
        self.user_id = user_id
        
        # Store user_id for easy access
        print(f"User {self.user_id} connected to /Chat namespace!")

        # Auto-Join all match rooms of the user
        self.auto_join_match_rooms()

    def on_join(self, data):
        """User joins a chat room (match_id used as room identifier)."""
        match_id = data.get("match_id")
        match_room= gen_match_room_name(match_id)
        
        if not match_id:
            print("Missing room_id/match_id. Join request ignored.")
            return

        # Join the chat room for match_id
        join_room(match_room)
        print(f"User {self.user_id} joined Match-Chat {match_room}")
        
        # Emit status message to all users in the chat room that the user has joined
        emit("status", {"msg": f"User {self.user_id} joined"}, room=match_room)
        
        
        # Get 10 Most Recent Messages from Postgres 
        MatchHelper = MatchModelHelper(match_id=match_id)
        recent_messages = MatchHelper.get_messages(limit=10, page=1, get_all_messages=False)
        
        # Emit Recent Messages to User
        emit("chat_history", {"match_id": match_id, "messages": recent_messages}, room=self.user_id)
        
        # TODO - Implement Caching/Queueing Messages in Redis
        # Retrieve last 10 messages from Redis/PostGres for chat history
        #chat_history = redis_client.lrange(str(match_id), -10, -1)
        #chat_messages = [json.loads(msg) for msg in chat_history] if chat_history else []
        #emit("chat_history", {"match_id": match_id, "messages": chat_messages}, room=self.user_id)

    def on_message(self, data):
        """Handle message sending."""
        match_id = data.get("match_id")
        match_room = gen_match_room_name(match_id)
        message_content = data.get("message_content")

        if not match_id or not message_content:
            print("Invalid message data. Ignored.")
            return

        print(f"User {self.user_id} sent message '{message_content}' in Match-Chat {match_room}")

        # Save message temporarily in Redis
        #message_data = json.dumps({"messager": self.user_id, "message": message})
        #redis_client.rpush(str(match_id), message_data)

        # Save message to Postgres - Persisting the Message
        MatchHelper = MatchModelHelper(match_id=match_id)
        saved_message = MatchHelper.save_message_to_match_chat(self.user_id, message_content=message_content)

        if not saved_message:
            print(f"Failed to save message to DB: {json.dumps(saved_message)}")
            return
    
        # Broadcast message to all users in the Match chat room, CLient should Update UI 
        emit("message", {"sender": self.user_id, "message": message_content}, room=match_room)
        
        # TODO - Broadcast Message to Notification Namespace for Push Notification Service

    def on_leave(self, data):
        """User leaves a chat room."""
        match_id = data.get("match_id")
        match_room = gen_match_room_name(match_id)
        if not match_id:
            print("Missing match_id. Leave request ignored.")
            return

        leave_room(match_room)
        print(f"User {self.user_id} left Match-Chat {match_room}")

        emit("status", {"msg": f"User {self.user_id} left"}, room=match_room)

    def on_disconnect(self):
        """Handle user disconnection and remove them from any match rooms."""
        
        if self.user_id is None:
            print("User is not authenticated. Disconnect event ignored.")
            return
    
        user = models.User.query.get(self.user_id)
        
        # Retrieve all match IDs where the user is involved
        match_ids = user.get_match_ids()
        
        # Generate room IDs for each match - Standardize Room Names "match_<match_id>"
        match_room_ids = [gen_match_room_name(match_id) for match_id in match_ids] # room_id is the match_id
        
        # Join each match room
        for match_room in match_room_ids:
            # Join the room if the user is not already in it
            if match_room  in rooms(self.user_id):
                leave_room(match_room, sid=self.user_id)
                print(f"User {self.user_id} left room: {match_room}")

        # Emit Disconnect Status Message to User
        emit("status", {"msg": f"User {self.user_id} disconnected"}, room=self.user_id)
        print(f"User {self.user_id} disconnected from /Chat namespace!")
        
        
    # --------------------Custom Methods ----------------------------------------------
        
    def get_user_match_rooms(self):
        """Retrieve all match rooms where this user is involved."""
        user = models.User.query.get(self.user_id)
        # Retrieve all match IDs where the user is involved
        match_ids = user.get_match_ids()
        # Generate room IDs for each match - Standardize Room Names "match_<match_id>"
        match_room_ids = [gen_match_room_name(match_id) for match_id in match_ids] # room_id is the match_id
        return match_room_ids
    
    def auto_join_match_rooms(self):
        """Retrieve and join all match rooms where this user is Not Joined."""
        match_room_ids = self.get_user_match_rooms()
       
        # Join each match room
        for room_id in match_room_ids:
            
            # Join the room if the user is not already in it
            if room_id not in rooms(self.user_id):
                join_room(room_id)
                print(f"User {self.user_id} auto-joined Match-Chat {room_id}")

            else:
                print(f"User {self.user_id} is already in Match-Chat {room_id}")

        emit("status", {"msg": f"User {self.user_id} auto-joined Match-Chats on Connection"}, room=self.user_id)

    def auto_leave_match_rooms(self):
        """Leave all match rooms where this user is Joined."""
        
        match_room_ids = self.get_user_match_rooms()
        
        # Leave each match room
        for room_id in match_room_ids:
            if room_id in rooms(self.user_id):
                leave_room(room_id, sid=self.user_id)
                print(f"User {self.user_id} auto-left Match-Chat {room_id}")
            else:
                print(f"User {self.user_id} is not in Match-Chat {room_id}")
                
        emit("status", {"msg": f"User {self.user_id} auto-left Match-Chats on Disconnection"}, room=self.user_id)    
            
# Register the chat namespace (Currently in App.py)
#socketio.on_namespace(ChatNamespace("/chat"))
