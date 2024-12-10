from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
import logging

from src.extensions import db

# Import the Models and Schemas
import src.models as models

# Usage: User.query.all() - Returns all Users in the Database

# TODO: ? Determine if Parameters should be passed in as JSON or URL Parameters in Routes ?

# TODO: ? Write a Validation Wrapper Function to Validate JSON Payloads
    # Each Route will call the Validation Function to Ensure Proper Data is Passed
    # If Data is Invalid or Missing, Return Bad Status and Error Message
    
# TODO: Implement a Response Wrapper Function to Return Standard Responses and Status Codes
# TODO: Implement a Function to Catch and Return Standard Error Messages

# TODO-Later: Implement Token-Based type system for Authentication and Access to Routes
# TODO-Later: Implement a Logging System to Log Errors and Events in the API
    

# -----Standard Response Codes Returned from Routes-----
# 200 - OK
# 201 - Created
# 400 - Bad Request
# 404 - Not Found
# 409 - Conflict
# 500 - Internal Server Error
#-------------------------------------------------------

# Create a new Blueprint for the API
# This will allow us to separate the API routes from the main app - If needed
app = Blueprint('app', __name__)


# Default Route - Home Page
@app.route('/')
def home():
    return "Welcome to the UnHinged API!", 200

# -----User Routes-----

# Create a new user in RDS
# POST /Users/Create
@app.route('/users', methods=['POST'])
def create_user():
    """
    Summary: Create a new user and add it to the database.
    
    Payload: JSON object with the following fields:
        - name: str, required
        - email: str, required
        
    Returns:
        str: A message indicating the success or failure of the user creation.
        Returs standard response codes (see above):
    """
    
    try:
        
        # Get the data from the request body
        data = request.get_json()
        
         # Validate the input
        if not data or not data.get('name') or not data.get('email'):
            return jsonify({"error": "Name and email are required fields."}), 400
        
        # Extract the values from the data
        name = data.get('name')
        username = data.get('username')
        email = data.get('email')
        
        # Check if the user already exists - Filter by email
        existing_user = models.user.User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "User with this Email already exists."}), 409
        
        # Create a new user object
        new_user = models.user.User(name=name,username=username,email=email)
        
        # Add the new user to the session
        db.session.add(new_user)
        # Commit the changes to the database
        db.session.commit()
        
        return jsonify({"Success":"User created successfully!"}), 201
    
    except SQLAlchemyError as e:
        
        # Rollback the session in case of an error, and return the error
        db.session.rollback()
        return jsonify({"error": "Database error occurred.", "details": str(e)}), 500
    
    except Exception as e:
        
        # Unexpected error, return Details back
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500

# Get all users from RDS
# GET /Users/GetAll
@app.route('/users', methods=['GET'])
def get_all_users():
    """
    Summary: Get all users from the database.
    
    Returns:
        list: A list of all users in the database.
        
    """
    try:
        # Get all users from the database
        users = models.user.User.query.all()
        
    except Exception as e:
            return jsonify({"error": "An error occurred"}), 500
        
    # Return the users as a list of dictionaries
    return jsonify([user.to_dict() for user in users]), 200

# Get user by ID from RDS
# GET /Users/Get/{id}
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id) :
    return db.get_or_404(models.user.User, id).to_dict()


#-----Match Routes-----

# Get all matches for a user
# GET /Users/Matches/{email}
@app.route('/users/matches/<string:email>', methods=['GET'])
def get_matches(email):
    """
    Summary: Get all matches for a user by ID.
    
    Parameters:
        email (string): The Email of the user.
        
    Returns:
        JSON with list: A list of matches for the user. - Including Matcher, Matchee and Match Date
        
       
    """
    # Get the matches for the user
    matches = models.match.Match.query.filter_by(matcher=email).all()
    
    # Return the matches - 
    return jsonify([match.to_dict() for match in matches]), 200


