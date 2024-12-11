# Routes for Message Resource

import logging

from flask import request, jsonify, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, and_, asc
from marshmallow import ValidationError

from Backend.src.extensions import db # socketio # Import the DB Instance
import Backend.src.models as models# Import the Models and Schemas
from Backend.src.models import message

#from Backend.src.sockets import get_private_chat_room

# Blueprint for the Message Routes
message_bp = Blueprint('message_bp', __name__)

message_bp_schema = models.message.MessageSchema()

# Schemas for Message Resource
message_schema = models.message.MessageSchema()
message_schema_filtered = models.message.MessageSchemaOnlyEmails(only = ('messager', 'messagee', 'message_content'))

@message_bp.route('/users/messages', methods=['POST'])
def post_message():
    """ 
    Summary: Create a new message and add it to the database.
    
    Parameters:
        JSON object with the following fields:
            - messager_email str, required
            - messagee_email: str, required
            - message_content: str, required
            - message_date: str, required
    """
    
    try:
        
        data = request.get_json()
        
        # Get the data from the request body
        user1_email = data.get('messager_email')
        user2_email = data.get('messagee_email')
        
        # Get the Users ID's from DB
        user1 = models.user.User.query.filter_by(email=user1_email).first()
        user2 = models.user.User.query.filter_by(email=user2_email).first()
        
        new_message = {
            "messager": user1.id,
            "messagee": user2.id,
            "message_content": data.get('message_content'),
            "message_date": data.get('message_date')
        }
        
        # Extract the values from the data
        message = message_bp_schema.load(data)
        
        # Add the new message to the session
        db.session.add(message)
        # Commit the changes to the database
        db.session.commit()
        
        #room_name = get_private_chat_room(user1.email, user2.email)
        
        """
        # Emit the new message to the private chat room
        socketio.emit('new_message', {
            "id": message.id,
            "messager_email": user1.email,
            "messagee_email": user2.email,
            "message_content": message.message_content,
            "message_date": message.message_date
        }, room=room_name)
        """
        
        return jsonify({"Success":"Message created successfully!"}), 201
    
    except ValidationError as e:
        return jsonify({"error": "Validation error occurred.", "details": str(e)}), 400
    
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred.", "details": str(e)}), 400



@message_bp.route('/users/messages/conversation', methods=['GET'])
def get_conversation():
    
    """Summary: Get all messages between two users, ordered by DateTime.
    
    Payload:
    
        ---Required---
        messager_email (string): The Email of the user sending the message.
        messagee_email (string): The Email of the user receiving the message.
        
        ---Optional---
        limit (int): The number of messages to return.
        offset (int): The number of messages to skip.

    Returns:
        List[dict]: A list of messages between two users, ordered by DateTime., 200
    """
        
    data = request.get_json()
    
    # Check if required parameters are missing
    if 'messager_email' not in data or 'messagee_email' not in data:
        return jsonify({"error": "Required parameters missing."}), 400
    
    # Get the User Emails from the Request
    user1_email = data.get('messager_email')
    user2_email = data.get('messagee_email')
    
    # Get the optional limit and offset values
    limit = data.get('limit')
    offset = data.get('offset')
    get_all_messages = data.get('get_all_messages')
    
    # Get the Users ID's from DB
    user1 = models.user.User.query.filter_by(email=user1_email).first()
    user2 = models.user.User.query.filter_by(email=user2_email).first()
    
    # Check if user1 or user2 is not found
    if not user1 or not user2:
        return jsonify({"error": "User not found in DB."}), 404
    
    # List of Messages Instances between two users, Retrieved from DB
    conversation = get_messages_between_users(user1.id, user2.id, limit, offset)
    
    # Filter the Shared Messages - Only Return User Emails and Message Content
    # According to the MessageSchemaOnlyEmails Schema and Only Filter
    normalized_conversation = [message_schema_filtered.dump(msg)for msg in conversation]
    
    for message in normalized_conversation:
        logging.info(f"Common Message: {message}")
    
    # Return the messages
    return jsonify(normalized_conversation), 200
    
    
#-------- Helper Functions --------#    
#----------------------------------#
#----------------------------------#
   
# Get Messages between two users, with optional limit and offset
def get_messages_between_users(user1_id, user2_id, limit=10, offset=0, get_all_messages=False):
    
    # SQL Filter to get Messages between two users
    # where User1 is the Messager AND User2 is the Messagee, OR Vice Versa
    conversation_filter = or_(
                and_(message.Message.messager.has(id=user1_id), message.Message.messagee.has(id=user2_id)),
                and_(message.Message.messager.has(id=user2_id), message.Message.messagee.has(id=user1_id))
            )
    
    # Query, Filter, Order and Paginate the Messages between two users
    # Order by DateTime, Oldest to Newest
    # Offset and Limit the Results (Optionally)
    conversation = (
        db.session.query(models.message.Message)
        .filter(
            conversation_filter
        )
        .order_by(models.message.Message.message_date.asc())  # Order messages by timestamp
        .offset(offset)  # Support pagination, start at offset when returning results   # Return limited results
    )
    
    # Return all messages if all_messages is True
    if not get_all_messages:
        return conversation.limit(limit)
    
    return conversation.all()

    # ----Alternative Method---
    #user1_messages = set(user1.sent_messages)
    #user2_received_messages = set(user2.received_messages)
            
    #common_messages = user1_messages.intersection(user2_received_messages)
            
    
 