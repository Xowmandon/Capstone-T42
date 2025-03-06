# Author: Joshua Ferguson

from flask import request, jsonify, Blueprint
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
async def get_swipe_pool():
    
    # Validate Current User and Parse Optional LImit
    user_id = get_jwt_identity()
    req_limit = request.args.get("limit", 20, type=int)

    pool_service = SwipePoolService()

    # Await for Pool_Service to get the Swipe_Pool, with optional limit
    users_swipe_pool = await pool_service.get_swipe_pool(user_id=user_id,limit=req_limit)

    # Return List of Users that are Recommended to Swipe On
    return jsonify(users_swipe_pool)