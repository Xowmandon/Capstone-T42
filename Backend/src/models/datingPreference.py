from marshmallow import ValidationError, validates


from Backend.src.extensions import db, ma # Import the Database and Marshmallow - SQLAlchemy and Marshmallow --> Flask

from Backend.src.models import user, UserSchema # Import the User Model


# Dating Preference Model for Dating Preferences Table

class DatingPreference(db.Model):
    __tablename__ = 'DatingPreferences' # Define the table name
    
    # Fields of Dating Preferences, data types provided - May need to change
    id = db.Column(db.Integer, primary_key=True, nullable=True) # Primary Key
    
    # Sexual Orientation
    sexual_orientation = db.Column(db.String(50), nullable=False)
    
    # Age Preference - Lower and Upper Bound
    age_preference_lower = db.Column(db.Integer, nullable=False)
    age_preference_upper = db.Column(db.Integer, nullable=False)
    
    # Reference to Users Table
    # On Delete Cascade to Remove Dating Preference if User is Deleted
    user = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True,nullable=False)
    
    
    # String representation of a Dating Preference, Outputting each Field Associated
    def __repr__(self):
        return f"<DatingPreference id={self.id}, preference={self.preference}>"

class DatingPreferenceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DatingPreference
        load_instance = True
        
    # Nested User Schema for User
    user = ma.Nested(UserSchema)
        
    # Validate the Age Preference - Lower Bound Must be Less than Upper Bound
    @validates("age_preference_lower")
    def validate_age_preference_lower(self, value):
        if value > self.age_preference_upper:
            raise ValidationError("Lower Age Preference Must be Less than Upper Age Preference")
        elif value < 18:
            raise ValidationError("Age Preference Must be Greater than 18")
        return value
    
    # Validate the Age Preference - Upper Bound Must be Greater than Lower Bound
    @validates("age_preference_upper")
    def validate_age_preference_upper(self, value):
        if value < self.age_preference_lower:
            raise ValidationError("Upper Age Preference Must be Greater than Lower Age Preference")
        return value
    