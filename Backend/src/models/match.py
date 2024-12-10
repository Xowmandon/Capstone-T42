# Desc: Match Model for Successful Matches between Users
# Schema for Deserializing and Serializing

from Backend.src.extensions import db, ma # DB and Marshmallow Instances
from Backend.src.models.user import User, UserSchema # User Model
from Backend.src.models.swipe import Swipe # Swipe Model

# Match Model for Matches Table
class Match(db.Model):
    __tablename__ = 'matches' # Define the table name
    
    id = db.Column(db.Integer, primary_key=True) # Primary Key
    
    # Foreign Keys - User ID's in the Successful Match
    # On Delete of User - Cascade to Remove Associated Matches
    matcher = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    matchee = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # ---Dimensional Fields---
    match_date = db.Column(db.DateTime, nullable=False)
    
    
    # Unique Constraint for matcher and matchee combination
    db.UniqueConstraint('matcher', 'matchee')
    
    
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
    
    # Nested User Schema for Matcher and Matchee
    matcher = ma.Nested(UserSchema)
    matchee = ma.Nested(UserSchema)
        