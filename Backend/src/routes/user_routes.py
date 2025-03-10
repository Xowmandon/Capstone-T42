# Author: Joshua Ferguson

from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import logging

from Backend.src import services
from Backend.src.extensions import db # Import the DB Instance
import Backend.src.models as models
from Backend.src.routes.route_helpers import validate_required_params # Import the Models and Schemas
from Backend.src.extensions import media_storage_service, AWS_MEDIA_MAIN_PHOTO_FOLDER, AWS_MEDIA_USER_PHOTO_FOLDER

user_bp = Blueprint('user_bp', __name__)

# -----User Routes-----

# Deserialize the JSON Data and Validate using Schema
user_schema = models.user.UserSchema()

# Create a new user in RDS
# POST /users/
# Admin Protected Route



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

@user_bp.route('/users/preferences', methods=['POST'])
@jwt_required()
def init_preferences():
    """
    Summary: Initialize a User's Dating Preferences.
    
    Auhorization:
        X-Authorization: Bearer <JWT-Token>
    
    Payload: JSON object with a Dating Preferences object:
        - minAge: int, required
        - maxAge: int, required
        - interestedIn: str (Male, Female, Any), required
    """
    print(request.json)
    required_fields = ['minAge', 'maxAge', 'interestedIn']
    if validate_required_params(request.json, required_fields) is False:
        print("Missing Required Fields.")
        return jsonify({"error": "Missing Required Fields."}), 400
    
    user_id = get_jwt_identity()
    user = models.user.User.query.get(user_id)
    
    if user is None:
        print("User not found.")
        return jsonify({"error": "User not found."}), 404
    
    # Check if the User has already set their Dating Preferences
    dating_pref_exists = db.session.query(models.datingPreference.DatingPreference).filter_by(user_id=user_id).first()
    if dating_pref_exists is not None:
        print("User Dating Preferences Already Initialized.")
        return jsonify({"msg": "User Dating Preferences Already Initialized."}), 200
    
    try:
        # Create a new Dating Preference Object, Validate and Add to the Database
        dating_pref = models.datingPreference.DatingPreference(
            user_id =user_id,
            age_preference_lower=request.json.get('minAge'),
            age_preference_upper=request.json.get('maxAge'),
            interested_in=request.json.get('interestedIn').lower()
        )
        
        # Add , Commit, and Close the Database Session
        db.session.add(dating_pref)
        db.session.commit()
        db.session.close()
    
    except SQLAlchemyError as e1:
        db.session.rollback()
        print(f"Database Error - {e1}")
        return jsonify({f"error": "Database Error - {e1}"}), 500
    
    except Exception as e:
        print(f"Invalid Data Provided - {e}")
        return jsonify({f"error": "Invalid Data Provided - {e}"}), 400
    
    # Success Response
    return jsonify({"success": "User Dating Preferences Initialized."}), 201

# Init User with Profile Creation Data
@user_bp.route('/users/profile', methods=['POST'])
@jwt_required()
def init_profile():
    """
    Summary: Initialize a User Profile with Profile Creation Data.
    
    Parameters:
        X-Authorization
    
    Payload: JSON object with a User object, excluding the Email, ID, is_admin, is_fake.:
        
    """
    # Retrieve User Info from Request
    auth_user_id = get_jwt_identity()
    auth_user = models.user.User.query.get(auth_user_id)
    if auth_user is None:
        return jsonify({"error": "User not found."}), 404
    
    required_fields = ['age', 'name', 'gender', 'state','city', 'bio']
    if validate_required_params(request.json, required_fields) is False:
        return jsonify({"error": "Missing Required Fields."}), 400

    try:
        
        auth_user.age = request.json.get('age')
        auth_user.name = request.json.get('name')
        auth_user.gender = request.json.get('gender').lower()
        auth_user.state_code = request.json.get('state')
        auth_user.city = request.json.get('city').lower()
        auth_user.bio = request.json.get('bio')
        
        # Commit the changes to the database
        db.session.commit()
        db.session.close()
        
    except db.exc.SQLAlchemyError as e1:
        db.session.rollback()
        return jsonify({f"error": "Database Error - {e1}"}), 500
    except Exception as e:
        return jsonify({f"error": "Invalid Data Provided - {e}"}), 400
    
    return jsonify({"success": "User Profile Initialized."}), 201
    
