
from datetime import datetime, timezone
from marshmallow_sqlalchemy import fields
from sqlalchemy.orm import relationship

from Backend.src.extensions import db, ma # DB and Marshmallow Instances
from Backend.src.models.model_helpers import MatchModelHelper
from Backend.src.models.user import User, UserSchema # User Model


# Prompt Model for Storing User Prompts and Answers (e.g., "What is your favorite color?")
# This model is used to store the prompts and their corresponding answers.
# The Prompt model has a one-to-many relationship with the PromptAnswer model.
# The PromptAnswer model stores the answers to the prompts, including the correct answer and decoys.

class Prompt(db.Model):
    __tablename__ = 'prompts' # Define the table name
    
    # Fields
    id = db.Column(db.Integer, primary_key=True) # Primary Key
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'), nullable=False)
    prompt_question = db.Column(db.String(256), nullable=False)
    
    # Metadata Fields
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    # Unique Constraint for user_id and prompt_question combination
    db.UniqueConstraint('user_id', 'prompt_question')
    
    # Relationships
    #user = relationship("User", back_populates="prompts")
    answers = relationship("PromptAnswer", back_populates="prompt", cascade="all, delete-orphan")
    
    # Dict Repr.
    def to_dict(self):
        return {
            'id': self.id,
            #'user_id': self.user_id,
            'prompt_question': self.prompt_question,
            'created_at': self.created_at,
            'answers': [answer.to_dict() for answer in self.answers].random.shuffle() 
        }
        
        
class PromptAnswer(db.Model):
    __tablename__ = 'prompt_answers' # Define the table name
    
    # Fields
    id = db.Column(db.Integer, primary_key=True) # Primary Key
    prompt_id = db.Column(db.Integer, db.ForeignKey('prompts.id'), nullable=False)
    answer = db.Column(db.String(256), nullable=False)
    decoy = db.Column(db.String(256), nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    db.UniqueConstraint('prompt_id', 'answer')
    
    # Relationships
    prompt = relationship("Prompt", back_populates="answers")
    
    # Dict Repr.
    def to_dict(self):
        return {
            'answer': self.answer,
            'decoy': self.decoy,
        }
        