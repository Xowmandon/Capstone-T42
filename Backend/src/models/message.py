# Desc: Message Model and Schema for Messages Table
# Schema for Deserializing and Serializing
from datetime import datetime, timezone
from marshmallow import ValidationError, validates

from marshmallow_sqlalchemy import fields
from sqlalchemy.orm import relationship

from Backend.src.extensions import db, ma # DB and Marshmallow Instances
from Backend.src.validators.text_val import TextValidator # Custom Validators

#from Backend.src.models.user import user_schema  # Causing Circular Import
#from Backend.src.models.user import UserSchema # User Model # Causing Circular Import


MESSAGE_CONTENT_LENGTH = 500

# Message Model for Messages Table
# TODO: Implement CASCADE on User Deletion
class Message(db.Model):
    __tablename__ = 'messages' # Define the table name
    
    # Supplementary ID for Messages
    id = db.Column(db.Integer, primary_key=True)
    
    
    # Foreign Keys - User ID's  of Sender and Receiver
    # On Delete of User - Cascade to Remove Associated Messages
    messager_id = db.Column(db.String(64), db.ForeignKey('users.id'), nullable=False)
    #messagee_id = db.Column(db.String(64), db.ForeignKey('users.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)

    # Message Content as String
    message_content = db.Column(db.String(MESSAGE_CONTENT_LENGTH), nullable=False)

    # TODO: Implement Date, Time, and TimeZone for Messages in the TimeDate Models
    message_date = db.Column(db.DateTime, nullable=False, default = datetime.now(timezone.utc))


    message_read = db.Column(db.Boolean, nullable=False, default=False) #Indicate if Message has been Read
    

# Marshmallow Base Schema for the Message
class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        load_instance = True
        include_relationships = True

    @validates("message_content")
    def validate_message(self, content):
        # Length and Profanity Filter
        self.message_content = TextValidator.val_all(content,censor=True)


# Nested Message Schema for Messagee and Messager
class MessageSchemaNested(MessageSchema):
    class Meta:
        model = Message
        load_instance = True
        include_relationships = True


    # Nested User Schema for Messager and Messagee
   # messager = fields.Nested(user_schema)
    #messagee = fields.Nested(UserSchema)
    
    
# Nested Message Schema for Messagee and Messager with Only Emails