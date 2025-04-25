# Author: Joshua Ferguson

# Routes for Message Resource

from datetime import datetime, timezone
import logging

from flask import request, jsonify, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, and_, asc
from marshmallow import ValidationError

from Backend.src.extensions import db # socketio # Import the DB Instance
from Backend.src.models.model_helpers import MatchModelHelper
import Backend.src.models as models# Import the Models and Schemas
from Backend.src.models import message
from flask_jwt_extended import jwt_required, get_jwt_identity
from Backend.src.services.messaging_service import send_fcm_notification


#from Backend.src.sockets import get_private_chat_room

# Blueprint for the Message Routes
message_bp = Blueprint('message_bp', __name__)

message_bp_schema = models.message.MessageSchema()

# Schemas for Message Resource
#message_schema = models.message.MessageSchema(only = ('messager', 'message_content', 'message_date'))


def save_message(message_dict):
    
    try:
        
         # Validate Match Exists
        match = models.match.Match.query.get(message_dict["match_id"])
        # Check if Match Exists
        if not match:
            raise ValidationError("Match not found in database.")

        user = models.user.User.query.get(message_dict["messager_id"])
        # Check if User Exists
        user_in_match = (user.id == match.matcher_id or user.id == match.matchee_id)
        if not user or not user_in_match:
            raise ValidationError("User not found in Match.")
        
        # Extract the values from the data
        #message = message_bp_schema.load(message_dict)
        timeDate = datetime.now(timezone.utc)
        print(f"----Time Date----: {timeDate}")
        
        message = models.message.Message(
            messager_id=message_dict["messager_id"],
            match_id=message_dict["match_id"],
            message_content=message_dict["message_content"],
            kind=message_dict.get("kind"),  # Default to 'text' if not provided
            message_date = timeDate  # Set to None for now, will be set later
        )
        # Set the message date to the current time
        
        # Add the new message to the session
        db.session.add(message)
        # Commit the changes to the database
        db.session.commit()
    
    except SQLAlchemyError as e:
        raise SQLAlchemyError(f"Database error occurred: {str(e)}")
    except ValidationError as e:
        raise ValidationError(f"Validation error occurred: {str(e)}")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")

@message_bp.route('/users/messages', methods=['POST'])
@jwt_required()
def post_message():
    """ 
    Summary: Create a new message and add it to the database.
    
    Parameters:
        JSON PAYLOAD object with the following fields:
            - match_id str, required
            - message_content: str, required
            - kind: str, optional (Default 'text' for now)
            
    Request Headers:
        X-Authorization: JWT Token for the requesting user (Needs to Be Apart of the Match)

    Returns:
        JSON response with the status of the message creation.

    """
    try:
    
        messager_id = get_jwt_identity()
        data = request.get_json()
        print(f"Data: {data}")
        print(f"Messager ID: {messager_id}")
        
        
        req_params = {
            "messager_id": messager_id,
            "match_id": int(data.get('match_id')),
            "message_content": data.get('message_content') # Default type for now
        }
        
        kind = data.get('kind')
        if kind not in ['text', 'game']:
            return jsonify({"error": "Invalid message type."}), 400
        
        elif kind is not None:
            req_params["kind"] = kind
    
        try:
            print(f"Request Params: {req_params}")
            # Save the message to the database
            save_message(req_params)
        except Exception as e:
            return jsonify({"error": "Failed to save message.", "details": str(e)}), 500
        
        
        # Get Recipient ID
       # match = models.match.Match.query.get(req_params["match_id"])
        #if match.matcher_id == messager_id:
        #    reciever_id = match.matchee_id
        #else:
        #    reciever_id = match.matcher_id
        
        # Send FCM Notification to the recipient
        #send_fcm_notification(
        #        user_id=reciever_id,
        #        title="New Message Received!",
        #        body=req_params["message_content"],
        #        data_payload={
        #            "match_id": req_params["match_id"],
        #            "messager_id": messager_id,
        #            "message_content": req_params["message_content"]
        #        }
        #    )

        # Success Response
        return jsonify({"status":"SUCCESS"}), 201

    # Handle Validation and Database Errors
    except ValidationError as e:
        return jsonify({"error": "Validation error occurred.", "details": str(e)}), 400
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred.", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred.", "details": str(e)}), 400


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
    limit = request.args.get("limit", type=int, default=20)
    get_all = request.args.get("all_messages", type=lambda x: x.lower() == "true", default=False)
    print(f"Get All Messages: {get_all}")
    
    
    # Get Match from Database
    match = models.match.Match.query.get(match_id)

    # Check if Match Exists
    if not match:
        return jsonify({"error": "Match not found in database."}), 404
    
    # Make sure the  Requesting user is part of the match
    user_id = get_jwt_identity()    
    user = models.user.User.query.get(user_id)
    user_in_match = (user.id == match.matcher_id or user.id == match.matchee_id)
    if not user or not user_in_match:
        return jsonify({"error": "User not found in Match."}), 404
    
    # Get Messages
    conversation_data = MatchModelHelper(match_id=match_id).get_messages(limit, page, get_all)

    # Extract only relevant messages
    messages_list = conversation_data["messages"]
    print(f"Messages List: {messages_list}")
    print(f"Type of Messages List: {type(messages_list)}")
    # Check if Messages Exist
    if not messages_list:
        return jsonify({"error": "No messages found in conversation."}), 404
    
    
    # Log Retrieved Messages - TODO
    #for message in messages_list:
        #logging.info(f"Message: {message} -")
        
    msgs_shaped = []
    for m in messages_list:
        msgs_shaped.append({
            "kind":            m.kind,                   # always text for now
            "content":         m.message_content,        # rename field
            "sentFromClient":  (m.messager_id == user_id)  # Bool
        })
            
    # Construct the Response, Base Message Return
    message_return = {
        "match_id": str(match_id),
        #"total_messages": str(conversation_data["total_messages"]),
        "messages": msgs_shaped
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
        **message_return
    }), 200
