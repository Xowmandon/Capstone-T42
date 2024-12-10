import unittest
from flask_testing import TestCase
import os, sys

from  Backend.src.extensions import db, ma

# TODO: Separate Creation and Retrieval of Models
# TODO: Implement Real Unit Tests
# TODO: Only Test the API Endpoints and Interaction with the Database


# Add the parent directory to the system path
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from  Backend.app import app
from  Backend.src.utils import TestDBConfig

# Import the Models and Schemas
from  Backend.src.models.user import User, UserSchema
from  Backend.src.models.match import Match, MatchSchema
from  Backend.src.models.swipe import Swipe, SwipeSchema
from  Backend.src.models.message import Message, MessageSchema
from Backend.src.models.datingPreference import DatingPreference, DatingPreferenceSchema


from Backend.scripts.gen_fake import GenFake



from Backend.src.routes import *
from Backend.src.models.user import UserSchema
from Backend.scripts.gen_fake import GenFake

class AppTest(TestCase):
    def create_app(self):
        app.config.from_object(TestDBConfig)
  

        return app

    # Runs Before Each Test, Sets Up The Database
    def setUp(self):
        with app.app_context():
            # Drop all tables in the database to ensure a clean state

            #db.drop_all()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            
            # Rollback the session to ensure that the database is in a clean state
            db.session.rollback()
            db.session.remove()
            #db.drop_all()

    # Creates Fake User - Correctly Adds User to DB
    # Uses External Request to Create User
    def test_create_user_external(self):
        # Create a fake user object
        user = {
            'name': 'John Doe',
            'username': 'johndoe',
            'email': GenFake().fake.email(), # Prevent Collision with Generated Emails
            'age': 25,
            'fake': True,
            'gender': 'male'
        }
        
        user_schema = UserSchema()
        user = user_schema.load(user)

        # Send a POST request to the create user endpoint
        response = self.client.post('/users', json=user_schema.dump(user))
        
        
        print(f"RESPONSE DATA: {response.data}")
        print(f"RESPONSE STATUS CODE: {response.status_code}")
        print(f"RESPONSE JSON: {response.json}")
        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, 201)
       
    # Creates Fake User - Correctly Adds User to DB
    # Uses Internal ORM Functionality to Create User
    def test_create_get_user_internal(self):
        
        #Create a new test user object and add it to the database
        user = GenFake().gen_fake_user()
        db.session.add(user)
        db.session.commit()
        

        # Attempt to retrieve the user from the database
        # Add Payload to Request
        response = self.client.get(f'/users/{user.email}')
        #response = self.client.get(f'/users/')
        
        self.assertEqual(response.status_code, 200)
        
        # Check if the response is the same as the user object
        #self.assertEqual(response.json, user.to_dict())
    

    # TODO - Currently Fails - Need to Fix
    # Testing Retrieval of a Match Object
    """def test_get_matches(self):
        \""" Summary: Test Get all matches for a user by ID.
        \"""
    
        matcher = GenFake().gen_fake_user()
        matchee = GenFake().gen_fake_user()
        
       # Add Matched Users to DB
        db.session.add(User(matcher))
        db.session.add(User(matchee)) 
        
        # Create a new match object and add it to the database
        match = Match(matcher=matcher, matchee=matchee, match_date='2024-01-01')
        
        
        db.session.add(match)   
        db.session.commit()

        # GET Matches for User
        response = self.client.get(f'/users/matches/{matcher.email}')
        
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        
        # Check if the response is the same as the match object created here
        #self.assertEqual(response.json, [match.MatchSchema().dump(match)])
    """  
    
    """def test_create_swipe(self):
        response = self.client.post('/users/swipe', json={
            'swiper': 1,
            'swipee': 2,
            'swipe_result': 1,
            'swipe_date': '2022-01-01'
        })
        db.session.commit()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, b"Swipe created successfully!")
    """

    """ # Default Test - Checks if the Home Page is Accessible
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the UnHinged API', response.data)
    """
    # Get All Users From DB 
    # Works as Expected
    #def test_get_all_users(self):
        
        #with app.app_context():
            #response = self.client.get('/users/{}')
            #self.assertEqual(response.status_code, 200)
            #print(f"--------------USERs-------------------\n{response.json}")

            #db.session.commit()
    
    
    """def test_del_user(self):
        user = GenFake().gen_fake_user()
        db.session.add(user)
        db.session.commit()
        response = self.client.delete(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"User deleted successfully!")
        
        """
if __name__ == "__main__":
    unittest.main()