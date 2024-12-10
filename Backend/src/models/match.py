# Desc: Match Model for Successful Matches between Users
# Schema for Deserializing and Serializing

from src.extensions import db, ma # DB and Marshmallow Instances
from src.models.user import User, UserSchema # User Model
from src.models.swipe import Swipe # Swipe Model

# Match Model for Matches Table
class Match(db.Model):
    __tablename__ = 'matches' # Define the table name
    
    # Foreign Keys - User ID's in the Successful Match
    matcher = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    matchee = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    
    # ---Dimensional Fields---
    match_date = db.Column(db.DateTime, nullable=False)
    
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
    
    # Nested User Schema for Matcher and Matchee
    matcher = ma.Nested(UserSchema)
    matchee = ma.Nested(UserSchema)
        