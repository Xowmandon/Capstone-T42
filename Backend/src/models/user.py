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
    
    # Location Information
    #city = db.Column(db.String(50), nullable=True)
    #state = db.Column(db.String(50), nullable=True)
    #country = db.Column(db.String(50), nullable=True)
    
    # User Description and Profile Picture
    profile_picture = db.Column(db.String(500), nullable=True) # Profile Picture - URL to Image
    bio = db.Column(db.String(500), nullable=True) # Bio - Description of User
    
    # Dating Preferences - Age Range, Sexual Orientation, etc
    #dating_preference = db.Column(db.Integer,db.ForeignKey('DatingPreferences.id'),nullable=True) # Dating Preference
    
    # Flag to Indicate Fake User, Default is False - Internal Use
    fake = db.Column(db.Boolean, nullable=True, default=False)
    
    #------Relationships--------------
    #swipes = relationship('Swipe', backref='user_swipes')
    #matches = relationship('Match', backref='user_matches')
    #messages = relationship('Message', backref='user_messages')
    
    
    #all_matches_matcher = relationship("Match", foreign_keys="[Match.matcher_id]", backref="matcher_user")
    #all_matches_matchee = relationship("Match", foreign_keys="[Match.matchee_id]", backref="matchee_user")
    
    #@property
    #def get_all_matches(self):
        #MatchAlias = aliased(Match)
        #return [match for match in self.all_matches_matcher] + [match for match in self.all_matches_matchee]


    # String representation of a User, Outputting each Field Associated
    # TODO: Correlate with Self Attributes
    #def __repr__(self):
    #    return f"<User id={self.id}, name={self.name}, username={self.username}, email={self.email}, {self.gender}>"

    #def __dir__(self):
        #return ['id', 'name', 'username', 'email']
    


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
    