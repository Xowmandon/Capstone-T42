# Author: Joshua Ferguson


import jwt
import json
import requests
from flask_jwt_extended import  create_access_token, create_refresh_token, decode_token, JWTManager



from Backend.src.extensions import db, bcrypt # Import the DB Instance
import Backend.src.models as models # Import the Models and Schemas
from Backend.src.utils import EnvManager
# Apple API Keys
APPLE_KEYS_URL = "https://appleid.apple.com/auth/keys"

# TODO: Move Signup & Login Handlers from auth_routes.py to Auth Classes in Services

def get_user_from_token(token):
    """
    Retrieves the user associated with the given token.
    
    Args:
        token (str): The token to decode and retrieve the user from.
    
    Returns:
        User: The user associated with the token.
        None: If the token is invalid or the user does not exist.
    """
    decoded_token = decode_token(token)
    user_id = decoded_token.get('sub')
    user = models.User.query.get(user_id)
    
    return user


def byte_to_str_decode_token(token):
    """Decode a token if it's bytes."""
    if isinstance(token, bytes):
        return token.decode("utf-8")
    return token

def gen_access_token(user_id):
    """Generate an access token for a user."""
    access_token = create_access_token(identity=str(user_id))
    return byte_to_str_decode_token(access_token)

def gen_refresh_token(user_id):
    """Generate a refresh token for a user."""
    refresh_token = create_refresh_token(identity=str(user_id))
    return byte_to_str_decode_token(refresh_token)

class AppleUser:
    """
    Represents a user authenticated with Apple Sign-In.
    """
    
    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email

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
            return None
        new_apple_user = AppleUser(user_id=user_data["sub"],email= user_data.get("email"))
        return new_apple_user

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