# Create a new match event of a User
# POST /users/matches
@app.route('/users/matches/<string:email>', methods=['GET'])
def create_match():
    """
    Summary: Create a new match event and add it to the database.
    
    Payload: JSON object with the following fields:
        - matcher: int, required
        - matchee: int, required
        - match_date: str, required
        
    Returns:
    
        str: Success or Failure of the match creation.
        
            201 Created for successful creation.
            400 Bad Request for invalid input.
            500 Internal Server Error for unexpected issues.

    """
    
    try:
        
        # Get the data from the request body
        data = request.get_json()
        
        # Validate the input
        # TODO - Implement Validation Function
        #if not data or not data.get('matcher') or not data.get('matchee') or not data.get('match_date'):
            #return jsonify({"error": "All fields are required."}), 400
        
        # Extract the values from the data
        matcher = data.get('matcher')
        matchee = data.get('matchee')
        match_date = data.get('match_date')
        
        # Create a new match object
        new_match = models.match.Match(matcher=matcher, matchee=matchee, match_date=match_date)
        
        # Add the new match to the session
        db.session.add(new_match)
        # Commit the changes to the database
        db.session.commit()
        
        return "Match created successfully!", 201
    
    except SQLAlchemyError as e:
        
        # Rollback the session in case of an error, and return the error
        db.session.rollback()
        return jsonify({"error": "Database error occurred.", "details": str(e)}), 500
    
    except Exception as e:
        
        # Unexpected error, return Details back
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500


#-----Swipe Routes-----

# Post A Swipe Event to the Database - Swipe Right or Left
# POST /Users/Swipes 
# 0 - Pending (Swiper Swiped Right, Swipee Hasn't Swiped Back Yet), 
# 1 - Accepted (Both Swiped Right),
# 2 - Rejected (Swiper Swipped Right, Swipee Swiped Left)
@app.route('/users/swipe', methods=['POST'])
def create_swipe():
    """
    Summary: Create a new swipe event and add it to the database.
    
    Payload: JSON object with the following fields:
        - swiper: int, required
        - swipee: int, required
        - swipe_result: int, required
        - swipe_date: str, required
        
    Returns:
        str: A message indicating the success or failure of the swipe creation.
        Returns standard response codes (see above):
    """
    
    try:
        
        # Get the data from the request body
        data = request.get_json()
        
        # Validate the input
        # TODO - Implement Wrapper Validation Function
        if not data or not data.get('swiper') or not data.get('swipee') or not data.get('swipe_result') or not data.get('swipe_date'):
            return jsonify({"error": "All fields are required."}), 400
        
        # Extract the Swiper and Swipee Users
        swiper = data.get('swiper')
        swipee = data.get('swipee')
        swipe_result = data.get('swipe_result') # 0 - Pending, 1 - Accepted, 2 - Rejected
        swipe_date = data.get('swipe_date') # Date of the Swipe
        
        # Create a new swipe object
        new_swipe = models.swipe.Swipe(swiper=swiper, swipee=swipee, swipe_result=swipe_result, swipe_date=swipe_date)
        
        # Add the new swipe to the session
        db.session.add(new_swipe)
        # Commit the changes to the database
        db.session.commit()
        
        # Log the success and return the message
        logging.info(f"Swipe created successfully! - {new_swipe}")
        return "Swipe created successfully!", 201
    
    except SQLAlchemyError as e:
        
        # Rollback the session in case of an error, and return the error
        db.session.rollback()
        return jsonify({"error": "Database error occurred.", "details": str(e)}), 500
    
    except Exception as e:
        
        # Unexpected error, return Details back
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500
    
    
    
@app.route('/users/swipe/<string:email>', methods=['GET'])
def get_swipes():
    """
    Summary: Get all swipes for a user by ID.
        
    Returns:
        JSON with list: A list of swipes for the user.
        0 - Pending (Swiper Swiped Right, Swipee Hasn't Swiped Back Yet),
        1 - Accepted (Both Swiped Right),
        2 - Rejected (Swiper Swipped Right, Swipee Swiped Left)
        
        Example Return:
        [
            {
                "id": 1,
                "swiper": 1,
                "swipee": 2,
                "swipe_result": 1,
                "swipe_date": "2022-01-01"
            }
        
    """
    
    # Get the data from the request body
    data = request.get_json()
    
    email = data.get('email')
    
    # Get the swipes for the user
    swipes = models.swipe.Swipe.query.filter_by(swiper=email).all()
    
    # Return the swipes  
    return jsonify([swipe.to_dict() for swipe in swipes])