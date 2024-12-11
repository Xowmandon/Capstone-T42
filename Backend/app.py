import logging

from flask import Flask, jsonify,request
from flask_socketio import SocketIO, emit

from Backend.src.utils import EnvManager, DevDBConfig, TestDBConfig
from Backend.src.extensions import db, ma #socketio
#from Backend.src.middleware import before_request

# Import the Main Routes and Blueprints
from Backend.src.routes import user_routes, match_routes, swipe_routes, message_routes
from Backend.src.routes import aggregate_routes # Utils Routes

logger = logging.getLogger(__name__)

# Init Flask App
app = Flask("UnHinged-API")

# Initialize SocketIO TODO
#socketio = SocketIO(app, cors_allowed_origins="*")

# Load the DB Configurations, (Host, Port, Database Name), etc
app.config.from_object(TestDBConfig)

# Register the Main Route Blueprints
app.register_blueprint(user_routes.user_bp)
app.register_blueprint(match_routes.match_bp)
app.register_blueprint(swipe_routes.swipe_bp)
app.register_blueprint(message_routes.message_bp)

# Register the Utility Route Blueprints
app.register_blueprint(aggregate_routes.aggregate_bp)

# Initialize the DB with Flask
db.init_app(app)

# Initialize the Marshmallow Schema with Flask
# Must be initialized after the DB
ma.init_app(app)

#app.register_blueprint(routes_api)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to UnHinged API!"})

"""
@app.before_request
def before_request():
    
    #This function runs before each request.
    
    #Logging the request method, path, and body.
    #Validating Request Body and Headers.
    
    

    # Log the request method, path, and body
    # TODO: Validate Request Body and Headers
    # TODO: Implement Security Measures
    logger.info(f"Request Path: {request.path}")
    logger.info(f"Request Method: {request.method}")
    logger.info(f"Request Headers: {request.headers}")
    logger.info(f"Request Body: {request.json}")
    
    

@app.after_request
def after_request(response):
"""
    #This function runs after each request.
    
    #Logging the response status code and body.
"""
        
    # Log the response status code and body
    logger.info(f"Response Status Code: {response.status_code}")
    logger.info(f"Response Body: {response.json}")
        
    return response
"""    




# Main Entry Point for the API Application
if __name__ == '__main__':
    # TODO - Test the Flask App on EC2 Instance
    
    # Create DB Tables
    with app.app_context():
        db.create_all()
    
    # Set up Logging
    #logging.basicConfig(filename='./logs/app.log', level=logging.INFO)
    
    #logger.info('Started')
    
    # Run the Flask App with HTTP Support
    app.run(host='0.0.0.0', port=3000)
    
     # Run the Flask App with WebSocket support
   # socketio.run(app, host='0.0.0.0', port=3000)
    
    #logger.info('Finished')
