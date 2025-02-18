from flask import request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from Backend.src.extensions import db # Import the DB Instance
import Backend.src.models as models # Import the Models and Schemas

from Backend.src.services.auth_service import EmailAuthService, AppleAuthService


auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route("/verify_token", methods=["POST"])
@jwt_required()
def verify_token():
    """
    Verify JWT token and return user information.

    POST /verify_token HTTP/1.1
    Host: __BASE_URL__
    Authorization: Bearer <your_jwt_token>
    Content-Type: application/json

    {
        "token": "<your_jwt_token>"
    }
    """
    current_user_id = get_jwt_identity()
    user = models.User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user_id": user.id, "email": user.email, "auth_provider": user.auth_provider}), 200

@auth_bp.route("/signup", methods=["POST"])
def signup():
    """Unified signup route
    
    Supports email/password and Apple Sign-In.
    
    POST /signup HTTP/1.1
    Host: __BASE_URL__
    Content-Type: application/json
    
    {
        "auth_method": <email/apple>, # Required
        "email": "", # Required  
        "password": "<your_password>" # Required for email signup
    }
    
    """
    
    data = request.json
    auth_method = data.get("auth_method")

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

    existing_user = models.User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already in use"}), 409

    user = models.User.create_user(email=email, password=password)
    token = create_access_token(identity=user.id)
    return jsonify({"message": "Signup successful", "token": token}), 201

def handle_apple_signup(identity_token):
    """Handles Apple Sign-In signup."""
    if not identity_token:
        return jsonify({"error": "Apple identity token required"}), 400

    auth_service = AppleAuthService()
    apple_sub, email = auth_service.authenticate(identity_token)

    if not apple_sub:
        return jsonify({"error": "Invalid Apple identity token"}), 401

    # Check if Apple user already exists
    existing_user = models.User.query.filter_by(email=email).first()
    
    # Linking Apple sub to existing user
    # Update Apple sub if user exists, else create a new user
    if existing_user:
        if existing_user.id != apple_sub:
            existing_user.id = apple_sub
            existing_user.auth_provider = "apple"
            db.session.commit()
        user = existing_user
    else:
        user = models.User.create_user(email=email, apple_sub=apple_sub)

    token = create_access_token(identity=user.id)
    return jsonify({"message": "Signup successful", "token": token}), 201



# ** Login Handlers **
def handle_email_login(email, password):
    """Handles email/password login."""
    auth_service = EmailAuthService()
    user_id = auth_service.authenticate(email, password)

    if not user_id:
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_access_token(identity=user_id)
    return jsonify({"message": "Login successful", "token": token}), 200

def handle_apple_login(identity_token):
    """Handles Apple Sign-In login."""
    if not identity_token:
        return jsonify({"error": "Apple identity token required"}), 400

    auth_service = AppleAuthService()
    apple_sub, _ = auth_service.authenticate(identity_token)

    if not apple_sub:
        return jsonify({"error": "Invalid Apple identity token"}), 401

    user = models.User.query.filter_by(id=apple_sub, auth_provider="apple").first()
    if not user:
        return jsonify({"error": "User not found, please sign up first"}), 404

    token = create_access_token(identity=user.id)
    return jsonify({"message": "Login successful", "token": token}), 200
