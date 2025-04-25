# Author: Joshua Ferguson

import json
from flask import request, jsonify
from flask import Blueprint
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from flask_jwt_extended import  jwt_required, get_jwt_identity
import logging

from Backend.src.extensions import db, redis_client # Import the DB Instance
import Backend.src.models as models # Import the Models and Schemas
from Backend.src.services.auth_service import validate_user_exists
from Backend.src.services.swipe_pool_service import SwipePoolService


matchmaking_bp = Blueprint('matchmaking_bp', __name__)


@matchmaking_bp.route('/users/swipe_pool', methods=['GET'])
@jwt_required()
def get_swipe_pool():
    """
    Get potential matches for the current user.
    
    Returns:
        JSON with list: A list of potential matches for the user, including:
        - UserID: str
        - age: int
        - name: str
        - gender: str
        - state: str
        - city: str
        - bio: str
    """
    # Get current user and validate
    user_id = get_jwt_identity()
    user = models.user.User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404
    
    # Check if user has dating preferences
    preferences = models.datingPreference.DatingPreference.query.filter_by(user_id=user_id).first()
    if not preferences:
        return jsonify({"error": "Please set your dating preferences first."}), 400
    
    req_limit = request.args.get("limit", default=20,type=int)
    pool_service = SwipePoolService()

    try:
        
        # Generate swipe pool for the specific user
        users_swipe_pool = pool_service.generate_swipe_pool(user_id, req_limit)
        
        # Format profiles for response
        profiles = []
        for user in users_swipe_pool:
            profile = {
                "userID": user.get("id"),
                "age": str(user.get("age")),
                "name": user.get("name"),
                "gender": user.get("gender"),
                "state": user.get("state"),
                "city": user.get("city"),
                "bio": user.get("bio"),
            }
            profiles.append(profile)
        
        if len(profiles) == 0:
            return jsonify({"error": "No profiles found."}), 404
        
        print(f"Swipe Pool for User: {user_id}")
        print(json.dumps(profiles,indent=4))
        return jsonify(profiles), 200
             
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500
    except ValidationError as e:
        return jsonify({"error": "Validation error", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
    