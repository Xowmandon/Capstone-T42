"""
Author: Joshua Ferguson

Flask Extensions Module
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
import redis
from flask import app
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from Backend.src.utils import EnvManager

# Load Environment Variables
EnvMan = EnvManager()

AWS_REGION = EnvMan.load_env_var("AWS_REGION")
AWS_MEDIA_BUCKET_NAME = EnvMan.load_env_var("AWS_MEDIA_BUCKET_NAME")
AWS_MEDIA_BUCKET_FOLDERS = EnvMan.load_env_var("AWS_MEDIA_BUCKET_FOLDERS")
AWS_MEDIA_MAIN_PHOTO_FOLDER = EnvMan.load_env_var("AWS_MEDIA_MAIN_PHOTO_FOLDER")
AWS_MEDIA_USER_PHOTO_FOLDER = EnvMan.load_env_var("AWS_MEDIA_USER_PHOTO_FOLDER")

# ------Flask Extensions (Init with/without App Instance)-----

db = SQLAlchemy()  # Postgres Client
ma = Marshmallow(app)  # JSON Serialization/Deserilization of Models
flask_jwt = JWTManager()  # JwtManager for Protected Resources
bcrypt = Bcrypt()  # Generating Password Hashes

# -----External Services-----

# Redis for Swipe Pool and Caching Frequently Reads
redis_client = redis.Redis(
    host="localhost", port=6379, decode_responses=True  # TODO use environment variables
)


## S3 Client for Media Storage
# Import the MediaStorageService Class - Imported Here to Avoid Circular Imports
from Backend.src.services.media_storage_services import (
    MediaStorageService,
)  # noqa: E402; noqa: E402

s3_client = boto3.client("s3", region_name=AWS_REGION)
media_storage_service = MediaStorageService(
    s3_client, AWS_MEDIA_BUCKET_NAME, AWS_REGION, AWS_MEDIA_BUCKET_FOLDERS
)

from Backend.src.services.messaging_service import GCPService  # noqa: E402

# Instantiate GCPManager and initialize the Firebase app
firebase_app = GCPService().get_app()


# OpenAI Service


from Backend.src.services.llm_service import LLMService  # noqa: E402

llm_service = LLMService()
