
import validators # URL Validation

from marshmallow_sqlalchemy import fields
from sqlalchemy.orm import relationship
from marshmallow import validates, ValidationError
from better_profanity import profanity # Profanity Filter

from  Backend.src.extensions import db, ma # Import the Database and Marshmallow - SQLAlchemy and Marshmallow --> Flask

# ---TODO --- 
# ? Normalize Address Information - Separate Tables for City, State, and Country ??
class Address(db.Model):
    __tablename__ = 'addresses' # Define the table name
    
    id = db.Column(db.Integer, primary_key=True) # Primary Key
  
    # Foreign Keys - User ID Associated with Address    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Location Information - Street Table, which Links to City, State, and Country
    
    # Right Now - Street, City, State, and Country are all in the Address 
    street = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    country_initials = db.Column(db.String(10),nullable=False)
    
    # -----Relationships-----
    user_address = relationship('User', back_populates='address')
  
  