import logging

from flask import request, jsonify, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from flask_jwt_extended import get_jwt_identity, jwt_required


from  Backend.src.extensions import db # Import the DB Instance
import  Backend.src.models as models # Import the Models and Schemas
from Backend.src.routes.match_routes import match_response_helper

# Blueprint for the Match Routes
polling_bp = Blueprint('polling_bp', __name__)

def poll_matches_helper():
    pass

def poll_messages_helper():
    pass


@polling_bp.route('/poll/matches', methods=['GET'])
@jwt_required()
def poll_matches():
    # Get the User ID from JWT
    user_id = get_jwt_identity()
    user = models.user.User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404
    try:
        
        helper = models.user.UserModelHelper(user_id)
        new_matches = helper.get_new_matches()
        
        if not new_matches:
            return jsonify({"NONE": "No new matches found."}), 404
        
        response = match_response_helper(new_matches)     
        # Return the Response
        return jsonify({"NEW",response}), 200
    
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred."}), 500
    except ValidationError as e:
        return jsonify({"error": "Validation error occurred."}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500
        
@polling_bp.route('/poll/messages', methods=['GET'])
@jwt_required()
def poll_messages():
    user_id = get_jwt_identity()
    user = models.user.User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404

    # Get the optional match_id from the query parameters
    match_id = request.args.get('match_id', None)
    
    try:
        helper = models.match.MatchModelHelper()
        
        if match_id:
            # If match_id is provided, filter messages for that match
            new_messages = helper.get_new_messages(user, match_id=match_id)
        else:
            # Otherwise, get all new messages
            new_messages = helper.get_new_messages(user)
        
        if not new_messages:
            return jsonify({"NONE": "No new messages found."}), 404
        
        response = models.message.MessageSchema(many=True).dump(new_messages)
        # Return the Response
        return jsonify({"NEW": response}), 200
    
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred."}), 500
    except ValidationError as e:
        return jsonify({"error": "Validation error occurred."}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500
