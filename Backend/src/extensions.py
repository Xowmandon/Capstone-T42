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

from flask import app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import redis
import boto3

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

# S3 Bucket Service for Media/Photo Storage & Retrieval
s3 = boto3.resource('s3') 

