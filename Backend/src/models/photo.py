# Author: Joshua Ferguson

from datetime import datetime, timezone

from Backend.src.extensions import db, ma  # DB and Marshmallow Instances


class UserPhoto(db.Model):
    __tablename__ = "user_photos"  # Define the table name

    # Supplementary ID for Messages
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys - User ID's  of Owner
    user_id = db.Column(
        db.String(64),
        db.ForeignKey("users.id"),
        name="fk_user_photo_owner",
        nullable=True,
    )

    url = db.Column(db.String, nullable=False)  # unique constraint

    # If the Photo is a Gallery Photo, title and  Description Are Needed
    title = db.Column(db.String(100), nullable=True)  #
    description = db.Column(db.String(500), nullable=True)

    # Metadata Fields
    is_main_photo = db.Column(db.Boolean, nullable=False, default=False)
    upload_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )
    # is_fake = db.Column(db.Boolean, nullable=True) # Is the Photo Fake or Not

    # Unique Constraint on url and is_main_photo, and user_id
    db.UniqueConstraint("url", "is_main_photo", "user_id")


# Marshmallow Base Schema for the Message
class UserPhotoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserPhoto
        load_instance = True
        include_relationships = True

    # Validation is Done Prior to  Upload to S3 and DB - In Services
