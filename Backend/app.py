import logging

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text, URL
from sqlalchemy.exc import SQLAlchemyError, OperationalError, TimeoutError

from src.utils import EnvManager, DevDBConfig, TestDBConfig
from src.models import *
from src.middleware import before_request
from src.routes import app as routes_api

# Initialize the Logger for Flask App
#logger = logging.getLogger(__name__)

# Init Flask App
app = Flask("UnHinged-API")

# Load the DB Configurations, (Host, Port, Database Name), etc
app.config.from_object(TestDBConfig)

# Initialize the DB with Flask
db.init_app(app)

# Initialize the Marshmallow Schema with Flask
# Must be initialized after the DB


# Register the API and Routing Blueprint with the App
app.before_request(before_request)
app.register_blueprint(routes_api)

def main():
    # TODO - Test the Flask App on EC2 Instance
    
    # Set up Logging
    logging.basicConfig(filename='../logs/app.log', level=logging.INFO)
    
    #logger.info('Started')
    
    # Run the Flask App on Port 5000
    app.run(host='0.0.0.0', port=3000)
    
    #logger.info('Finished')

# Main Entry Point for the API Application
if __name__ == '__main__':
    main()
