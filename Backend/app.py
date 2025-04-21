#Author: Joshua Ferguson

from datetime import datetime, timezone
import logging

from flask import Flask, jsonify,request
from flask_socketio import SocketIO, emit
from flask_migrate import Migrate


from Backend.src.utils import EnvManager, TestingConfig
from Backend.src.extensions import db, ma, bcrypt, flask_jwt

from Backend.src.sockets.chat import ChatNamespace
from Backend.src.sockets.swiping import SwipeNamespace

# Import the Main Routes and Blueprints
from Backend.src.routes import (
    user_routes, 
    match_routes, 
    swipe_routes, 
    message_routes,
    polling_routes,
    prompt_routes,
    aggregate_routes,
    auth_routes,
    matchmaking_routes,
)


envMan = EnvManager()
PASS_SECRET_KEY = envMan.load_env_var("PASS_SECRET_KEY")

# Initialize the Logger
file_handler = logging.FileHandler("app.log")
# Extend Flask With Logging
file_handler.setLevel(logging.INFO)
# Set the log format
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)


# Load the Config for Flask App
# - DB Configurations, (Host, Port, Database Name), etc
# - JWT_HEADER_NAME, JWT_HEADER_TYPE, and JWT_SECRET_KEY
app = Flask("UnHinged-API")
app.config.from_object(TestingConfig)

# Blueprint Routes in /routes
# - Resource, Utility , Auth, Polling, etc
blueprints = [
    user_routes.user_bp,
    match_routes.match_bp,
    swipe_routes.swipe_bp,
    message_routes.message_bp,
    polling_routes.polling_bp,
    matchmaking_routes.matchmaking_bp,
    prompt_routes.prompt_bp,
    aggregate_routes.aggregate_bp,
    auth_routes.auth_bp, 
]

# Register the Blueprints
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# Initialize the DB with Flask
db.init_app(app)

# Initialize the JWT Manager with Flask
flask_jwt.init_app(app)
bcrypt.init_app(app)

# Initialize the Marshmallow Schema with Flask
# Must be initialized after the DB
ma.init_app(app)

# Alembic Migrations with Flask
# - Migrations are used to manage database schema changes
migrate = Migrate(app, db)

# Socket Io Init with App - Needs to Be Defined in App.py
socketio = SocketIO(app)

# Register the SocketIo Namespaces, After the SocketIo Init
socketio.on_namespace(ChatNamespace("/chat"))
socketio.on_namespace(ChatNamespace("/swipe"))

# Register Logger with Flask
app.logger.addHandler(file_handler)



@app.route('/')
def home():
    return jsonify({"message": "Welcome to the UnHinged API!"}), 200

@app.route('/api/info')
def info():
    return jsonify({
        "app_name": "UnHinged API",
        "version": "1.0.0",
        "description": "API for UnHinged, a dating app.",
        "author": "Joshua Ferguson",
        "libraries": "Python - Flask, SocketIO, PostgreSQL, SQLAlchemy, Marshmallow, JWT, Redis, and more."
    }), 200

@app.route('/robots.txt')
def robots():
    return jsonify({"User-agent": "*", "Disallow": "/"}), 200


@app.before_request
def before_request():
    """
    Log request details before processing the request.
    """
    # Get the current timestamp
    timestamp = datetime.now(timezone.utc).isoformat()

    # Log the request method and URL
    app.logger.info(f"Request: {request.method} {request.path}")
    app.logger.info(f"Request Headers: {request.headers}")
    
    
    # Log URL parameters (query string)
    if request.args:
        app.logger.info(f"URL Parameters: {request.args.to_dict()}")

    # Log body parameters (for POST/PUT requests)
    if request.method in ['POST', 'PUT', 'PATCH']:
        try:
            logger.info(f"Body Parameters: {request.json}")
        except Exception as e:
            logger.warning(f"Failed to parse body parameters: {e}")
          
    # Example: Add custom headers to the response
    request.start_time = datetime.now()  
@app.after_request
def after_request(response):
    """
    Log response details after processing the request.
    """

   # Log the response status, method, and url
    logger.info(f"Response: {response.status_code} for {request.method} {request.path}")

    # Log response body (if applicable)
    if response.is_json:
        app.logger.info(f"Response Body: {response.get_json()}")
        
    # Example: Log request duration
    if hasattr(request, 'start_time'):
        duration = datetime.now() - request.start_time
        logger.info(f"Request duration: {duration.total_seconds()} seconds")
    
    return response



# Main Entry Point for the API Application
if __name__ == '__main__':

    socketio.logger.info('Flask App Starting')
    # Run the Flask App with HTTP Support
    socketio.run(app, debug=True, port=3001)
    
    socketio.logger.info('Flask App Finished Running')
