import unittest
from flask_testing import TestCase
import os, sys

from Backend.src.extensions import db

# TODO: Separate Creation and Retrieval of Models
# TODO: Implement Real Unit Tests
# TODO: Only Test the API Endpoints and Interaction with the Database


# Add the parent directory to the system path
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Backend.app import app
from Backend.src.utils import TestDBConfig

# Import the Models and Schemas
from Backend.src.models.user import User, UserSchema
from Backend.src.models.match import Match, MatchSchema
from Backend.src.models.swipe import Swipe, SwipeSchema
from Backend.src.models.message import Message, MessageSchema

class AppTest(TestCase):
    def create_app(self):
        app.config.from_object(TestDBConfig)
        return app

    # Runs Before Each Test, Sets Up The Database
    def setUp(self):
        with app.app_context():
            # Drop all tables in the database to ensure a clean state
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            # Drop all tables in the database
            db.drop_all()
            db.session.remove()

    # Creates Fake User - Correctly Adds User to DB
    # Uses External Request to Create User
    def test_create_user_external(self):
        
        with app.app_context():
            # Add a test user by calling the create_user endpoint
            response = self.client.post('/users', json={
                'name': 'Tester Smith',
                'username': 'testuser123',
                'email': 'testuser@example.com'
            })
            # Ensure the user was created successfully
            self.assertEqual(response.status_code, 201)
            #self.assertIn(b'User created successfully!', response.data)
            db.session.commit()
            
    # Creates Fake User - Correctly Adds User to DB
    # Uses Internal ORM Functionality to Create User
    def test_create_get_user_internal(self):
        
        #Create a new test user object and add it to the database
        user = User(name='Test User', username="tester", email='testuser@example.com')
        db.session.add(user)
        db.session.commit()

        # Attempt to retrieve the user from the database
        response = self.client.get(f'/users/{user.id}')
        
        # Check if the response is 200 OK
        self.assertEqual(response.status_code, 200)
        
         # Check if the response is the same as the user object
        self.assertEqual(response.json, user.to_dict())

    # Testing Retrieval of a Match Object
    def test_get_matches(self):
        """ Summary: Test Get all matches for a user by ID.
        """
    
        # Create test Matcher and Matchee Users
        matcher = User(name='Matcher User', username="Matcher", email="Matcher@example.com")
        matchee = User(name='Matchee User', username="Matchee", email="Matchee@example.com")
       
       # Add Matched Users to DB
        db.session.add(matcher)
        db.session.add(matchee) 
        
        # Create a new match object and add it to the database
        match = Match(matcher=matcher.email, matchee=matchee.email, match_date='2024-01-01')   
        db.session.add(match)   

        # GET Matches for User
        response = self.client.get(f'/users/matches/{matcher.email}')
        self.assertEqual(response.status_code, 200)
        
        # Check if the response is the same as the match object created here
        self.assertEqual(response.json, [match.to_dict()])
        
    def test_create_swipe(self):
        response = self.client.post('/users/swipe', json={
            'swiper': 1,
            'swipee': 2,
            'swipe_result': 1,
            'swipe_date': '2022-01-01'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, b"Swipe created successfully!")


    # Default Test - Checks if the Home Page is Accessible
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the UnHinged API', response.data)

    # Get All Users From DB - Creates Fake User - TODO Checks if User is in DB
    def test_get_all_users(self):
        
        with app.app_context():
            self.test_create_user()
            response = self.client.get('/users')
            self.assertEqual(response.status_code, 200)
            print(f"--------------USER-------------------{response.data}")
            db.session.commit()

if __name__ == "__main__":
    unittest.main()