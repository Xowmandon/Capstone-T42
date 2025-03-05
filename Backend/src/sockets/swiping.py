from flask import Flask, request
from flask_socketio import SocketIO, Namespace, disconnect, emit, join_room, leave_room
from flask_jwt_extended import JWTManager, decode_token
import redis

from Backend.src.extensions import db
import  Backend.src.models as models
from Backend.src.services.auth_service import get_user_from_token
# Listen for Swipe Events, Emits Back Successful Match Message if Swipe is accepted

# TODO: Handle Emit and Buffering of Successful Matches for Offline Users
# TODO: Implement Redis Pub/Sub for Offline User Successful Match 


class SwipeNamespace(Namespace):
    def __init__(self, namespace=None):
        super().__init__(namespace)
        self.user_id = None  # Initialize user_id as None


    # -----------------Main Websocket Events---------------------

    def on_connect(self):
        """Authenticate user via JWT when they connect."""

        user_token = request.args.get("token")
        
        if not user_token:
            print("Missing token. Connection refused.")
            disconnect()
            return False

        user = get_user_from_token(user_token)
        
        if user is None:
            print("Invalid JWT token or User Does not Exist. Connection refused.")
            disconnect()
            return False

        self.user_id = user.id
        
        print(f"User {self.user_id} connected to Swipe namespace!")

    def on_swipe(self, data):
        """Process swipe event."""
        if self.user_id is None:  # Cleaner authentication check
            print("User is not authenticated. Swipe event ignored.")
            return
        
        swipee_id = data.get("swipee_id")
        new_swipe_result = data.get("swipe_result")

        if not swipee_id or not new_swipe_result:
            print("Invalid swipe data received.")
            return
        
        print(f"User {self.user_id} swiped '{new_swipe_result}' on User {swipee_id}")

        # Process swipe logic
        processed_swipe = models.swipe.SwipeProcessor.process_new_swipe(self.user_id, swipee_id, new_swipe_result)

        # Process New Match if Swipe is Accepted - Create Match and Emit to Both Users
        if processed_swipe and processed_swipe.swipe_result == "ACCEPTED":
            print(f"New Match Detected: {processed_swipe}")
            self.process_new_match(swipee_id)

    def on_disconnect(self):
        """Disconnect event."""
        
        if self.user_id is None: #Handle Disconnection of Unauthenticated Users without Attrubute Error
            print("Invalid user_id User disconnected from Swipe namespace - Ignored.")
        else:
            print(f"User {self.user_id} disconnected from Swipe namespace.")
            
        # Emit Disconnect Status Message to User
        emit("status", {"msg": f"User {self.user_id} disconnected"}, room=self.user_id)
        return
        #self.user_id = None

    # -----------------Custom/Helper Methods & Events---------------------

    def process_new_match(self, matchee_id):
        """
        Process the New Match Event and Create a New Match

        Args:
            matchee_id (int): The ID of the user being matched.

        Returns:
            - None if not a Successful Match
            - If Successful Match Detected, Emits success message to both users.
        """
        try:
            # Create New Match and Push to DB
            new_match = models.match.Match().create_match(matcher_id=self.user_id, matchee_id=matchee_id)
            
            if new_match:
                print(f"Match Created: {new_match}")

                # Notify both users about the successful match
                emit('successful_match', {'matchee_id': matchee_id, 'match_id': new_match.id}, room=self.user_id)
                emit('successful_match', {'matchee_id': self.user_id, 'match_id': new_match.id}, room=matchee_id)
                
                 # TODO - Broadcast Message to Notification Namespace for Push Notification Service
            else:
                print(f"Failed to create match between {self.user_id} and {matchee_id}")
                emit('match_creation_failed', {'matchee_id': matchee_id, 'message': 'Match creation failed'}, room=self.user_id)

        except Exception as e:
            print(f"Error in processing match: {str(e)}")
            emit('match_creation_failed', {'matchee_id': matchee_id, 'message': 'Internal server error'}, room=self.user_id)

# Register the chat namespace (CURRENTLY IN APP)
#socketio.on_namespace(SwipeNamespace("/swipe"))

