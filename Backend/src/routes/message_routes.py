from flask import request, jsonify, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import logging

from Backend.src.extensions import db # Import the DB Instance
import Backend.src.models as models # Import the Models and Schemas

# Blueprint for the Message Routes
message_bp = Blueprint('message_bp', __name__)

message_bp_schema = models.message.MessageSchema()


@message_bp.route('/users/messages', methods=['POST'])
def post_message():
    
    
    try:
        
        # Get the data from the request body
        data = request.get_json()
        
        # Extract the values from the data
        message = message_bp_schema.load(data)
        
        # Add the new message to the session
        db.session.add(message)
        # Commit the changes to the database
        db.session.commit()
        
        return jsonify({"Success":"Message created successfully!"}), 201
    
    except ValidationError as e:
        return jsonify({"error": "Validation error occurred.", "details": str(e)}), 400
    
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred.", "details": str(e)}), 400



@message_bp.route('/users/messages/conversation', methods=['GET'])
def get_ordered_convo():
    
    """Summary: Get all messages between two users, ordered by DateTime.
    
    Payload:
        messager_email (string): The Email of the user sending the message.
        messagee_email (string): The Email of the user receiving the message.

    Returns:
        List[dict]: A list of messages between two users, ordered by DateTime., 200
    """
        
    data = request.get_json()
        
    user1 = data.get('messager_email')
    user2 = data.get('messagee_email')
    
    # Get the messages between the two users
    messager_to_messagee = models.message.Message.query.filter_by(messager=user1, messagee=user2).all()
    messagee_to_messager = models.message.Message.query.filter_by(messager=user2, messagee=user1).all()
    
    # Return the messages as Conversation - List of Messages (Dict) Between Two Users
    conversation = [models.message.MessageSchema().dump(message) for message in messager_to_messagee]
    conversation.extend([models.message.MessageSchema().dump(message) for message in messagee_to_messager])
    
    # Remove the Messagee Item - Not Needed for Conversation, as we can infer from the sender
    conversation = [message.pop("messagee") for message in conversation]  # Remove unnecessary 'del' keyword and fix parentheses

    # Order Conversation by DateTime, Oldest to Newest
    conversation = sorted(conversation, key=lambda x: x['message_date'])

    # Return the messages - 
    return jsonify(conversation), 200
    