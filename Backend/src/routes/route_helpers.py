# Author: Joshua Ferguson

from flask import request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity




def validate_required_params(request, required_params):
    """Validate that all required parameters are in the request."""
    for param in required_params:
        if param not in request.keys() or request[param] is None:
            return False
    return True
