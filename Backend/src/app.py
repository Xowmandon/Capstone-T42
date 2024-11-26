from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text, URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import OperationalError, TimeoutError

# Import APP Config Settings and DB Connection Points
# Refer to the config.py file for the Config Class
from config import Config, ConfigTestLocal

# Import the Class models for the Database Schema
# Refer to the models.py file for the Class Definitions
from models import db, User, Match, Message, Swipe, Report

# Import Preprocessed Routes for the API (Before Request, After Request, etc.)
from middleware import before_request

# Import the API Blueprint for the Routes
# Refer to the routes.py file for the API Blueprint
from routes import app as routes_api

# Create a Flask app
app = Flask(__name__)

# Load the Configurations from the Config Class
app.config.from_object(ConfigTestLocal)

# Initialize the Database with the App
#db.init_app(app)

# Create all Tables in RDS - Put this in a separate Utils Py Script
#with app.app_context():
#    db.create_all()

# Register the API Blueprint with the App
app.before_request(before_request)
app.register_blueprint(routes_api)

# Main Entry Point for the API Application
if __name__ == '__main__':
    
    
    # TODO - Test the Flask App on EC2 Instance
    app.run(host='0.0.0.0', port=5000)
