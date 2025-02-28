from flask import Flask, request
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room
from flask_jwt_extended import JWTManager, decode_token
from Backend.src.extensions import redis_client
from Backend.app import socketio

class ChatNamespace(Namespace):
    """Handles chat socket events for real-time messaging."""

    def on_connect(self):
        """Authenticate user via JWT when they connect."""
        self.user_token = request.args.get("token")
        if not self.user_token:
            print("Missing token. Connection refused.")
            return False  # Reject connection

        try:
            decoded_token = decode_token(self.user_tokentoken)
            self.user_id = decoded_token.get("sub")
            print(f"User {self.user_token} connected to chat namespace!")
        except:
            print("Invalid JWT token. Connection refused.")
            return False

    def on_join(self, data):
        """User joins a chat room (match_id used as room identifier)."""
        match_id = data["match_id"]
        join_room(match_id,sid=self.user_token)
        print(f"User_id {self.user_id} joined Match-Chat {match_id}")

        emit("status", {"msg": f"User {self.user_token} joined"}, room=match_id)

    def on_message(self, data):
        """Handle message sending."""
        match_id = data["match_id"]
        message = data["message"]
    
        print(f"User_id {self.user_id} sent message '{message} in Match-Chat  {match_id}")
        
        # Save message temporarily in Redis
        redis_client.rpush(match_id, f"{self.user_id}:{message}")

        # Broadcast message to all users in the chat room
        emit("message", 
             {"messager": self.user_token, "message": message}, 
             room=match_id
             )

    def on_leave(self, data):
        """User leaves a chat room."""
        match_id = data["match_id"]
        leave_room(match_id)
        print(f"User {self.user_id} left room {match_id}")

        emit("status", {"msg": f"User {self.user_id} left"}, room=match_id)

    def on_disconnect(self):
        """Handle user disconnection."""
        print(f"User {self.user_id} disconnected")


# Register the chat namespace
socketio.on_namespace(ChatNamespace("/chat"))