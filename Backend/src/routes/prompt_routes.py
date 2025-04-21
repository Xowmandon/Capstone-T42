from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import logging

from Backend.src import services
from Backend.src.extensions import db # Import the DB Instance
import Backend.src.models as models


# Blueprint for the Prompt Routes
prompt_bp = Blueprint('prompt_bp', __name__)


@prompt_bp.route('/users/prompts', methods=['GET'])
@jwt_required()
def get_prompts():
    user_id = get_jwt_identity()
    user = models.user.User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404
    try:
        # Get the Prompts for the User
        prompts = models.prompt.Prompt.query.filter_by(user_id=user_id).all()
        
        if not prompts:
            return jsonify({"error": "No prompts found for user."}), 404
        
        # Convert to JSON
        prompts_json = [prompt.to_dict() for prompt in prompts]
        
        return jsonify(prompts_json), 200
    
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred."}), 500
    except ValidationError as e:
        return jsonify({"error": "Validation error occurred."}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500
    
@prompt_bp.route('/users/prompts/<int:prompt_id>', methods=['GET'])
@jwt_required()
def get_prompt(prompt_id):
    
    # Get the User ID from JWT
    # "X-Authorization" header
    user_id = get_jwt_identity()
    user = models.user.User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404
    try:
        # Get the Prompt for the User
        prompt = models.prompt.Prompt.query.filter_by(id=prompt_id, user_id=user_id).first()
        
        if not prompt:
            return jsonify({"error": "Prompt not found."}), 404
        
        # Return as JSON
        prompt_json = prompt.to_dict()
        return jsonify(prompt_json), 200
    
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred."}), 500
    except ValidationError as e:
        return jsonify({"error": "Validation error occurred."}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500

@prompt_bp.route('/users/prompts', methods=['POST'])
@jwt_required()
def post_prompt():
    # Get the User ID from JWT
    user = models.user.User.query.get(get_jwt_identity())
    if not user:
        return jsonify({"error": "User not found."}), 404
    
    
    try:
        # Get the JSON Data from the Request
        data = request.get_json()
        question = data.get('prompt_question')
        
        # Validate the Request Data
        if not data or question is None:
            return jsonify({"error": "Prompt question is required."}), 400
   
        # Create a New Prompt
        new_prompt = models.prompt.Prompt(
            user_id=user.id,
            prompt_question=question,
        )
        
        # Add to DB and Commit
        db.session.add(new_prompt)
        
        # Add Answers to the Prompt 
        answers = data.get('answers')    
        if not answers:
            # Answer is required
            db.session.rollback()
            return jsonify({"error": "At least one answer is required."}), 400
        
        for answer in answers:
            new_answer = models.prompt.PromptAnswer(
                prompt_id=new_prompt.id,
                answer=answer['answer'],
                decoy=answer['decoy'] # True by default
            )
            db.session.add(new_answer)
                  
        # Commit the Changes   
        db.session.commit()
        
        return jsonify(new_prompt.to_dict()), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred."}), 500
    except ValidationError as e:
        db.session.rollback()
        return jsonify({"error": "Validation error occurred."}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred."}), 500