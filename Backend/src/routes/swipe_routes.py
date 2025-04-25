# Author: Joshua Ferguson

#-----Swipe Routes-----


from datetime import datetime, timezone
from flask import request, jsonify, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import logging

from  Backend.src.extensions import db # Import the DB Instance
import  Backend.src.models as models # Import the Models and Schemas
#from  Backend.src.routes import app # Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_socketio import emit

from Backend.src.services.messaging_service import send_fcm_notification
# Blueprint for the Swipe Routes
swipe_bp = Blueprint('swipe_bp', __name__)


swipe_schema = models.swipe.SwipeSchema()

# -----Swipe Routes-----
def notify_new_match(user_ids, new_match):
    """
    Notify users of a new match through FCM
    """
    try:
        for id in user_ids:
            # Get Name of the User
            user = models.user.User.query.get(id)
            # Send FCM Notification
            send_fcm_notification(
                    user_id=id,
                    title="New Match!",
                    body=f"Matched with {user.name}",
                    data_payload=models.match.match_schema.dump(new_match)
                )
    except Exception as e:
        raise Exception(f"Error notifying users of new match: {str(e)}")

# Post A Swipe Event to the Database - Swipe Right or Left
# POST /Users/Swipes 
# 0 - Pending (Swiper Swiped Right, Swipee Hasn't Swiped Back Yet), 
# 1 - Accepted (Both Swiped Right),
# 2 - Rejected (Swiper Swipped Right, Swipee Swiped Left)
@swipe_bp.route('/users/swipes', methods=['POST'])
@jwt_required()
def create_swipe():
    """
    Summary: Create a new swipe event or Update and add it to the database.
    
    # TODO: Check if Swipe Already Exists, Update Instead of Creating New If So
    
    
    Payload: JSON object with the following fields:
        - swipee_id, stry, required
        - swipe_result: int, required

    Returns:
        str: A message indicating the success or failure of the swipe creation.
        Returns standard response codes (see above):
    """

    swiper_id = get_jwt_identity()
    data = request.get_json()
    swipee_id = data.get('swipee_id')
    swipe_result = data.get('swipe_result')
    
    if swiper_id is None or swipee_id is None:
        return jsonify({"error": "One or more users not found."}), 404
    
    try:
        processed_swipe = models.swipe.SwipeProcessor.process_new_swipe(swiper_id, swipee_id, swipe_result)
    except Exception as e:
       return jsonify({"error": "Failed to process swipe.", "details": str(e)}), 500
   
    # Create New Match, Push to DB, and Emit MSG Back to Client
    if processed_swipe.swipe_result == "ACCEPTED":
        print(f"New Match Detected from Swipe - {processed_swipe.swiper_id} <--> {processed_swipe.swipee_id}")
        
        try:
            
                        
            # Set Online Status to Now
            current_user = models.user.User.query.get(swiper_id)
            current_user.last_online = datetime.now(timezone.utc)
            db.session.commit()
            
            # Create a new match event
            new_match = models.match.Match().create_match(matcher_id=swiper_id,matchee_id=swipee_id)
            if new_match is None:
                return jsonify({"error": "Failed to create a new match."}), 500
            
            matched_user = models.user.User.query.get(swipee_id)
            if matched_user is None:
                return jsonify({"error": "Matched user not found."}), 404
            
    
            # b59f1987-2943-4cdb-be0e-c0b60a13a025
            #H - 000519.f1637da8f2c14d39b61d3653a8797532.1310
            
             # Notify Users of the New Match
            return jsonify({"status": "NEW", "match_id": str(new_match.id)}), 201
        
            # FCM Notifs
            #notify_new_match([swiper_id, swipee_id], new_match)

        except Exception as e:
            return jsonify({"error": "Failed to create a new match.", "details": str(e)}), 500

    # Log the success and return the message
    #logging.info(f"Swipe created successfully! - {swipe}")
    return jsonify({"status": "SUCCESS"}), 201

    
@swipe_bp.route('/users/swipes>', methods=['GET'])
def get_swipes():
    """
    Summary: Get all swipes for a user by ID.
        
    Returns:
        JSON with list: A list of swipes for the user.
        0 - Pending (Swiper Swiped Right, Swipee Hasn't Swiped Back Yet),
        1 - Accepted (Both Swiped Right),
        2 - Rejected (Swiper Swipped Right, Swipee Swiped Left)

        
    """
    
    # Get the data from the request body
    data = request.get_json()
    
    email = data.get('email')
    
    # Get the swipes for the user
    swipes = models.swipe.Swipe.query.filter_by(swiper=email).all()
    
    # Return the list of swipes  
    return jsonify([swipe_schema.dump(swipe) for swipe in swipes])

@swipe_bp.route('/users/swipes', methods=['PUT'])
def update_swipe():
    """
    Summary: Update a user by Email.
    
    Payload: JSON object with the following fields:
        - swiper_email: str, required
        - swipee_email: str, required
        
        # Values to Potentially Update
        -  "swipe_result": 1),  required
        -  "swipe_date": "2021-09-01"), required
        
    """
    
    # Fields Allowed to be Updated
    # TODO: Standardize the Fields that can be Updated to a Single Location
    changable_fields = ['swipe_result', 'swipe_date']
     
    # Payload from Request
    data = request.get_json()
    
    # Parse Payload for Emails
    swipe_schema = models.swipe.SwipeSchema()
 
    # Load and Validate the Swipe Payload
    new_swipe = swipe_schema.load(data)
    
    # Retrieve Swipe from Database
    swipe = models.swipe.Swipe.query.filter_by(swiper=new_swipe.swiper.email, swipee=new_swipe.swipee_email).first()
    
    if swipe is None:
        return jsonify({"error": "Swipe not found."}), 404
    # Update User Data with New User Data, Excluding the Email and ID
    # Only Updates Values Sent in payload with Validated Data (Not None)
     
    for field in changable_fields:
        new_attr = getattr(new_swipe, field)
        if new_attr is not None:
            setattr(swipe, field, new_attr)
            
               
    # Commit the changes to the database
    db.session.commit()
        
    # Return the updated Swipe and a success message
    return jsonify({"success": "Swipe updated successfully.", "Swipe": swipe_schema.dump(swipe)}), 200

# TODO: Implement Delete Swipe Route, Not Currently Needed
#@swipe_bp.route('/users/swipes', methods=['DELETE'])
#def delete_swipe():

#-----End of Swipe Routes-----