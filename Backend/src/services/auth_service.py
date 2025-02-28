# Author: Joshua Ferguson

import uuid
import jwt
import json
import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from flask_bcrypt import Bcrypt
from datetime import datetime


from Backend.src.extensions import db, bcrypt # Import the DB Instance
import Backend.src.models as models # Import the Models and Schemas
from Backend.src.utils import EnvManager
# Apple API Keys
APPLE_KEYS_URL = "https://appleid.apple.com/auth/keys"

# TODO: Move Signup & Login Handlers from auth_routes.py to Auth Classes in Services

# Apple Authentication Service
class AppleAuthService:
    """Handles Apple Sign-In authentication."""

    def get_apple_public_keys(self):
        """Retrieve Apple’s public keys."""
        response = requests.get(APPLE_KEYS_URL)
        return response.json() if response.status_code == 200 else None

    def verify_apple_identity_token(self, identity_token):
        """Verify Apple identity token and return user data."""
        apple_keys = self.get_apple_public_keys()
        if not apple_keys:
            return None

        header = jwt.get_unverified_header(identity_token)
        key = next((k for k in apple_keys["keys"] if k["kid"] == header["kid"]), None)
        if not key:
            return None

        try:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
            audience_link = EnvManager().load_env_var("APPLE_AUDIENCE")
            return jwt.decode(identity_token, public_key, algorithms=["RS256"], audience=audience_link)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

    def authenticate(self, identity_token):
        """Authenticate using Apple identity token."""
        user_data = self.verify_apple_identity_token(identity_token)
        if not user_data:
            return None, None

        return user_data["sub"], user_data.get("email")

# Email Authentication Service
class EmailAuthService:
    """Handles email/password authentication."""

    def authenticate(self, email, password):
        """Authenticate user using email and password."""
        if not email or not password:
            return None

        user = models.User.query.filter_by(email=email, auth_provider="email").first()
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return None

        return user.id

