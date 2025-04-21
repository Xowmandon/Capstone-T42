# Author: Joshua Ferguson

from datetime import datetime, timezone
from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from Backend.src.extensions import db # Import the DB Instance
import Backend.src.models as models # Import the Models and Schemas

from Backend.src.models.userFCMToken import UserFcmToken
from Backend.src.services.auth_service import EmailAuthService, AppleAuthService, gen_access_token, gen_refresh_token

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route("/verify_token", methods=["GET"])
@jwt_required()
def verify_token():
    """
    Verify JWT token and return user information.

    POST /verify_token HTTP/1.1
    Host: __BASE_URL__
    X-Authorization: Bearer <your_Refresh_jwt_token>
    Content-Type: application/json
    
    
    Return JSON:
    
    {
        "user_id": <user_id>,
        "email": "<user_email>",
        "auth_provider": "<auth_provider 
    }

    """
    current_user_id = get_jwt_identity()
    user = models.User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user_id": user.id, "email": user.email, "auth_provider": user.auth_provider}), 200

@auth_bp.route("/fcm", methods=["POST"])
@jwt_required()
def register_fcm_token():
    """Register FCM token for push notifications.
    POST /fcm HTTP/1.1
    Body Parameters:
        - fcm_token: The FCM token to register.
    Headers:
        X-Authorization: Bearer <your_jwt_token>
    Returns:
        - 200 OK: Token registered successfully.
        - 400 Bad Request: Missing fcm_token in request body.
    """
    try:

        # Get the user ID from the JWT token
        # and the fcm_token from the request body
        user_id = get_jwt_identity()
        data = request.get_json()
        fcm_token = data.get("fcm_token")

        if not fcm_token:
            return jsonify({"error": "Missing fcm_token"}), 400

        # Check if Token already exists, update it if it does
        # or create a new entry if it doesn't
        token_entry = UserFcmToken.query.filter_by(user_id=user_id).first()
        if token_entry:
            token_entry.fcm_token = fcm_token
        else:
            token_entry = UserFcmToken(user_id=user_id, fcm_token=fcm_token)
            db.session.add(token_entry)

        # Commit the changes to the database
        # This is where the token is actually saved
        db.session.commit()
        return jsonify({"status": "token registered"}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Database error.", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal error.", "details": str(e)}), 500


@auth_bp.route("/signup", methods=["POST"])
def signup():
    """Unified signup route
    
    Supports email/password and Apple Sign-In.
    
    POST /signup HTTP/1.1
    Host: __BASE_URL__
    Content-Type: application/json

    This route handles user sign up using either email/password or Apple Sign-In.
    The request should be a POST request to the '/signup' endpoint.
    The request body should be in JSON format and include the following fields:

    
    {
        "auth_method": <email/apple>, # Required
        "identity_token": "<apple_identity_token>", # Required for Apple Sign-In
        "email":, # Required  for email signup
        "password": "<your_password>" # Required for email signup
    }
    
    Returns:
        The response will be a JSON object with the following structure:
        - If the authentication method is 'email', the response will be the result of the 'handle_email_signup' function.
        - If the authentication method is 'apple', the response will be the result of the 'handle_apple_signup' function.
        - If the authentication method is invalid, the response will be a JSON object with an 'error' field and a 400 status code.
    """
    
    data = request.json
    auth_method = data.get("auth_method")
    auth_method = auth_method.lower()
    
    if auth_method == "email":
        return handle_email_signup(data.get("email"), data.get("password"))
    elif auth_method == "apple":
        return handle_apple_signup(data.get("identity_token"))
    else:
        return jsonify({"error": "Invalid authentication method"}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    """Unified login route."""
    data = request.json
    auth_method = data.get("auth_method")

    if auth_method == "email":
        return handle_email_login(data.get("email"), data.get("password"))
    elif auth_method == "apple":
        return handle_apple_login(data.get("identity_token"))
    else:
        return jsonify({"error": "Invalid authentication method"}), 400


# ** Signup Handlers **
def handle_email_signup(email, password):
    """Handles email/password signup."""
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400


    user = models.User.create_user(email=email, password=password)
    token = gen_access_token(str(user.id))
    
    return jsonify({"message": "Signup successful", "token": token}), 201

def handle_apple_signup(identity_token):
    """Handles Apple Sign-In signup."""
    if not identity_token:
        return jsonify({"error": "Apple identity token required"}), 400

    auth_service = AppleAuthService()
    apple_user = auth_service.authenticate(identity_token)
    if apple_user is None:
        return jsonify({"error": "Invalid Apple identity token"}), 401
    
    apple_sub = apple_user.user_id
    email = apple_user.email

    # Check if Apple user already exists by Apple id
    existing_user = models.User.query.filter_by(id=apple_sub).first()
    

    if existing_user:
        # User already exists and is linked to Apple sub
        existing_user.last_online = datetime.now(timezone.utc)
        db.session.commit()
        return jsonify({"message": "User already exists"}), 200

    try:
        # Create New User if one does not exists, export name, email, and apple_sub as user.id
        user = models.User.create_user(email=email, apple_sub=apple_sub)
         
        # Create Unique JWT associated/encoded to user.id
        token = gen_access_token(str(user.id))
        print(token)
            
        return jsonify({"message": "Signup successful", "token": token}), 201
    
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred.", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred,", "details": str(e)}), 500

# ** Login Handlers **
def handle_email_login(email, password):
    """Handles email/password login."""
    auth_service = EmailAuthService()
    user_id = auth_service.authenticate(email, password)

    if not user_id:
        return jsonify({"error": "Invalid email or password"}), 401

    user = models.User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    user.last_online = datetime.now(timezone.utc)
    db.session.commit()
    token = create_access_token(identity=str(user_id))
    return jsonify({"message": "Login successful", "token": token}), 200

def handle_apple_login(identity_token):
    """Handles Apple Sign-In login."""
    if not identity_token:
        return jsonify({"error": "Apple identity token required"}), 400

    auth_service = AppleAuthService()
    apple_user = auth_service.authenticate(identity_token)
    apple_sub = apple_user.user_id
    
    if not apple_sub:
        return jsonify({"error": "Invalid Apple identity token"}), 401

    user = models.User.query.filter_by(id=apple_sub, auth_provider="apple").first()
    if not user:
        return jsonify({"error": "User not found, please sign up first"}), 404
    user.last_online = datetime.now(timezone.utc)
    db.session.commit()
    #token = gen_access_token(str(user.id))    
    return jsonify({"message": "Login successful"}), 200


def handle_apple_sub_update(user_id, apple_sub):
    """Handles Apple sub update."""
    user = models.User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.id = apple_sub
    user.auth_provider = "apple"
    db.session.commit()
    
    return jsonify({"message": "Apple sub updated successfully"}), 200