# Author: Joshua Ferguson

# Desc: User Model and Schema for Users Table
# Schema for Deserializing and Serializing

import uuid # UUID for User ID
from datetime import datetime, timezone

from marshmallow_sqlalchemy import fields
from sqlalchemy.orm import relationship
from marshmallow import validates, ValidationError
from better_profanity import profanity # Profanity Filter

# Import the Database and Marshmallow - SQLAlchemy and Marshmallow --> Flask
from  Backend.src.extensions import db, ma, bcrypt

from Backend.src.models.photo import UserPhoto # User Photo Model # Keep This Before User Model and Helper

# Last Import - Avoid Circular Imports
from Backend.src.models.model_helpers import UserModelHelper 
 
# TODO: User Model Needs Normalization - Separate Tables for User Information and Bio

class User(db.Model):
    __tablename__ = 'users' # Define the table name
    
    # Fields of Users, data types provided - May need to change
    id = db.Column(db.String(64), primary_key=True) # Primary Key

    username = db.Column(db.String(50), nullable=True)
    password_hash = db.Column(db.String(128), nullable=True)  # Store hashed password (email users only)   # TODO: Hash + Salt Password
    
    # Unique Constraint on Email
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    auth_provider = db.Column(db.String(36), nullable=False)  # "apple" or "email"
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    # General User Information
    name = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    
    # BROKEN / BUG Caused Circular DB DROP Constraints
    # Makes Reference to One Photo in Photos Table as Main Profile Picture
    #profile_picture_id = db.Column(db.Integer, 
                                  #db.ForeignKey('user_photos.id',ondelete='CASCADE'),name='fk_user_profile_picture"',
                                   #nullable=True,
                                   #) # Profile Picture - URL to Image

    bio = db.Column(db.String(500), nullable=True) # Bio - Description of User

    # Location Information
    state_code = db.Column(db.String(10), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    country_code = db.Column(db.String(10), nullable=True)
    
    # Flag to Indicate Fake User, Default is False - Internal Use
    is_fake = db.Column(db.Boolean, nullable=True, default=False)
    is_admin = db.Column(db.Boolean, nullable=True, default=False)

    # Combined matches (user is either the matcher or matchee)
    @staticmethod
    def get_matches(self):
        """
        Combines matches where the user is the matcher or the matchee.
        """
        helper = UserModelHelper(self.id)
        return helper.get_user_matches()
    
    @staticmethod
    def get_match_ids(self):
        """
        Combines matches where the user is the matcher or the matchee.
        """
        helper = UserModelHelper(self.id)
        return helper.get_user_matches_ids()
    
    @staticmethod
    def create_user(name=None,email=None, password=None, apple_sub=None):
        """Create a user with either Apple `sub` or email/password."""
        if apple_sub:
            user_id = apple_sub
            auth_provider = "apple"
            password_hash = None  # No password for Apple users
        else:
            user_id = str(uuid.uuid4())
            auth_provider = "email"
            password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(id=user_id, email=email, password_hash=password_hash, auth_provider=auth_provider,name=name)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def hard_delete_user(self):
        """Delete a user."""
        db.session.delete(self)
        db.session.commit()

    #@staticmethod
    #def soft_delete_user(self):
        #"""Soft delete a user."""
        #self.deleted = True
        #db.session.commit()
        


# Marshmallow Schema for the User Model
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_relationships = True

    # Validate the Age Field - Must be Greater than 18
    @validates("age")
    def validate_age(self, value):
        if value and value < 18:
            raise ValidationError("Age must be greater than 18.")

    # Validate Email Field - Must Contain an @ Symbol
    # TODO: Add More String Validation, Use Marshmallow Builtin Validation
    @validates("email")
    def validate_email(self, value):
        if not "@" in value:
            raise ValidationError("Email must be valid.")
        
    @validates("username")
    def validate_username(self, value):
        if value is None:
            return
        elif len(value) > 50:
            raise ValidationError("Username must be less than 50 characters.")
        elif len(value) < 1:
            raise ValidationError("Username must be at least 1 character.")
        
        elif profanity.contains_profanity(value):
            profanity.censor(value)
            raise ValidationError("Username contains profanity. Please choose a different username.")

    @validates("bio")
    def validate_bio(self,text):
        
        if text is None:  
            return # Allow Null Bio
        
        # Validate the Bio Length and Content
        elif len(text) > 500:
            raise ValidationError("Bio must be less than 500 characters.")
        elif len(text) < 1:
            raise ValidationError("Bio must be at least 1 character.")
        
        elif profanity.contains_profanity(text):
            profanity.censor(text)
            raise ValidationError("Bio contains profanity. Please choose a different bio.")
    
    """
    @validates("profile_picture")
    def validate_profile_picture(self, url):
        
        if url is None:  
            return # Allow Null Bio
        
        # Validate the URL Length and Content
        elif len(url) > 500:
            raise ValidationError("URL must be less than 500 characters.")
        elif len(url) < 1:
            raise ValidationError("URL must be at least 1 character.")
        #elif not validators.url(url):
            #raise ValidationError("Invalid URL. Please enter a valid URL.")
        elif profanity.contains_profanity(url):
            profanity.censor(url)
            raise ValidationError("URL contains profanity. Please choose a different URL.")
    """
