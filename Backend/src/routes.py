from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from models import db, User, Match, Message, Swipe, Report


# Create a new Blueprint for the API
# This will allow us to separate the API routes from the main app - If needed
app = Blueprint('app', __name__)


@app.route('/')
def home():
    return "Welcome to the Unhinged API!"

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
             Failure messages include details about the error.
        
            201 Created for successful creation.
            400 Bad Request for invalid input.
            409 Conflict for duplicate users.
            500 Internal Server Error for unexpected issues.

    """
    
    try:
        
        # Get the data from the request body
        data = request.get_json()
        
         # Validate the input
        if not data or not data.get('name') or not data.get('email'):
            return jsonify({"error": "Name and email are required fields."}), 400
        
        # Extract the values from the data
        name = data.get('name')
        email = data.get('email')
        
        # Check if the user already exists - Filter by email
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "User with this Email already exists."}), 409
        
        # Create a new user object
        new_user = User(name=name, email=email)
        
        # Add the new user to the session
        db.session.add(new_user)
        # Commit the changes to the database
        db.session.commit()
        
        return "User created successfully!"
    
    except SQLAlchemyError as e:
        
        # Rollback the session in case of an error, and return the error
        db.session.rollback()
        return jsonify({"error": "Database error occurred.", "details": str(e)}), 500
    
    except Exception as e:
        
        # Unexpected error, return Details back
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500

# Get user by ID from RDS
# GET /Users/Get/{id}
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id) :
    return db.get_or_404(User, id).to_dict()

# Get all matches for a user
# GET /Users/Matches/{id}
@app.route('/users/matches', methods=['GET'])
def get_matches(id):
    """
    Summary: Get all matches for a user by ID.
    
    Parameters:
        id (int): The ID of the user.
        
    Returns:
        list: A list of matches for the user.
        
    """
    # Get the matches for the user
    matches = Match.query.filter_by(matcher=id).all()
    
    # Return the matches
    return jsonify([match.to_dict() for match in matches])

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
             Failure messages include details about the error.
        
            201 Created for successful creation.
            400 Bad Request for invalid input.
            500 Internal Server Error for unexpected issues.

    """
    
    try:
        
        # Get the data from the request body
        data = request.get_json()
        
        # Validate the input
        # TODO - Implement Validation Function
        #if not data or not data.get('swiper') or not data.get('swipee') or not data.get('swipe_result') or not data.get('swipe_date'):
            #return jsonify({"error": "All fields are required."}), 400
        
        # Extract the values from the data
        swiper = data.get('swiper')
        swipee = data.get('swipee')
        swipe_result = data.get('swipe_result')
        swipe_date = data.get('swipe_date')
        
        # Create a new swipe object
        new_swipe = Swipe(swiper=swiper, swipee=swipee, swipe_result=swipe_result, swipe_date=swipe_date)
        
        # Add the new swipe to the session
        db.session.add(new_swipe)
        # Commit the changes to the database
        db.session.commit()
        
        return "Swipe created successfully!"
    
    except SQLAlchemyError as e:
        
        # Rollback the session in case of an error, and return the error
        db.session.rollback()
        return jsonify({"error": "Database error occurred.", "details": str(e)}), 500
    
    except Exception as e:
        
        # Unexpected error, return Details back
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500