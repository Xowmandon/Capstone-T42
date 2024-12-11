from enum import Enum
from marshmallow_sqlalchemy import fields
from sqlalchemy.orm import relationship

# Desc: Swipe Model for Swipes Table
# Schema for Deserializing and Serializing

from  Backend.src.extensions import db, ma # DB and Marshmallow Instances
from  Backend.src.models.user import User, UserSchema # User Model

# Enum for Swipe Result
class SwipeResult(Enum):
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2

# ...

# Swipe Model for Swipes Table
# TODO: Implement CASCADE on User Deletion
class Swipe(db.Model):
    __tablename__ = 'swipes'
    
    # Foreign Keys - User ID's of Swiper and Swipee
    # On Delete of User - Cascade to Remove Associated Swipes
    swiper = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    swipee = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    
    swipe_result = db.Column(db.Enum(SwipeResult), nullable=False, default=SwipeResult.PENDING)
    
    # ---Dimensional Fields---
    swipe_date = db.Column(db.DateTime, nullable=False)
    
    swiper_user = relationship("User", foreign_keys=[swiper])
    swipee_user = relationship("User", foreign_keys=[swipee])
    
    """
    def to_dict(self):
        return {
            'swiper': User.query.get(self.swiper),
            'swipee': User.query.get(self.swipee),
            'swipe_result': self.swipe_result,
            'swipe_date': self.swipe_date
        }
    
    
    def __repr__(self):
        return f"<Swipe swiper={self.swiper}, swipee={self.swipee}, swipe_result={self.swipe_result}, swipe_date={self.swipe_date}>"
    """

class SwipeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Swipe
        load_instance = True
        include_relationships = True
        
        
class SwipeSchemaNested(SwipeSchema):

    class Meta:
        model = Swipe
        load_instance = True
        include_relationships = True

    swiper = ma.Nested(UserSchema)
    swipee = ma.Nested(UserSchema)
    
class SwipeSchemaOnlyEmails(SwipeSchema):
    class Meta:
        model = Swipe
        load_instance = True
        include_relationships = True
        
    # Nested User Schema for Swiper and Swipee
    swiper = fields.Nested(UserSchema(only=("email",)))
    swipee = fields.Nested(UserSchema(only=("email",)))
    
    """Example Dictionary Representation of Swipe Object
    {
        'swiper': { 'id': self.id,
                    'name': self.name,
                    'username': self.username,
                    'email': self.email
                },
        'swipee': { 'id': self.id,
                    'name': self.name,
                    'username': self.username,
                    'email': self.email
                },
        'swipe_result': 0,
        'swipe_date': "2025-01-01
    }
    
    """