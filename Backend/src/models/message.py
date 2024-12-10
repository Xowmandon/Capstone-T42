# Desc: Message Model and Schema for Messages Table
# Schema for Deserializing and Serializing

from marshmallow import ValidationError, validates
from better_profanity import profanity # Profanity Filter

from src.extensions import db, ma # DB and Marshmallow Instances

# Message Model for Messages Table
class Message(db.Model):
    __tablename__ = 'messages' # Define the table name
    
    # Supplementary ID for Messages
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys - User ID's  of Sender and Receiver
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
    
    