# Author: Joshua Ferguson

from flask import request, jsonify, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from flask_jwt_extended import  get_jwt_identity, jwt_required
import logging

from Backend.src.extensions import db # Import the DB Instance
import Backend.src.models as models
from Backend.src.models.model_helpers import UserModelHelper, MatchModelHelper


# Blueprint for the Match Routes
match_bp = Blueprint('match_bp', __name__)

match_schema = models.match.MatchSchema()

#-----Match Routes-----
def match_response_helper(matches):
    """
    Helper function to create a response for a match.
    """
    matches_response = []
    for user_match in matches:
            
        # Get the Last Message in the Match
        last_message = user_match.get_last_message()
        
        # Get the Matched User Id
        matched_user_id = user_match.matchee_id if user_match.matcher_id == user_match.id else user_match.matcher_id
        
        # Get the Matched User Object
        matched_user = models.user.User.query.get(matched_user_id)
        
        # TODO Get the Unread Count for the Match
        
        # Serialize the Match Data and Add to the Response
        match_data = {
            "match_id": user_match.id,
            "matched_user_id": matched_user_id,
            "matched_user_name": matched_user.name,
            "match_date": user_match.match_date.isoformat(),
            "last_message": last_message.message_content,
            #"unread_count": 0
        }
        
        matches_response.append(match_data)
        
    return matches_response

# Get all matches for a user
@match_bp.route('/users/matches', methods=['GET'])
@jwt_required()
def get_matches():
    """
    Summary: Get all matches for a user.
    
    Returns:
        JSON with list: A list of matches for the user, including:
        - match_id: str
        - matched_user_id: str
        - matched_user_name: str
        - match_date: str
        - last_message: str 
        - unread_count: int 
    """
    # Get current user and validate
    user_id = get_jwt_identity()
    user = models.user.User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404
    
    try:
        # Get the Last Message in the Match
        matches = UserModelHelper(user_id).get_user_matches()
            
        if not matches:
            return jsonify({"error": "No matches found."}), 404
        
        # Create the response
        matches_response = match_response_helper(matches)
        # Return the response
        
        # Return the response
        return jsonify(matches_response), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


# Create a new match event of a User
# POST /users/matches
@match_bp.route('/users/matches', methods=['GET'])
def post_match():
    """
    Summary: Create a new match event and add it to the database.
    
    Payload: JSON object with the following fields:
        - matcher: int, required
        - matchee: int, required
        
    Returns:
    
        str: Success or Failure of the match creation.
        
            201 Created for successful creation.
            400 Bad Request for invalid input.
            500 Internal Server Error for unexpected issues.

    """
    
    try:
        
        # Get the data from the request body
        data = request.get_json()
        
        # Validate the input
        match = match_schema.load(data)
        # Create a new match object
        
        # Add the new match to the session
        db.session.add(match)
        # Commit the changes to the database
        db.session.commit()
        
        return "Match created successfully!", 201
    
    except SQLAlchemyError as e:
        
        # Rollback the session in case of an error, and return the error
        db.session.rollback()
        return jsonify({"error": "Database error occurred.", "details": str(e)}), 500
    
    except Exception as e:
        
        # Unexpected error, return Details back
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500

# TODO - Implement Update Match Functionality - Not Required for MVP
#@app.route('users/matches',methods=["UPDATE"])
#def update_match():
    
@match_bp.route('/users/matches',methods=["DELETE"])
def delete_match():
    """
    Summary: Delete a match event by ID.
    
    Parameters:
       matcher email (string): The Email of the user.
       matchee email (string): The Email of the user.
        
    Returns:
        str: Success or Failure of the match deletion.

    """
    
    try:
        
        # Get the ID from the request
        data = request.get_json()
        matcher = data.get('matcher')
        matchee = data.get('matchee')
        
        # Get the match from the database - According to Matcher and Matchee
        match = models.match.Match.query.filter_by(matcher=matcher, matchee=matchee).first()
        
        # If the match is not found, return a 404
        if not match:
            return jsonify({"error": "Match not found."}), 404
        
        # Delete the match from the database
        db.session.delete(match)
        db.session.commit()
        
        
        # Emit Successfull Match to Client
        #room_name = get_private_chat_room(matcher, matchee)
        
         # Emit the new message to the private chat room
        #socketio.emit('deleted_match')
        
        
        return "Match deleted successfully!", 200
    
    except SQLAlchemyError as e:
        
        # Rollback the session in case of an error, and return the error
        db.session.rollback()
        return jsonify({"error": "Database error occurred.", "details": str(e)}), 500
    
    except Exception as e:
        
        # Unexpected error, return Details back
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500
    