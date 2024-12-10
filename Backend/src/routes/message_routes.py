from flask import request, jsonify, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import logging

from Backend.src.extensions import db # Import the DB Instance
import Backend.src.models as models # Import the Models and Schemas



# Blueprint for the Message Routes
message_bp = Blueprint('message_bp', __name__)

message_bp_schema = models.message.MessageSchema()