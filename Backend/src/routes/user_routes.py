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
from Backend.src.models.user import UserSchema, UserProfileSchema

user_bp = Blueprint('user_bp', __name__)

# -----User Routes-----

# Deserialize the JSON Data and Validate using Schema
user_schema = models.user.UserSchema()


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
        X-Authorization: Bearer <JWT-Token>
    
    Payload: JSON object with a User Profile object:
        - age: int, required
        - name: str, required
        - gender: str, required
        - state_code: str, required
        - city: str, required
        - bio: str, required
    """
    # Retrieve User Info from Request
    auth_user_id = get_jwt_identity()
    auth_user = models.user.User.query.get(auth_user_id)
    if auth_user is None:
        return jsonify({"error": "User not found."}), 404

    try:
        # Load and validate the profile data
        profile_schema = UserProfileSchema()
        profile_data = profile_schema.load(request.json)
        
        # Update user profile
        auth_user.age = profile_data['age']
        auth_user.name = profile_data['name']
        auth_user.gender = profile_data['gender'].lower()
        auth_user.state_code = profile_data['state_code'].lower()
        auth_user.city = profile_data['city'].lower()
        auth_user.bio = profile_data['bio']
        
        # Commit the changes to the database
        db.session.commit()
        db.session.close()
        
    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.messages}), 400
    except db.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database Error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Invalid Data Provided", "details": str(e)}), 400
    
    return jsonify({"success": "User Profile Initialized."}), 201

@user_bp.route('/users/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Summary: Get the Basic Profile of a User (For Displaying on the Frontend).
    
    Header Parameters:
        X-Authorization: Bearer <JWT-Token>
        
    Return Payload: 
    JSON object of Basic User Profile Information:
        - age: int
        - name: str
        - gender: str
        - state_code: str
        - city: str
        - bio: str
    """
    user_id = get_jwt_identity()
    if user_id is None:
        return jsonify({"error": "Invalid JWT Token."}), 400
    user = models.user.User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found."}), 404

    # Check if the User has a Profile
    if user.age is None or user.name is None or user.gender is None:
        return jsonify({"error": "User Profile Not Initialized."}), 400

    # Use the profile schema to serialize the data
    profile_schema = UserProfileSchema()
    return jsonify(profile_schema.dump(user)), 200

@user_bp.route('/users/profile', methods=['PATCH'])
@jwt_required()
def update_profile():
    """
    Update a User Profile with only the fields provided in the JSON payload.
    
    Header Parameters:
        X-Authorization: Bearer <JWT-Token>
        
    Payload: JSON object with any of the following fields:
        - age: int
        - name: str
        - gender: str
        - state_code: str
        - city: str
        - bio: str
    """
    auth_user_id = get_jwt_identity()
    auth_user = models.user.User.query.get(auth_user_id)
    if auth_user is None:
        return jsonify({"error": "User not found."}), 404


    data = request.json or {}
    if not data:
        return jsonify({"error": "No data provided."}), 400

    try:
        # Load and validate the profile data (partial=True allows updating only some fields)
        profile_schema = UserProfileSchema(partial=True)
        profile_data = profile_schema.load(request.json)
        
        # Update only the provided fields, Ensure Proper Fields are Lowercase
        for field, value in profile_data.items():
            if field in ['gender', 'city', 'state_code']:
                setattr(auth_user, field, value.lower())
            else:
                setattr(auth_user, field, value)
            
        # Commit the changes to the database
        db.session.commit()
        db.session.close()
        
    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.messages}), 400
    except db.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database Error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Invalid Data Provided", "details": str(e)}), 400
    
    return jsonify({"success": "User Profile Updated."}), 200

@user_bp.route('/users/profile_picture', methods=['POST'])
@jwt_required()
def upload_profile_picture():
    """
    Summary: Upload a Profile Picture for a User.
    
    Header Parameters:
        X-Authorization: Bearer <JWT Token>
        
    Send Payload:
        - profile_picture: request.files, required
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
    #if 'profile_picture' not in request.files:
        #return jsonify({"error": "No Profile Picture Provided."}), 400
    
    profile_picture = request.files['profile_picture']
 
    if profile_picture.filename == '':
        return jsonify({"error": "Invalid file name."}), 400

   
    # Check if is_main_photo was sent, default to False
    is_main_photo = request.form.get('is_main_photo',type=bool,default= False)
    
    # Retrieve the Profile Picture from the Request, Convert to BLOB
    #profile_picture = request.files.get('profile_picture',type=bytes)
    #if profile_picture is None:
        #return jsonify({"error": "No Profile Picture Provided."}), 400

    if is_main_photo:
        folder = AWS_MEDIA_MAIN_PHOTO_FOLDER
    else:
        folder = AWS_MEDIA_USER_PHOTO_FOLDER
        
    pic_saved_path = "./Data/" + profile_picture.filename
    profile_picture.save(pic_saved_path)
    # Upload the Profile Picture to S3 with Media Storage Service
    url = media_storage_service.upload_user_photo(
        file=pic_saved_path,
        file_name=profile_picture.filename,
        user_id=user_id,
        folder=folder,
        is_main_photo=is_main_photo
    )
    
    profile_picture.close()
    if url is None:
        # Return Form 
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
            models.photo.UserPhoto) \
        .filter_by(user_id=user_id, is_main_photo=True) \
        .first()
        
        # Additional Profile Pictures
        additional_photos = db.session.query( 
            models.photo.UserPhoto) \
        .filter_by(user_id=user_id, is_main_photo=False) \
        .all()

    except db.exc.SQLAlchemyError as e: # Database Errors
        db.session.rollback()
        return jsonify({f"error": "Database Error - {e}"}), 500
    
    # Success Response
    return jsonify({
        "main_photo": main_photo.url if main_photo else None,
        # Convert additional_photos to a list of URLs
        "user_photos": [photo.url for photo in additional_photos] if additional_photos else None,
    }), 200


@user_bp.route('/users/profile_picture', methods=['DELETE'])
@jwt_required()
def delete_user_photo():
    """
    Summary: Delete a User Photo.
    
    Header Parameters:
        X-Authorization: Bearer <JWT Token>
        
    Payload:
        - s3_photo_url: str, required
        
    Returns:
        - "success": Photo deleted successfully
        - "error": Error message
    """
    
    user_id = get_jwt_identity()
    if user_id is None:
        return jsonify({"error": "Invalid JWT Token."}), 400
    user = db.session.query(models.user.User).get(user_id)
    if user is None:
        return jsonify({"error": "User not found."}), 404
    
    photo_id = request.json.get('s3_photo_id')
    if photo_id is None:
        return jsonify({"error": "No Photo ID Provided."}), 400
    
    photo = db.session.query(models.userPhoto.UserPhoto).get(photo_id)
    if photo is None:
        return jsonify({"error": "Photo not found."}), 404
    
    try:
        # Delete the Photo from S3 and DB
        media_storage_service.delete_file(photo.url, user_id)

        return jsonify({"success": "Photo deleted successfully."}), 200
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred.", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500
    
    
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
        
        user.deleted = True
        db.session.commit()
        return jsonify({"success": "User deleted successfully."}), 200
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred.", "details": str(e)}), 500   
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500
    