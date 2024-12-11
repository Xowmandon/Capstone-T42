# BUG:sqlalchemy.exc.InvalidRequestError: 
# Column users.id has been marked as a sentinel column with no default generation function; 
# it at least needs to be marked nullable=False assuming user-populated sentinel values will be used.

# BUG: Currntly Not Working as Expected

import unittest, json, requests
from flask import jsonify
from flask_testing import TestCase
from unittest.mock import patch

from Backend.app import app
from  Backend.src.extensions import db, ma, URL

from  Backend.src.utils import TestDBConfig
import Backend.src.models as models
from Backend.scripts.gen_fake import GenFake

user_schema = models.user.UserSchema()

class TestGetConversationRoute(TestCase):
    """Tests for the /users/messages/conversation route."""

    def create_app(self):
        # Use testing configuration
        app.config.from_object(TestDBConfig)
  

        return app

    def setUp(self):
        # Create tables and set up test data
        db.create_all()
        self.fakeFac = GenFake()
        # Create mock users
        self.user1 = self.fakeFac.gen_fake_user()
        self.user2 = self.fakeFac.gen_fake_user()
        db.session.add(self.user1)
        db.session.add(self.user2)

        # Create mock messages
        self.messages = [
            self.fakeFac.gen_fake_message(self.user1, self.user2),
            self.fakeFac.gen_fake_message(self.user2, self.user1),
        ]
        db.session.add_all(self.messages)
        db.session.commit()

    def tearDown(self):
        # Clean up the database after each test
        db.session.remove()
        db.drop_all()


def test_get_conversation():
    
    # Define the API URL
    url = URL + "/users/messages/conversation"
    
    with app.app_context():
        
        """ # Clear the DB
        db.drop_all()
        db.create_all()"
        """
        
        # Generate Fake User Pair
        # Add the fake users to the DB if they don't exist
        Generator = GenFake()
        gen_pair =(Generator.gen_fake_user(), Generator.gen_fake_user())
        if not Generator.add_fake_users_to_db(gen_pair):
            exit(1)

        # Get the generated users and their emails
        user1 = gen_pair[0]
        user2 = gen_pair[1]
        user1_email = user1.email
        user2_email = user2.email
        
        print(f"Generated Fake User Pair: {user1_email}, {user2_email}")
        print("----------------------\n")
        
        messages = Generator.gen_fake_conversation(user1, user2, num_messages=15)
        message_schema = models.message.MessageSchema()
        
        # Add the new message to the session
        db.session.add_all(messages)
        db.session.commit()

    # Payload with required and optional parameters
    payload = {
        "messager_email": user1_email,
        "messagee_email": user2_email,
        "limit": 10,
        "offset": 0
    }

    # Send the GET request with JSON payload
    response = requests.get(url, json=payload)

    # Print the response
    print(f"Status Code: {response.status_code}")
    print("\n")
    print(f"----Response JSON----\n: {response.json()}")

if __name__ == "__main__":

    test_get_conversation()
