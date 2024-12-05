from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text, URL
from sqlalchemy.exc import SQLAlchemyError, OperationalError, TimeoutError

from src.utils import EnvManager, DevDBConfig, TestDBConfig
from src.models import *
from src.middleware import before_request
from src.routes import app as routes_api

# Create a Flask app
app = Flask("UnHinged-API")

# Load the DB Configurations
app.config.from_object(TestDBConfig)

# Initialize the Database with the App
db.init_app(app)

# Register the API Blueprint with the App
app.before_request(before_request)
app.register_blueprint(routes_api)

# Main Entry Point for the API Application
if __name__ == '__main__':
    # TODO - Test the Flask App on EC2 Instance
    app.run(host='0.0.0.0', port=5000)
