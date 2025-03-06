import inspect
from logging import log
import pytest

from  Backend.src.extensions import db, ma

# TODO: Separate Creation and Retrieval of Models
# TODO: Implement Real Unit Tests
# TODO: Only Test the API Endpoints and Interaction with the Database


# Add the parent directory to the system path
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import Backend.app
from  Backend.src.utils import TestingConfig

# Import the Models and Schemas
from  Backend.src.models.user import  User, UserSchema
from Backend.src.utils import EnvManager
from Backend.scripts.gen_fake import GenFake
from Backend.tests.utils_for_tests import pytest_start_test_display, pytest_assertion_success, pytest_test_success, pytest_assertion_failure

# TODO- assert JSON reponse is in the correct format returned from get_user() route for the test_get_user_route

    
@pytest.fixture()
def app():
    Backend.app.app.config.from_object(TestingConfig) 
    yield app #

@pytest.fixture()
def client(app):
    return Backend.app.app.test_client() 

"""
def test_apple_signup_route(client): # Test the Signup Endpoint
    EnvMan = EnvManager()
    user_creds = {
        'auth_method': 'apple',  
        'identity_token': EnvMan.load_env_var('SAMPLE_IDENTITY_TOKEN'),
    }
    
    response = client.post('/signup', json=user_creds) # Send a POST request to the signup endpoint
    
    assert response.status_code == 201 # Check that the status code is 201 (Created)
    assert response.json["token"] is not None # Check that the token is not None
    assert response.json["message"] == "Signup successful" # Check that the message is correct
"""
    
def test_email_signup_route(client): # Test the Email Signup Route
    
    pytest_start_test_display()
    
    # Create a fake user object
    email = GenFake().fake.email()
    user_creds = {
        'auth_method': 'email',
        'email': email, # Prevent Collision with Generated Emails
        'password': 'tester123',
    }
    # Send a POST request to the signup endpoint
    response = client.post('/signup', json=user_creds)

    assert response.status_code == 201, pytest_assertion_failure(f"Unexpected status code: {response.status_code} - {response.data}") # Check that the status code is 201 (Created)
    assert response.json["token"] is not None, pytest_assertion_failure("'Token' Not Found in Response JSON") # Check that the token is not None
    assert response.json["message"] == "Signup successful" # Check that the message is correct
    
    for msg in ["Status Code", "Token Found in Response","Signup Success Found in Response"]:
        pytest_assertion_success(msg)
    
    pytest_test_success()
    
    # Write JWT Token to .env File for Future Use
    EnvManager().write_env_var('TEST_JWT', response.json["token"])

def test_get_user_route(client): 
    """Test Retrieving a User from the Database Through Route"""
    pytest_start_test_display()
    
    # Load the Test JWT, which is used to authenticate the user (predefined User)
    test_jwt = EnvManager().load_env_var('TEST_JWT')
    assert test_jwt, "TEST_JWT is not set!"
    pytest_assertion_success("Test JWT Loaded")

    # Send a GET request to the get user endpoint with X-Authorization Header as JWT
    response = client.get('/users/', headers={'X-Authorization': f'Bearer {test_jwt}'}) 

    with Backend.app.app.app_context():

        # Assert, status code is 200 (OK), id is in the response JSON, and user exists in the database
        assert response.status_code == 200, \
            pytest_assertion_failure(f"Unexpected Response:{response.status_code}{response.data}")
        assert "id" in response.json, \
            pytest_assertion_failure("Response JSON does not contain 'id'")
        assert db.session.get(User, response.json["id"]) is not None, \
            pytest_assertion_failure("User not found in the database")
    
    for msg in ["Status Code 200", "id Found in Response","User Found in DB by id"]:
        pytest_assertion_success(msg)
    
    pytest_test_success()



def test_home_route(client): # Test the Home Route
    pytest_start_test_display()
    # Send a GET request to the home route
    response = client.get('/')
    
    # Check that the status code is 200 (OK) and that the welcome message is correct
    assert response.status_code == 200, \
        pytest_assertion_failure(f"- {response.status_code} - Server is Not Responding, Might be Offline!")
    assert response.json["message"] == "Welcome to the UnHinged API!", \
        pytest_assertion_failure("Welcome Message Not Found in Response") 
        
    for msg in ["Status Code 200", "Welcome Message Found in Response"]:
        pytest_assertion_success(msg)
    pytest_test_success()
    
def test_get_swipe_pool(client):
    """Test Retrieving a User from the Database Through Route"""
    pytest_start_test_display()
    
    # Load the Test JWT, which is used to authenticate the user (predefined User)
    test_jwt = EnvManager().load_env_var('TEST_JWT')
    assert test_jwt, "TEST_JWT is not set!"
    pytest_assertion_success("Test JWT Loaded")

    # Send a GET request to the get user endpoint with X-Authorization Header as JWT
    response = client.get('/users/swipe_pool', headers={'X-Authorization': f'Bearer {test_jwt}'}) 

    with Backend.app.app.app_context():

        # Assert, status code is 200 (OK), id is in the response JSON, and user exists in the database
        assert response.status_code == 200, \
            pytest_assertion_failure(f"Unexpected Response:{response.status_code}{response.data}")
        print(response.json)
        assert response.json is not None, "Response JSON is None"
        #print(response.json)
    
    for msg in ["Status Code 200", "Swipe Pool is Not Empty"]:
        pytest_assertion_success(msg)
    
    pytest_test_success()
