
from datetime import datetime, timezone
from marshmallow_sqlalchemy import fields
from sqlalchemy.orm import relationship, deferred
import enum
from sqlalchemy import  CheckConstraint
# Desc: Swipe Model for Swipes Table
# Schema for Deserializing and Serializing

from  Backend.src.extensions import db, ma # DB and Marshmallow Instances
from  Backend.src.models.user import User, UserSchema # User Model

# Swipe Model for Swipes Table
# TODO: Implement CASCADE on User Deletion
class Swipe(db.Model):
    __tablename__ = 'swipes'
    
    # Foreign Keys - User ID's of Swiper and Swipee
    # On Delete of User - Cascade to Remove Associated Swipes
    swiper_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    swipee_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    
    swipe_result = db.Column(db.String, nullable=False, default='PENDING')
    
    # ---Dimensional Fields---
    swipe_date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    
    __table_args__ = (
        CheckConstraint(swipe_result.in_(['PENDING', 'ACCEPTED', 'REJECTED']), name='swipe_result_check'),
    )
    # ------Relationships------
    
    # Many to One Relationship - Multiples Swipes to One User
    """
    swiper = relationship(
        "User", 
        foreign_keys=[swiper_id],
        back_populates="swipes_as_swiper"
    )
    
    swipee = relationship(
        "User", 
        foreign_keys=[swipee_id],
        back_populates="swipes_as_swipee"
    )
    
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
 