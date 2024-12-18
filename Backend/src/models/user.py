# Desc: User Model and Schema for Users Table
# Schema for Deserializing and Serializing

import validators # URL Validation

from marshmallow_sqlalchemy import fields
from sqlalchemy.orm import relationship
from marshmallow import validates, ValidationError
from better_profanity import profanity # Profanity Filter

from  Backend.src.extensions import db, ma # Import the Database and Marshmallow - SQLAlchemy and Marshmallow --> Flask

# TODO: User Model Needs Normalization - Separate Tables for User Information and Bio
# TODO: Implement Apple ID - For Authentication
# TODO: Refactor Nullable Fields to be Required - Add Default Values
class User(db.Model):
    __tablename__ = 'users' # Define the table name
    
    # Fields of Users, data types provided - May need to change
    id = db.Column(db.Integer, primary_key=True, nullable=True) # Primary Key

    username = db.Column(db.String(50), nullable=True)
    #password = db.Column(db.String(100), nullable=False)   # TODO: Hash + Salt Password
    
    # Unique Constraint on Email
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    # General User Information
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    
    #profile_picture = db.Column(db.String(500), nullable=True) # Profile Picture - URL to Image
    bio = db.Column(db.String(500), nullable=True) # Bio - Description of User

    # Location Information
    #latitude = db.Column(db.Float, nullable=True)
    #longitude = db.Column(db.Float, nullable=True)
    
    # Flag to Indicate Fake User, Default is False - Internal Use
    fake = db.Column(db.Boolean, nullable=True, default=False)
    
    #------------Relationships--------------
    dating_preference = relationship('DatingPreference', back_populates='user_dating_preference', uselist=False)
    address = relationship('Address', back_populates='user_address', lazy="select", uselist=False) 
    game_metrics = relationship('GameMetrics', back_populates='user_game_metrics',lazy="select", uselist=False)
    activity_metrics = relationship('ActivityMetrics', back_populates='user_activity_metrics',lazy="select", uselist=False)
    
    # Swipes, Matches, and Messages - One to Many Relationships - User Can Have Many Swipes, Matches, and Messages    
    swipes_as_swiper = relationship(
        "Swipe",
        foreign_keys="Swipe.swiper_id",
        back_populates="swiper",
        lazy="dynamic"
    )
    
    swipes_as_swipee = relationship(
        "Swipe",
        foreign_keys="Swipe.swipee_id",
        back_populates="swipee",
        lazy="dynamic"
    )
    
    # Matches where the user is the matcher
    matches_as_matcher = relationship(
        "Match",
        foreign_keys="Match.matcher_id",
        back_populates="matcher",
        lazy="dynamic"
    )

    # Matches where the user is the matchee
    matches_as_matchee = relationship(
        "Match",
        foreign_keys="Match.matchee_id",
        back_populates="matchee",
        lazy="dynamic"
    )
    
    # Messages
    messages_sent = relationship(
        "Message",
        foreign_keys="Message.messager_id",
        back_populates="messager",
        lazy="dynamic"
    )
    
    messages_received = relationship(
        "Message",
        foreign_keys="Message.messagee_id",
        back_populates="messagee",
        lazy="dynamic"
    )
    
    
    # Reports 
    reports_received = relationship(
        "Report",
        foreign_keys="Report.reportee_id",
        back_populates="reportee",
        lazy="dynamic"
    )
    reports_sent = relationship(
        "Report",
        foreign_keys="Report.reporter_id",
        back_populates="reporter",
        lazy="dynamic"
    )
    
    
    # Combined matches (user is either the matcher or matchee)
    @property
    def matches(self):
        """
        Combines matches where the user is the matcher or the matchee.
        """
        return self.matches_as_matcher.union(self.matches_as_matchee)


# Marshmallow Schema for the User Model
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_relationships = True

        
    # Validate the Age Field - Must be Greater than 18
    @validates("age")
    def validate_age(self, value):
        if value < 18:
            raise ValidationError("Age must be greater than 18.")

    # Validate Email Field - Must Contain an @ Symbol
    # TODO: Add More String Validation, Use Marshmallow Builtin Validation
    @validates("email")
    def validate_email(self, value):
        if not "@" in value:
            raise ValidationError("Email must be valid.")
        
    @validates("username")
    def validate_username(self, value):
        if len(value) > 50:
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
    
    @validates("profile_picture")
    def validate_profile_picture(self, url):
        
        if url is None:  
            return # Allow Null Bio
        
        # Validate the URL Length and Content
        elif len(url) > 500:
            raise ValidationError("URL must be less than 500 characters.")
        elif len(url) < 1:
            raise ValidationError("URL must be at least 1 character.")
        elif not validators.url(url):
            raise ValidationError("Invalid URL. Please enter a valid URL.")
        elif profanity.contains_profanity(url):
            profanity.censor(url)
            raise ValidationError("URL contains profanity. Please choose a different URL.")
    