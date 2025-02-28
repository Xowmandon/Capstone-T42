from flask import request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from Backend.src.extensions import db # Import the DB Instance
import Backend.src.models as models # Import the Models and Schemas


def validate_required_params(request, required_params):
    """Validate that all required parameters are in the request."""
    for param in required_params:
        if param not in request.args:
            return False
    return True


def get_user_from_token(token):
    """Get the user object from the JWT token."""
    user_id = get_jwt_identity()    
    return models.User.query.get(user_id)
