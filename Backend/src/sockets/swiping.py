from flask import Flask, request
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room
from flask_jwt_extended import JWTManager, decode_token
import redis

from Backend.app import socketio
from Backend.src.extensions import db
from Backend.src.models import Swipe, Match


# Listen for Swipe Events, Emits Back Successful Match Message if Swipe is accepted
class SwipeNamespace(Namespace):
    def on_connect(self):
        """Authenticate user via JWT when they connect."""
        self.user_token = request.args.get("token")
        if not self.user_token:
            print("Missing token. Connection refused.")
            return False  # Reject connection

        try:
            decoded_token = decode_token(self.user_tokentoken)
            self.user_id = decoded_token.get("sub")
            print(f"User {self.user_token} connected to Swipe namespace!")
        except:
            print("Invalid JWT token. Connection refused.")
            return False

    def on_disconnect(self):
        print('Client disconnected')

    def on_swipe(self, data):
        """
        Process the swipe event and check if the swipe is accepted.

        Args:
            data (dict): A dictionary containing the swipe data, including the swipee_id and swipe_result.

        Returns:
            None if not a Successful Match
            
            If Successful Match Detected, Returns Success Msg and swipee_id and Created match_id
        """
        # Get Current User (self.user_token)
        # Get User that Current User Swiped On 
        swipee_id = data["swipee_id"]
        
        # Get Swipe Result
        new_swipe_result = data["swipe_result"]
        
        print(f"User {self.user_id} Swiped '{new_swipe_result} on User {swipee_id}")
        
        # Check if Swipe Exists for the two Users
        # Meaning, There is a record Where Swipee equals Current Swiper, and Vice Versa
        swipe_exists = Swipe.query.filter_by(swiper_id=swipee_id, swipee_id=self.user_id).first()
        
        # If swipe does not exist, create a new swipe instance
        if not swipe_exists:
            
            new_swipe = Swipe(swiper_id=self.user_id, swipee_id=swipee_id, swipe_result=new_swipe_result)
            db.session.add(new_swipe)
            db.session.commit()
            print(f"New swipe created - {Swipe.swipee_id}, {Swipe.swiper_id}, {Swipe.swipe_result}")
            pass
        
        # Swipe Exits - Good to Compare and Check for New Match
        
        # If Already Rejected, Pass
        elif swipe_exists.swipe_result == "REJECTED":
            pass
        
        # If New Swipe is Rejected, set Stored Swipe Record as Rejected, Pass
        elif new_swipe_result == "REJECTED":
            swipe_exists.swipe_result = "REJECTED"
            pass

        # If Both Stored Swipe and New is PENDING, Turn to Accepted, Indicating Successful Match
        elif swipe_exists.swipe_result == "PENDING" and new_swipe_result == "PENDING":
            swipe_exists.swipe_result == "ACCEPTED"
        
            # Create New Match, Push to DB, and Emit MSG Back to Client
            print(f"New Match Detected from Swipe - {Swipe.swipee_id}, {Swipe.swiper_id}, {Swipe.swipe_result}")
            
            new_match = Match().create_match(matcher_id=self.user_id,matchee_id=swipee_id)
            
            if new_match:
                # Emit Successful Match to Client, with Swipee ID and Match ID
                emit('successful_match', {'swipee_id': swipee_id, 'match_id': new_match.id})
            else:
                # Emit Error Code, Tried to Create Match, Failed
                emit('match_creation_failed', {'Current User -> swipee_id': swipee_id})

# Register the chat namespace
socketio.on_namespace(SwipeNamespace("/swipe"))