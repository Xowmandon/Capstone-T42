# Author: Joshua Ferguson


from datetime import datetime, timezone
from marshmallow_sqlalchemy import fields
from sqlalchemy.orm import relationship

from Backend.src.extensions import db, ma # DB and Marshmallow Instances
from Backend.src.models.model_helpers import MatchModelHelper
from Backend.src.models.user import User, UserSchema # User Model
from Backend.src.models.swipe import Swipe # Swipe Model

# Match Model for Matches Table
class Match(db.Model):
    __tablename__ = 'matches' # Define the table name
    
    id = db.Column(db.Integer, primary_key=True) # Primary Key
    
    # Foreign Keys - User ID's in the Successful Match
    # On Delete of User - Cascade to Remove Associated Matches
    matcher_id = db.Column(db.String(64), db.ForeignKey('users.id'), nullable=False)
    matchee_id = db.Column(db.String(64), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    """"
    # Relationships for matcher and matchee
    # Backref for User to Access All Matches
    matcher = relationship(
        "User",
        foreign_keys=[matcher_id],
        back_populates="matches_as_matcher"
    )
    matchee = relationship(
        "User",  
        foreign_keys=[matchee_id], 
        backref="matches_as_matchee"
    )
    """
    
    # ---Dimensional Fields---
    match_date = db.Column(db.DateTime, nullable=False, default = datetime.now(timezone.utc))
    
    # Unique Constraint for matcher and matchee combination
    db.UniqueConstraint('matcher_id', 'matchee_id')
    
    # Dictionary Representation of Match Object
    # Returns the Matcher and Matchee Email Addresses and Match Date
    def to_dict(self):
        return {
            'matcher': User.query.get(self.matcher),
            'matchee': User.query.get(self.matchee),
            'match_date': self.match_date
        }
        
    @staticmethod
    def create_match(matcher_id, matchee_id):
        
        # Check if Match Already Exists
        match = Match.query.filter_by(matcher_id=matcher_id, matchee_id=matchee_id).first()
        if match:
            return match
        # Validate matcher and matchee
        if matcher_id == matchee_id:
            return None
        # Validate Each Id is a User
        if not User.query.get(matcher_id) or not User.query.get(matchee_id):
            return None
        
        # Create Match
        match = Match(matcher_id=matcher_id, matchee_id=matchee_id)
        db.session.add(match)
        db.session.commit()
        return match
    
    @staticmethod 
    # Get Messages between two users, with optional limit and offset
    def get_messages(self, limit=10, page=1, get_all_messages=False):
        """
        Get messages between two users in a match.
        """
        helper = MatchModelHelper(self.id)
        return helper.get_messages(limit=limit, page=page, get_all_messages=get_all_messages)
    
    
    # String representation of a User, Outputting each Field Associated
    def __repr__(self):
        return f"<Match matcher={self.matcher}, matchee={self.matchee}, match_date={self.match_date}>"
    
# Marshmallow Schema for the Match
class MatchSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Match
        load_instance = True
        include_relationships = True
        
class MatchSchemaNested(MatchSchema):
    class Meta:
        model = Match
        load_instance = True
        include_relationships = True
        
    # Nested User Schema for Matcher and Matchee
    matcher = fields.Nested(UserSchema)
    matchee = fields.Nested(UserSchema)
    
    
class MatchSchemaOnlyEmails(MatchSchema):
    class Meta:
        model = Match
        load_instance = True
        include_relationships = True

    # Nested User Schema for Matcher and Matchee
    matcher = fields.Nested(UserSchema(only=("email",)))
    matchee = fields.Nested(UserSchema(only=("email",)))

    