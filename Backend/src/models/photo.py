# Author: Joshua Ferguson

from datetime import datetime, timezone
from marshmallow import ValidationError, validates
from Backend.src.validators.image_val import ImageValidator


from Backend.src.extensions import db, ma # DB and Marshmallow Instances

class UserPhoto(db.Model):
    __tablename__ = 'user_photos' # Define the table name
    
    # Supplementary ID for Messages
    id = db.Column(db.Integer, primary_key=True)
    
    url = db.Column(db.String, nullable=False, unique=True)  # unique constraint
    
    # Foreign Keys - User ID's  of Owner
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'),name="fk_user_photo_owner", nullable=True)
    is_main_photo = db.Column(db.Boolean, nullable=False,default=False)

    # TODO: Implement Date, Time, and TimeZone for Messages in the TimeDate Models
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    size_mb = db.Column(db.Integer, nullable=True)
    
    # Unique Constraint on url
    

# Marshmallow Base Schema for the Message
class UserPhotoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserPhoto
        load_instance = True
        include_relationships = True


    # Validation is Done Prior to  Upload to S3 and DB - In Services
    
    