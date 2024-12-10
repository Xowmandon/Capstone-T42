from src.models import * # Import all the Models, db and ma (Database and Marshmallow)
from marshmallow import validates, ValidationError
#import src.routes # Import the routes

# Marshmallow Schema for the User Model
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        
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
             
# Marshmallow Schema for the Match Model
class MatchSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Match
    
    matcher = ma.Nested(UserSchema)
    matchee = ma.Nested(UserSchema)
        
# Marshmallow Schema for the Swipe
class SwipeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Swipe
       
# Marshmallow Schema for the Message
class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
    
    @validates("message")
    def validate_message(self, content):
        
        # Validate the Message Length
        if len(content) > 500:
            raise ValidationError("Message must be less than 500 characters.")
        elif len(content) < 1:
            raise ValidationError("Message must be at least 1 character.")
        
        # Validate the Message Content for Severe Profanity
        
                 
# Marshmallow Schema for the Report

class ReportSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Report
  