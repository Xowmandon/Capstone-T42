"""

Flask Extensions Module
Author: Joshua Ferguson


This module initializes and provides extensions for the Flask application.

Extensions:
- db: SQLAlchemy instance for database management.
- ma: Marshmallow instance for object serialization/deserialization.
- flask_jwt: JWTManager for handling JSON Web Tokens.
- bcrypt: Bcrypt instance for password hashing.
- redis_client: Redis client for caching and data storage.
- s3: Boto3 S3 resource for interacting with Amazon S3.

"""

import boto3
from flask import app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import redis


from Backend.src.utils import EnvManager

# Load Environment Variables
EnvMan = EnvManager()

AWS_REGION = EnvMan.load_env_var("AWS_REGION")
AWS_MEDIA_BUCKET_NAME = EnvMan.load_env_var("AWS_MEDIA_BUCKET_NAME")
AWS_MEDIA_BUCKET_FOLDERS = EnvMan.load_env_var("AWS_MEDIA_BUCKET_FOLDERS")
AWS_MEDIA_MAIN_PHOTO_FOLDER = EnvMan.load_env_var("AWS_MEDIA_MAIN_PHOTO_FOLDER")
AWS_MEDIA_USER_PHOTO_FOLDER = EnvMan.load_env_var("AWS_MEDIA_USER_PHOTO_FOLDER")

# ------Flask Extensions (Init with/without App Instance)-----

db = SQLAlchemy() # Postgres Client
ma = Marshmallow(app) # JSON Serialization/Deserilization of Models
flask_jwt = JWTManager() # JwtManager for Protected Resources
bcrypt = Bcrypt() # Generating Password Hashes


# -----External Services-----

# Redis for Swipe Pool and Caching Frequently Reads
redis_client = redis.Redis(
    host='localhost',  # TODO use environment variables
    port=6379,
    decode_responses=True
)

s3_client = boto3.client('s3', region_name=AWS_REGION)
# Initilize S3  as MediaStorageService

from Backend.src.services.media_storage_services import MediaStorageService
media_storage_service = MediaStorageService(
    s3_client,
    AWS_MEDIA_BUCKET_NAME, 
    AWS_REGION, 
    AWS_MEDIA_BUCKET_FOLDERS
    )