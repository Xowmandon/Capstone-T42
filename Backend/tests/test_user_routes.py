import unittest, json, requests
from flask import jsonify
from flask_testing import TestCase
from unittest.mock import patch

from Backend.app import app
from  Backend.src.extensions import db, ma

from  Backend.src.utils import TestDBConfig
import Backend.src.models as models
from Backend.scripts.gen_fake import GenFake

user_schema = models.user.UserSchema()

def test_post_user():
    
    # Define the API URL
    url = "http://127.0.0.1:5000/users"
    
    
    with app.app_context():
        
        # Clear the DB
        db.drop_all()
        db.create_all()
        
        # Generate Fake User Pair
        # Add the fake users to the DB if they don't exist
        Generator = GenFake()
        new_user = Generator.gen_fake_user()
        
        payload = {
            "email": new_user.email,
            "username": new_user.username,
            "name": new_user.name,
            "age": new_user.age,
            "gender": new_user.gender
        }   
        
            # Send the GET request with JSON payload
        response = requests.post(url, json=payload)
        
        user_added = models.user.User.query.filter_by(email=new_user.email).first()
        print(f"User Added: {user_schema.dump(user_added)}")

        # Print the response
        print(f"Status Code: {response.status_code}")
        print("\n")
        print(f"----Response JSON----\n: {response.json()}")

        
        
if __name__ == "__main__":
    test_post_user()
    
    