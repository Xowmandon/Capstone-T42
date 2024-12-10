# Desc: Swipe Model for Swipes Table
# Schema for Deserializing and Serializing

from src.extensions import db, ma # DB and Marshmallow Instances
from src.models.user import User, UserSchema # User Model

# Swipe Model for Swipes Table
class Swipe(db.Model):
    __tablename__ = 'swipes'
    
    # Foreign Keys - User ID's of Swiper and Swipee
    swiper = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    swipee = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    
    # ---Dimensional Fields---
   
    # TODO: Refactor with Enum for Swipe Result
    # 0 - Pending (Swiper Swiped Right, Swipee Hasn't Swiped Back Yet), 
    # 1 - Accepted (Both Swiped Right),
    # 2 - Rejected (Swiper Swipped Right, Swipee Swiped Left)
    swipe_result = db.Column(db.Integer, nullable=False)
    
    # ---Dimensional Fields---
    swipe_date = db.Column(db.DateTime, nullable=False)
    
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

    swiper = ma.Nested(UserSchema)
    swipee = ma.Nested(UserSchema)
    
    
    
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