import unittest
from flask_testing import TestCase
import os, sys

# TODO: Separate Creation and Retrieval of Models
# TODO: Implement Real Unit Tests
# TODO: Only Test the API Endpoints and Interaction with the Database


# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app import app
from src.utils import TestDBConfig
from src.models import db, User

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
    def test_create_user(self):
        
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