# Desc: User Model and Schema for Users Table
# Schema for Deserializing and Serializing

from marshmallow import validates, ValidationError
from better_profanity import profanity  #Profanity Filter

from src.extensions import db, ma # Import the Database and Marshmallow - SQLAlchemy and Marshmallow --> Flask



# TODO: Add more fields to the User Model to Match the Frontend and ERD
class User(db.Model):
    __tablename__ = 'users' # Define the table name
    
    # Fields of Users, data types provided - May need to change
    id = db.Column(db.Integer, primary_key=True, nullable=True) # Primary Key
    
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    #password = db.Column(db.String(100), nullable=False)   # TODO: Hash + Salt Password
    email = db.Column(db.String(100), unique=True, nullable=False) # Unique Email Address
    
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    
    fake = db.Column(db.Boolean, nullable=False) # Flag to Indicate Fake User
    
    # to_dict Method to Serialize User Object to JSON
    # TODO: Correlate with Self Attributes
    """def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'gender': self.gender
        }
        
    # TODO: Correlate with Self Attributes
    # Consider __dir__ for User Object
    def to_csv(self):
        return f"{self.name}, {self.username}, {self.email}, {self.gender}"
        
    # Convert User Object to String Format, or CSV Format
    # TODO: Correlate with Self Attributes
    #def __str__(self):
        #return f"{self.id},{self.name},{self.username},{self.email}"

    # String representation of a User, Outputting each Field Associated
    # TODO: Correlate with Self Attributes
    def __repr__(self):
        return f"<User id={self.id}, name={self.name}, username={self.username}, email={self.email}, {self.gender}>"

    #def __dir__(self):
        #return ['id', 'name', 'username', 'email']
    """



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
        
    @validates("username")
    def validate_username(self, value):
        if len(value) > 50:
            raise ValidationError("Username must be less than 50 characters.")
        elif len(value) < 1:
            raise ValidationError("Username must be at least 1 character.")
        
        elif profanity.contains_profanity(value):
            profanity.censor(value)
            raise ValidationError("Username contains profanity. Please choose a different username.")
