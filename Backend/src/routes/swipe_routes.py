
#-----Swipe Routes-----
# WIP - Not yet implemented For the Swipe Routes

from flask import request, jsonify, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import logging

from  Backend.src.extensions import db # Import the DB Instance
import  Backend.src.models as models # Import the Models and Schemas
#from  Backend.src.routes import app # Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# Blueprint for the Swipe Routes
swipe_bp = Blueprint('swipe_bp', __name__)


swipe_schema = models.swipe.SwipeSchema()

# -----Swipe Routes-----
    

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
    swipee_id = request.get_json().get('swipee_id')
    swipe_result = request.get_json().get('swipe_result')
    
    if swiper_id is None or swipee_id is None:
        return jsonify({"error": "One or more users not found."}), 404
    
    processed_swipe = models.swipe.SwipeProcessor.process_new_swipe(swiper_id, swipee_id, swipe_result)
    
    if processed_swipe.swipe_result == "ACCEPTED":
        # Create New Match, Push to DB, and Emit MSG Back to Client
        print(f"New Match Detected from Swipe - {str(processed_swipe)}")
        
        new_match = models.match.Match().create_match(matcher_id=swiper_id,matchee_id=swipee_id)

        if new_match is not None:
            # Emit Successful Match to Client, with Swipee ID and Match ID
            emit('successful_match', {'swipee_id': swipee_id, 'match_id': new_match.id})
    # Log the success and return the message
    #logging.info(f"Swipe created successfully! - {swipe}")
    return "Swipe created successfully!", 201
    
    
    
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