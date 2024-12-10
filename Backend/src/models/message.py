# Desc: Message Model and Schema for Messages Table
# Schema for Deserializing and Serializing

from marshmallow import ValidationError, validates
from better_profanity import profanity # Profanity Filter

from Backend.src.extensions import db, ma # DB and Marshmallow Instances



 
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



# Message Model for Messages Table
# TODO: Implement CASCADE on User Deletion
class Message(db.Model):
    __tablename__ = 'messages' # Define the table name
    
    # Supplementary ID for Messages
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys - User ID's  of Sender and Receiver
    # On Delete of User - Cascade to Remove Associated Messages
    messager = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    messagee = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Message Content as String
    message = db.Column(db.String(500), nullable=False)
    
    # ---Dimensional Fields---
    message_date = db.Column(db.DateTime, nullable=False)

    message_read = db.Column(db.Boolean, nullable=False) #Indicate if Message has been Read
    
    
    #def to_dict(self):
        #return {
            #'id': self.id,
            #'sender': User.query.get(self.sender),
            #'receiver': User.query.get(self.receiver),
            #'message': self.message,
            #'message_date': self.message_date,
            #'message_read': self.message_read
        #}

    #def __repr__(self):
        #return f"<Message id={self.id}, sender={self.sender}, receiver={self.receiver}, message={self.message}, message_date={self.message_date}>"


# Marshmallow Schema for the Message
class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        load_instance = True
    
    @validates("message")
    def validate_message(self, content):
        
        # Validate the Message Length
        if len(content) > 500:
            raise ValidationError("Message must be less than 500 characters.")
        elif len(content) < 1:
            raise ValidationError("Message must be at least 1 character.")
        
        # Potential-TODO: Add Profanity Filter with Probabilistic Censoring based on Sentences
        # Validate the Message Content for Severe Profanity
        elif profanity.contains_profanity(content):
            profanity.censor(content)
            #raise ValidationError("Message contains profanity. Censoring...")
    
