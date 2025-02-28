
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
        - swipe_date: str, required
        
    Returns:
        str: A message indicating the success or failure of the swipe creation.
        Returns standard response codes (see above):
    """
    
    try:
        
        # Get the data from the request body
        data = request.get_json()
    
        swiper = db.session.query(models.user.User).filter(models.user.User.email == data.get('swiper_email')).first()
        swipee = db.session.query(models.user.User).filter(models.user.User.email == data.get('swipee_email')).first()
        
        if swiper is None or swipee is None:
            return jsonify({"error": "One or more users not found."}), 404
        
        # Check if the swipe already exists bidirectionally - Filter by email
        swiper_swipe = models.swipe.Swipe.query.filter_by(swiper=swiper, swipee=swipee).first()
        swipee_swipe = models.swipe.Swipe.query.filter_by(swiper=swipee, swipee=swiper).first()
        
        if swiper_swipe is not None:
            
            new_result = data.get('swipe_result')
            if new_result == 1 or new_result == models.swipe.SwipeResult.ACCEPTED: 
                # Successful Match Made
                return
                
            
            
            #swipe.swipe_date = data.get('swipe_date') 
        else:
            swipe = models.swipe.Swipe(
                swiper=swiper, 
                swipee=swipee, 
                swipe_result=data.get('swipe_result'), 
                swipe_date=data.get('swipe_date')
            )
        
           
       
        # Add the new swipe to the session
        db.session.add(swipe)
        # Commit the changes to the database
        db.session.commit()
        
        # Log the success and return the message
        #logging.info(f"Swipe created successfully! - {swipe}")
        return "Swipe created successfully!", 201
    
    except SQLAlchemyError as e:
        
        # Rollback the session in case of an error, and return the error
        db.session.rollback()
        return jsonify({"error": "Database error occurred.", "details": str(e)}), 500
    
    except Exception as e:
        
        # Unexpected error, return Details back
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500
    
    
    
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