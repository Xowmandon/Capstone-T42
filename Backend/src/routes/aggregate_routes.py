
from flask import request, jsonify, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import logging

from Backend.src.extensions import db # Import the DB Instance
import Backend.src.models as models # Import the Models and Schemas

aggregate_bp = Blueprint('aggregate_bp', __name__)


# Get all users from DB
# GET /Users/GetAll
@aggregate_bp.route('/aggregate/users', methods=['GET'])
def get_all_users():
    """
    Summary: Get all users from the database.
    
    Returns:
        list: A list of all users in the database.
        
    """
    
    user_schema = models.user.UserSchema()
    try:
        # Get all users from the database
        users = models.user.User.query.all()
        
    except Exception as e:
            return jsonify({"error": "An error occurred"}), 500
        
    # Return the users as a list of dictionaries
    return jsonify([user_schema.dump(user) for user in users]), 200


# Get all matches from DB
# GET /aggregate/matches
@aggregate_bp.route('/aggregate/matches', methods=['GET'])
def get_all_matches():
    """
    Summary: Get all matches from the database.
    
    Returns:
        list: A list of all matches in the database.
        
    """
    
    match_schema = models.match.MatchSchema()
    try:
        # Get all matches from the database
        matches = models.match.Match.query.all()
        
    except Exception as e:
            return jsonify({"error": "An error occurred"}), 500
        
    # Return the matches as a list of dictionaries
    return jsonify([match_schema.dump(match) for match in matches]), 200



# Get all Messages for a User
@aggregate_bp.route('/aggregate/users/messages', methods=['GET'])
def get_users_agg_messages():
    
    data = request.get_json()
    user = data.get('user')
    
    # Get the messages for the user
    messages = models.message.Message.query.filter_by(sender=user).all()
    
    # Return the messages - 
    return jsonify([models.message.MessageSchema().dump(message) for message in messages]), 200 