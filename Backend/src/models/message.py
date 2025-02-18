# Desc: Message Model and Schema for Messages Table
# Schema for Deserializing and Serializing
from datetime import datetime, timezone
from marshmallow import ValidationError, validates

from marshmallow_sqlalchemy import fields
from sqlalchemy.orm import relationship

from Backend.src.extensions import db, ma # DB and Marshmallow Instances
from Backend.src.models.user import UserSchema # User Model
from Backend.src.validators.text_val import TextValidator # Custom Validators
 
# Example JSON Response for querying a Message

#   {
#    "id": 1,
#    "messager": {
#        "id": 2,
#        "username": "john_doe"
#         ...,
#    },
#    "messagee": {
#        "id": 3,
#        "username": "jane_smith",
#         ...,
#    },
#    "message": "Hello, how are you?",
#    "message_date": "2022-01-01 12:00:00",
#    "message_read": false
#   }

MESSAGE_CONTENT_LENGTH = 500

# Message Model for Messages Table
# TODO: Implement CASCADE on User Deletion
class Message(db.Model):
    __tablename__ = 'messages' # Define the table name
    
    # Supplementary ID for Messages
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys - User ID's  of Sender and Receiver
    # On Delete of User - Cascade to Remove Associated Messages
    messager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    messagee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Message Content as String
    message_content = db.Column(db.String(MESSAGE_CONTENT_LENGTH), nullable=False)

    # TODO: Implement Date, Time, and TimeZone for Messages in the TimeDate Models
    message_date = db.Column(db.DateTime, nullable=False, default = datetime.now(timezone.utc))


    message_read = db.Column(db.Boolean, nullable=False, default=False) #Indicate if Message has been Read
    
    # -----Relationships-----
    """
    reports = relationship(
        "Report", 
        back_populates="reports_on_message",
        lazy="dynamic"
    )

    # Many to One Relationship - Multiples Swipes to One User
    messager = relationship(
        "User",  
        foreign_keys=[messager_id], 
        backref="messages_sent"
    )
    messagee = relationship(
        "User",  
        foreign_keys=[messagee_id], 
        backref="messages_received"
    )
    """

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
    messager = fields.Nested(UserSchema)
    messagee = fields.Nested(UserSchema)
    
    
# Nested Message Schema for Messagee and Messager with Only Emails
class MessageSchemaOnlyEmails(MessageSchema):
    class Meta:
        model = Message
        load_instance = True
        include_relationships = True
        
    # Nested User Schema for Messager and Messagee
    messager = fields.Nested(UserSchema(only=("email",)))
    messagee = fields.Nested(UserSchema(only=("email",)))