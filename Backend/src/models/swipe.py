# Author: Joshua Ferguson

from datetime import datetime, timezone
from marshmallow_sqlalchemy import fields
from sqlalchemy.orm import relationship, deferred
from sqlalchemy import  CheckConstraint

from  Backend.src.extensions import db, ma # DB and Marshmallow Instances
from  Backend.src.models.user import User, UserSchema # User Model

# Swipe Model for Swipes Table
# TODO: Implement CASCADE on User Deletion
class Swipe(db.Model):
    __tablename__ = 'swipes'
    
    # Foreign Keys - User ID's of Swiper and Swipee
    # On Delete of User - Cascade to Remove Associated Swipes
    swiper_id = db.Column(db.String(64), db.ForeignKey('users.id'), primary_key=True, nullable=False)
    swipee_id = db.Column(db.String(64), db.ForeignKey('users.id'), primary_key=True, nullable=False)
    
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
 
 
class SwipeProcessor():
    
    def process_new_swipe(swiper_id, swipee_id, new_swipe_result):
        
        # Check if Swipe Exists for the two Users
        # Meaning, There is a record Where Swipee equals Current Swiper, and Vice Versa
        swiper_swipe = Swipe.query.filter_by(swiper_id=swipee_id, swipee_id=swiper_id).first()
        swipee_swipe = Swipe.query.filter_by(swiper_id=swiper_id, swipee_id=swipee_id).first()

        # Swipe Exits - Good to Compare and Check for New Match
        swipe_record = swiper_swipe if swiper_swipe else swipee_swipe

        # If swipe does not exist, create a new swipe instance
        if swipe_record is None:
            new_swipe = Swipe(swiper_id=swiper_id, swipee_id=swipee_id, swipe_result=new_swipe_result)
            db.session.add(new_swipe)
            db.session.commit()
            print(f"New swipe created - Swiper: {new_swipe.swiper_id}, Swipee: {new_swipe.swipee_id}, Result: {new_swipe.swipe_result}")
            return new_swipe

        # If Given Swipe_Result is Rejected, set Stored Swipe Record as Rejected, Pass
        elif new_swipe_result == "REJECTED":
            swipe_record.swipe_result = "REJECTED"

        # If Both Stored Swipe and New is PENDING, Turn to Accepted, Indicating Successful Match
        elif swipe_record.swipe_result == "PENDING" and new_swipe_result == "PENDING":
            swipe_record.swipe_result = "ACCEPTED"

        return swipe_record