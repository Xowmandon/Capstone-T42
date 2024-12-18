# Desc: Match Model for Successful Matches between Users
# Schema for Deserializing and Serializing

from datetime import datetime
from marshmallow_sqlalchemy import fields
from sqlalchemy.orm import relationship

from Backend.src.extensions import db, ma # DB and Marshmallow Instances
from Backend.src.models.user import User, UserSchema # User Model
from Backend.src.models.swipe import Swipe # Swipe Model

# Match Model for Matches Table
class Match(db.Model):
    __tablename__ = 'matches' # Define the table name
    
    id = db.Column(db.Integer, primary_key=True) # Primary Key
    
    # Foreign Keys - User ID's in the Successful Match
    # On Delete of User - Cascade to Remove Associated Matches
    matcher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    matchee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    

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
    
    # ---Dimensional Fields---
    match_date = db.Column(db.DateTime, nullable=False, default = datetime.now)
    
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

    