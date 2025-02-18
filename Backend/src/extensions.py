from flask import app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
ma = Marshmallow(app)

jwt = JWTManager()
bcrypt = Bcrypt()


# Initialize SocketIO TODO
#socketio = SocketIO(app, cors_allowed_origins="*")

URL = "https://cowbird-expert-exactly.ngrok-free.app"




#------------------------------------------------------------
