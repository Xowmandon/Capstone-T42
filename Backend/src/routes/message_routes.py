# Routes for Message Resource

import logging

from flask import request, jsonify, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, and_, asc
from marshmallow import ValidationError

from Backend.src.extensions import db # socketio # Import the DB Instance
import Backend.src.models as models# Import the Models and Schemas
from Backend.src.models import message
from flask_jwt_extended import jwt_required, get_jwt_identity
import Backend.src.routes.route_helpers as route_helpers


#from Backend.src.sockets import get_private_chat_room

# Blueprint for the Message Routes
message_bp = Blueprint('message_bp', __name__)

message_bp_schema = models.message.MessageSchema()

# Schemas for Message Resource
message_schema = models.message.MessageSchema()
message_schema_filtered = models.message.MessageSchemaOnlyEmails(only = ('messager', 'message_content'))


def save_message(message):
    
    #match_id = message.match_id
    #match = models.match.Match.query.get(match_id)
    #messager = message.messager
    #message_content = message.message_content
    #message_date = message.message_date
    
    # Extract the values from the data
    message = message_bp_schema.load(message)
    
    # Add the new message to the session
    db.session.add(message)
    # Commit the changes to the database
    db.session.commit()

    return message

@message_bp.route('/users/messages', methods=['POST'])
@jwt_required()
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
        
        messager_id = get_jwt_identity()
        
        data = request.get_json()
        
        match_id = data.get('match_id')
        message_content = data.get('message_content')
        #message_date = data.get('message_date') # TODO: Add the message date to the message schema
        
        # Validate Match Exists
        match = models.match.Match.query.get(match_id)
        if not match:
            return jsonify({"error": "Match not found in database."}), 404
        
        # Validate Users Exist
        messager = models.user.User.query.get(messager_id)
        if not messager:
            return jsonify({"error": "Messager not found in database."}), 404
        
        # Add Messager ID to the Data to be Loaded into Schema
        data['messager_id'] = messager_id
        
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
@jwt_required()
def get_conversation():
    """ 
    Summary: Get all messages between two users, ordered by DateTime.

    URL Params:
        ---Required---
        match_id (string): The ID of the match.
        

        ---Optional---
        limit (int): The number of messages to return per page.
        page (int): The page number for pagination.
        all_messages (bool): If True, returns all messages between users.

    Request Headers:
        Authorization: JWT Token for the requesting user (Needs to Be Apart of the Match)

    Returns:
        JSON response with message details and pagination metadata.
    """

    # Validate Required Parameters
    if "match_id" not in request.args:
        return jsonify({"error": "Required parameter 'match_id' not found in request."}), 400

    # Extract Parameters, with Defaults
    match_id = request.args.get("match_id", type=int)
    page = request.args.get("page", type=int, default=1)
    limit = request.args.get("limit", type=int, default=10)
    get_all = request.args.get("all_messages", type=lambda x: x.lower() == "true", default=False)

    # Get Match from Database
    match = models.match.Match.query.get(match_id)

    # Check if Match Exists
    if not match:
        return jsonify({"error": "Match not found in database."}), 404
    
    # Make sure the  Requesting user is part of the match
    user_id = get_jwt_identity()    
    user = models.user.User.query.get(user_id)
    user_in_match = (user.id == match.user1_id or user.id == match.user2_id)
    if not user or not user_in_match:
        return jsonify({"error": "User not found in Match."}), 404
    
    # Get Messages
    conversation_data = get_messages_in_match(match, limit, page, get_all)

    # Extract only relevant messages
    messages_list = [message_schema_filtered.dump(msg) for msg in conversation_data["messages"]]

    # Log Retrieved Messages - TODO
    #for message in messages_list:
        #logging.info(f"Message: {message} -")
        
    # Construct the Response, Base Message Return
    message_return = {
        "match_id": match_id,
        "messages": messages_list,
        "total_messages": conversation_data["total_messages"],
    }

    # Add Pagination Metadata if not getting all messages
    if not get_all:
        message_return["pagination"] = {
            "total_pages": conversation_data["total_pages"],
            "current_page": conversation_data["current_page"],
            "has_next": conversation_data["has_next"],
            "has_prev": conversation_data["has_prev"]
        }

        
    return jsonify({
        message_return
    }), 200

# Get Messages between two users, with optional limit and offset
def get_messages_in_match(match_id, limit=10, page=1, get_all_messages=False):
    """
    Retrieve messages exchanged between two users in a match.

    Parameters:
    - match: Match object containing user1_id and user2_id.
    - limit: Number of messages per page.
    - page: Page number for pagination.
    - get_all_messages: If True, returns all messages without pagination.

    Returns:
    - Dictionary containing messages and pagination metadata.
    """

    # Filter: Get messages where one user is the sender and the other is the recipient
    #conversation_filter = or_(
        #and_(models.message.Message.messager_id == user1_id, models.message.Message.messagee_id == user2_id),
        #and_(models.message.Message.messager_id == user2_id, models.message.Message.messagee_id == user1_id)
    #)
    
    # Get the messages marked with the match ID
    conversation_filter = models.message.Message.match_id == match_id

    # Construct the Query
    conversation_query = (
        db.session.query(models.message.Message)
        .filter(conversation_filter)
        .order_by(models.message.Message.message_date.desc())  # Order by newest first
    )
    
    conversation = conversation_query.all()

    # Fetch all messages if `get_all_messages` is True
    if get_all_messages:
        return {"messages": conversation, "total_messages": len(conversation)}

    # Paginate Results
    paginated_results = conversation_query.paginate(page=page, per_page=limit, error_out=False)

    return {
        "messages": paginated_results.items,  # List of messages on the current page
        "total_messages": paginated_results.total,  # Total messages in the conversation
        "total_pages": paginated_results.pages,  # Total number of pages
        "current_page": paginated_results.page,  # Current page number
        "has_next": paginated_results.has_next,  # Whether there is a next page
        "has_prev": paginated_results.has_prev,  # Whether there is a previous page
    }