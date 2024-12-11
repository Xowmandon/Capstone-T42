
from flask import request, jsonify, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import logging

from Backend.src.extensions import db # Import the DB Instance
import Backend.src.models as models # Import the Models and Schemas


user_bp = Blueprint('user_bp', __name__)

# -----User Routes-----

# Deserialize the JSON Data and Validate using Schema
user_schema = models.user.UserSchema()

# Create a new user in RDS
# POST /Users/Create
@user_bp.route('/users', methods=['POST'])
def post_user():
    """
    Summary: Create a new user and add it to the database.
    
    Payload: JSON object with the following fields:
        - name: str, required
        - email: str, required
        - username: str, required
        - gender: str, required
        - age: int, required
        
        
    Returns:
        str: A message indicating the success or failure of the user creation.
        Returs standard response codes (see above):
    """

    
    try:
        
        # Get the data from the request body
        data = request.get_json()

        # Check if the user already exists - Filter by email
        existing_user = models.user.User.query.filter_by(email=data.get('email')).first()
        if existing_user is not None:
            raise ValidationError("User with this Email already exists.")
        

        # Extract the values from the data
        user = user_schema.load(data)
        
        # Add the new user to the session
        db.session.add(user)
        # Commit the changes to the database
        db.session.commit()
        
        return jsonify({"Success":"User created successfully!"}), 201
    
    # Validation Error Spawned from Schema
    except ValidationError as e:
        return jsonify({"error": "Validation error occurred.", "details": str(e)}), 400

    except SQLAlchemyError as e:
        
        # Rollback the session in case of an error, and return the error
        db.session.rollback()
        return jsonify({"error": "Database error occurred.", "details": str(e)}), 500
    
    except Exception as e:
        
        # Unexpected error, return Details back
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500


# Get user by Email from DB
# GET /Users
# TODO: Test this Route
@user_bp.route('/users/', methods=['GET'])
def get_user():
    """
    Summary: Get a user by Email
    
    Parameters:
        email (str): The Email of the user.
        
    Returns:
        JSON: The user object.
        
    """
    
    try:
        # Get the data from the request body and Parse
        data = request.get_json()
        email = data.get('email')
        print(f"Email: {email}")
        
        # Get the user by Email from DB
        user = models.user.User.query.filter_by(email=email).first()
        
        # If the user is not found, return a 404
        if user is None:
            return jsonify({"error": "User not found."}), 404
        
    # Catch any unexpected errors
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500
    
       
    # Return the user as JSON Response with 200 Status Code
    return jsonify(user_schema.dump(user)), 200



# UPDATE User by Email
# PUT /Users
# TODO: Test this Route
@user_bp.route('/users', methods=['PUT'])
def update_user():
    """
    Summary: Update a user by Email.
    
    Payload: JSON object with the following fields:
        - email: str, required
         - ... All other fields are optional
        
    """
    try:
        
        # Retrieve JSON Payload - User Data
        user_data = request.get_json()
        
        user_email = user_data.get('email')
        
        # Check if the user already exists - Filter by email
        user = models.user.User.query.filter_by(email=user_email).first()
        if user is None:
            raise ValidationError("User with this Email does not exist.")
        
         # Deserialize the JSON Data
        validated_user_data = user_schema.load(user_data,partial=True)

        
        # Update User Data with New User Data, Excluding the Email and ID
        # Only Updates Values Sent in payload with Validated Data (Not None)
        for field, value in validated_user_data.items():
            if field != 'email' and field != 'id' and value is not None:
                setattr(user, field, value)
            
        # Commit the changes to the database
        db.session.commit()
        
        
        # Serialize and return the updated user
        updated_user_data = user_schema.dump(user)
        return jsonify({"success": "User updated successfully.", "user": updated_user_data}), 200



    except ValidationError as e:
        return jsonify({"error": "Validation error occurred.", "details": e.messages}), 400

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred.", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500
    
    # Update User Data with New User Data
    # Not Creating a New User, but Updating the Existing User
    
    
    
# DELETE User by Email
# DELETE /Users
# TODO: Test this Rout
@user_bp.route('/users', methods=['DELETE'])
def delete_user():
    """
    Summary: Delete a user by Email.
    
    Payload: JSON object with the following fields:
        - email: str, required
        
    Returns:
        str: A message indicating the success or failure of the user deletion.
        Returns standard response codes (see above):
    """
    
    try:
        
        # Retrieve JSON Payload - User Data
        user_data = request.get_json()
        
        # Deserialize the JSON Data
        validated_user_data = user_schema.load(user_data)
        
        # Get the user by Email from DB
        user = models.user.User.query.filter_by(email=validated_user_data['email']).first()
        
        # If the user is not found, return a 404
        if not user:
            return jsonify({"error": "User not found."}), 404
        
        # Delete the user from the session
        db.session.delete(user)
        # Commit the changes to the database
        db.session.commit()
        
        return jsonify({"success": "User deleted successfully."}), 200
    
    except ValidationError as e:
        return jsonify({"error": "Validation error occurred.", "details": e.messages}), 400

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred.", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500
    