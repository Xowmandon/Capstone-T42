# Author: Joshua Ferguson

from flask import request, jsonify
from flask import Blueprint
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from flask_jwt_extended import  jwt_required, get_jwt_identity
import logging

from Backend.src.extensions import db, redis_client # Import the DB Instance
import Backend.src.models as models # Import the Models and Schemas
from Backend.src.services.swipe_pool_service import SwipePoolService


matchmaking_bp = Blueprint('matchmaking_bp', __name__)


@matchmaking_bp.route('/users/swipe_pool', methods=['GET'])
@jwt_required()
def get_swipe_pool():
    
    # Validate Current User and Parse Optional LImit
    user_id = get_jwt_identity()
    req_limit = request.args.get("limit",default=20,type=int)

    pool_service = SwipePoolService()

    try:
        # Await for Pool_Service to get the Swipe_Pool, with optional limit
        users_swipe_pool =  pool_service.generate_swipe_pool(user_id, req_limit)
        print(users_swipe_pool)
        # Return Age,Name, Gender, State, City, Bio, and Profile Picture for Each User in the Swipe Pool
        
        # Retrieve Profile Information for Each User in the Swipe Pool
        user_ids = [user.get("id") for user in users_swipe_pool]
        print(user_ids) 
        profile_pictures = db.session.query(models.photo.UserPhoto).filter(models.photo.UserPhoto.user_id.in_(user_ids)).all()
        profile_picture_w_user = {pic.user_id: pic.url for pic in profile_pictures}

        profiles = []
        for user in users_swipe_pool:
            profile = {
                "userId": user.get("id"),
                "age": user.get("age"),
                "name": user.get("name"),
                "gender": user.get("gender"),
                "state": user.get("state_code"),
                "city": user.get("city"),
                "bio": user.get("bio"),
                "profilePicture": profile_picture_w_user.get(user.get("id"))
            }
            print(profile, indent=4, sort_keys=True)
            profiles.append(profile)
        
        if len(profiles) == 0:
            return jsonify({"msg": "No Profiles Found in Swipe Pool"}), 404
             
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}),
    # Return List of Users that are Recommended to Swipe On
    return jsonify(profiles), 200