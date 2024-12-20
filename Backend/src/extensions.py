from flask import app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO


db = SQLAlchemy()
ma = Marshmallow(app)


# Initialize SocketIO TODO
#socketio = SocketIO(app, cors_allowed_origins="*")

URL = "https://cowbird-expert-exactly.ngrok-free.app"


# TODO - TODO: Consider Using FlaskMarshmallow for Serialization/Deserialization
# - Can also Include Validation and Error Handling Easier than Manual Methods like to_dict

#----If Flask-Marshmallow is  Not Used, Add the Following Code----
# TODO: ADD def to_dict for Each Model to Serialize to JSON
# TODO: ADD def from_dict for Each Model to Deserialize from JSON

# TODO: ADD def to_csv for Each Model to Serialize to CSV
# TODO: ADD def from_csv for Each Model to Deserialize from CSV

#------------------------------------------------------------
