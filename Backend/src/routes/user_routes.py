
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import logging

from Backend.src.extensions import db # Import the DB Instance
import Backend.src.models as models # Import the Models and Schemas


user_bp = Blueprint('user_bp', __name__)

# -----User Routes-----

# Deserialize the JSON Data and Validate using Schema
user_schema = models.user.UserSchema()

# Create a new user in RDS
# POST /users/
# Admin Protected Route


# Get user by Email from DB
# GET /Users
# TODO: Test this Route
@user_bp.route('/users/', methods=['GET'])
@jwt_required()
def get_user():
    """
    Summary: Get a user_id by JWT Token. Return the user object.
    
    Parameters:
        X-Authorization: Bearer <JWT Token>
        
    Returns:
        JSON: The user object.
        
    """
    
    user_id = get_jwt_identity()
    
    user = models.user.User.query.get(user_id)
    
    # If the user is not found, return a 404
    if user is None:
        return jsonify({"error": "User not found."}), 404
    
    return jsonify(user_schema.dump(user)), 200

# Init User with Profile Creation Data
@user_bp.route('/users/init', methods=['POST'])
@jwt_required()
def init_profile():
    """
    Summary: Initialize a User Profile with Profile Creation Data.
    
    Parameters:
        Authorization
    
    Payload: JSON object with a User object, excluding the Email, ID, is_admin, is_fake.:
        
    """
    auth_user_id = get_jwt_identity()
    auth_user = models.user.User.query.get(auth_user_id)
    if auth_user is None:
        return jsonify({"error": "User not found."}), 404
    
    required_fields = ['age', 'dating_preferences', 'gender', 'location', 'profile_picture']
    
    
    # Update User Data with New User Data from Request
    auth_user.age = request.json.get('age')
    auth_user.dating_preferences = request.json.get('dating_preferences')
    auth_user.gender = request.json.get('gender')
    
    
    #auth_user.location = request.json.get('profile_picture')

@user_bp.route('/users/profile_picture', methods=['POST'])
@jwt_required()
def upload_profile_picture():
    """
    Summary: Upload a Profile Picture for a User.
    
    Header Parameters:
        X-Authorization: Bearer <JWT Token>
        
    Sent Payload:
        - profile_picture: BLOB, required
        - is_main_photo: bool, optional, default=False
    
    Return Payload:
        JSON: 
        - A message indicating the success or failure of the profile picture upload.
        - S3 Stored URL of the Profile Picture    
    """
    
    pass

def get_profile_pictures():
    """
    Summary: Get the Profile Picture for a User.
    
    Header Parameters:
        X-Authorization: Bearer
    """
    pass    


# UPDATE User by Email
# PUT /Users
# TODO: Test this Route
@user_bp.route('/users', methods=['PUT'])
@jwt_required()
def update_user():
    """
    Summary: Update a user by Email.
    
    Headers:
        Authorization: Bearer <JWT Token>
        
    Payload: JSON object with a User object, excluding the Email, ID, is_admin, is_fake.:
    
    """
    try:
        
        user_id = get_jwt_identity()
        user = models.user.User.query.get(user_id)
        
        if user is None:
            return jsonify({"error": "User not found."}), 404
        
        # Retrieve User Info from Request
        # Partially Deserialize the JSON Data and Validate using Schema
        updated_user_data = request.get_json()
        
        # Check if the User Data is None or if Invalid Fields are Present
        if updated_user_data is None:
            return jsonify({"error": "No data provided."}), 400
        
        invalid_fields = ['email', 'id', 'is_admin', 'is_fake']
        for field in invalid_fields:
            if field in updated_user_data:
                return jsonify({"error": f"Field '{field}' cannot be updated."}), 400
        
        validated_user_data = user_schema.load(updated_user_data, partial=True)
        
        # Update User Data with New User Data, Excluding the Email and ID
        # Only Updates Values Sent in payload with Validated Data (Not None)
        for field, value in validated_user_data.items():
            if field != 'email' and field != 'id' and value is not None:
                setattr(user, field, value)
            
        # Commit the changes to the database
        db.session.commit()
        
        
        # Serialize and return the updated user
        updated_user_data = user_schema.dump(user)
        
        
        return jsonify({"success": "User updated successfully.", "user": updated_user_data}), 200


    # Catch any unexpected errors
    except ValidationError as e:
        return jsonify({"error": "Validation error occurred.", "details": e.messages}), 400

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred.", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500
    

    
# DELETE User by Email
# DELETE /Users
# TODO: Test this Rout
@user_bp.route('/users', methods=['DELETE'])
@jwt_required()
def delete_user():
    """
    Summary: Delete/Ban a User, identified by JWT Token.
    
    
    Parameters:
        Authorization: Bearer <JWT Token>
        
        
    Returns:
        str: A message indicating the success or failure of the user deletion.
        Returns standard response codes (see above):
        
    """
    
    user_id = get_jwt_identity()
    user = models.user.User.query.get(user_id)
    
    # If the user is not found, return a 404
    if user is None:
        return jsonify({"error": "User not found."}), 404
    
    try:
        
        user.hard_delete_user()
        return jsonify({"success": "User deleted successfully."}), 200
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred.", "details": str(e)}), 500   
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500
    