@user_bp.route('/users/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Summary: Get the Basic Profile of a User (For Displaying on the Frontend).
    
    Header Parameters:
        X-Authorization: Bearer
        
    Return Payload: 
    JSON object of Basic User Profile Information:
        - age: int
        - name: str
        - gender: str
        - state: str
        - city: str
        - bio: str
    """
    user_id = get_jwt_identity()
    if user_id is None:
        return jsonify({"error": "Invalid JWT Token."}), 400
    user = models.user.User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found."}), 404

    #Check if the User has a Profile 
    # TODO #7 - Validate Profile Data (Age, Name, gender, etc) Exists with Schema
    if user.age is None or user.name is None or user.gender is None:
        return jsonify({"error": "User Profile Not Initialized."}), 400

    # Return the User Profile Information, Age, Gender, State, City, Bio
    # TODO #6 - Implement User Schema for Profile Information (Age, Name, Gender, State, City, Bio)
    user_profile = {
        "age": user.age,
        "name": user.name,
        "gender": user.gender,
        "state": user.state_code,
        "city": user.city,
        "bio": user.bio
    }
    
    # Return Schema when Implemented from #6
    return jsonify(user_profile), 200

@user_bp.route('/users/profile', methods=['PATCH'])
@jwt_required()
def update_profile():
    """
    Update a User Profile with only the fields provided in the JSON payload.
    """
    auth_user_id = get_jwt_identity()
    auth_user = models.user.User.query.get(auth_user_id)
    if auth_user is None:
        return jsonify({"error": "User not found."}), 404

    # List of fields that can be updated
    updatable_fields = ['age', 'name', 'gender', 'state', 'city', 'bio']
    
    data = request.json or {}
    if not data:
        return jsonify({"error": "No data provided."}), 400

    # Update the User Profile with the New Data if Provided
    for field in updatable_fields:
        if field in data:
            setattr(auth_user, field, data[field])
            
    # Commit the changes to the database
    try:
        db.session.commit()
        db.session.close()
    except db.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database Error - {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Invalid Data Provided - {e}"}), 400   
    
    return jsonify({"success": "User Profile Updated."}), 200  

@user_bp.route('/users/profile_picture', methods=['POST'])
@jwt_required()
def upload_profile_picture():
    """
    Summary: Upload a Profile Picture for a User.
    
    Header Parameters:
        X-Authorization: Bearer <JWT Token>
        
    Send Payload:
        - profile_picture: BLOB, required
        - is_main_photo: bool, optional, default=False
    
    Return JSON Payload:
        - "success": Profile Picture Uploaded
        - "url": URL of the Profile Picture in S3
        
    """
    user_id = get_jwt_identity()
    if user_id is None:
        return jsonify({"error": "Invalid JWT Token."}), 400
    user = db.session.query(models.user.User).get(user_id)
    if user is None:
        return jsonify({"error": "User not found."}), 404
    
    # Check if a file is in the request
    if 'profile_picture' not in request.files:
        return jsonify({"error": "No Profile Picture Provided."}), 400
    
    file = request.files['profile_picture']

    if file.filename == '':
        return jsonify({"error": "Invalid file name."}), 400


    # Check if is_main_photo was sent, default to False
    is_main_photo = request.form.get('is_main_photo', 'false').lower() == 'true'
    
    # Retrieve the Profile Picture from the Request, Convert to BLOB
    profile_picture = request.files.get('profile_picture',type=bytes)
    if profile_picture is None:
        return jsonify({"error": "No Profile Picture Provided."}), 400
    
    # Create Folder URL for the Profile Picture
    is_main_photo = request.json.get('is_main_photo', False)
    if is_main_photo:
        folder = AWS_MEDIA_MAIN_PHOTO_FOLDER
    else:
        folder = AWS_MEDIA_USER_PHOTO_FOLDER
    
    # Upload the Profile Picture to S3 with Media Storage Service
    url = media_storage_service.upload_file(profile_picture, user_id, folder)
    if url is None:
        return jsonify({"error": "Profile Picture S3 Upload Failed."}), 500
    
    return jsonify({"success": "Profile Uploaded", "url": url}), 201
    

@user_bp.route('/users/profile_picture', methods=['GET'])
@jwt_required()
def get_profile_pictures():
    """
    Summary: Get the Profile Pictures for a User.
    
    Header Parameters:
        X-Authorization: Bearer
        
    Return Payload:
        JSON: 
        - "main_photo": Main Profile Picture
        - "user_photos": Additional Profile Pictures
    """
    user_id = get_jwt_identity()
    if user_id is None:
        return jsonify({"error": "Invalid JWT Token}"}), 400
    user = db.session.query(models.user.User).get(user_id)
    if user is None:
        return jsonify({"error": "User not found."}), 404
    
    try:
        # Main Profile Picture
        main_photo = db.session.query( 
            models.userPhoto.UserPhoto) \
        .filter_by(user_id=user_id, is_main_photo=True) \
        .first()
        
        # Additional Profile Pictures
        additional_photos = db.session.query( 
            models.userPhoto.UserPhoto) \
        .filter_by(user_id=user_id, is_main_photo=False) \
        .all()

    except db.exc.SQLAlchemyError as e: # Database Errors
        db.session.rollback()
        return jsonify({f"error": "Database Error - {e}"}), 500
    
    # Success Response
    return jsonify({
        "main_photo": main_photo,
        "user_photos": additional_photos
    }), 200

       
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
    