import os
import hashlib
from dotenv import load_dotenv
import argparse
import sys


# Add the parent directory to the system path
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from Backend.app import app
from Backend.src.extensions import db
from Backend.src.utils import EnvManager

# Create all tables in the database, according to the models defined
def create_all_tables():
    with app.app_context():
        db.create_all()
        print("All tables created successfully.")

# Drop all tables in the database
def drop_all_tables():
    with app.app_context():
        db.drop_all()
        # Validate If Admin wants to drop all tables
        if input("Are you sure you want to drop all tables? (y/n): ").strip().lower() == 'y':
            db.drop_all()
            print("All tables dropped successfully.")
        else:
            print("Operation cancelled.")

# Hash the key using SHA-256
def hash_key(key):
    return hashlib.sha256(key.encode()).hexdigest()

def validate_key(provided_key, expected_hashed_key):
    return hash_key(provided_key) == expected_hashed_key

def main(action):
    # The hashed value of DB_UTILS_KEY
    expected_hashed_key = '247ebb3b36442b1d23264bc0c91d886bdfdd582f9e803cbebe26bfe1d3b8c043'
    
    # Get the key from the environment variable and hash it
    provided_key = EnvManager().load_env_var('DB_UTILS_KEY')
    
    if validate_key(provided_key, expected_hashed_key):
        if action == 'create':
            create_all_tables()
            print("All tables created successfully.") # TODO: Log this message 
        elif action == 'drop':
            if input("Are you sure you want to drop all tables? (y/n): ").strip().lower() == 'y':
                drop_all_tables()
                print("All tables dropped successfully.") # TODO: Log this message
        else:
            print("Invalid action. Please enter 'create' or 'drop'.")
    else:
        print("Unauthorized access. Set the correct DB_UTILS_KEY environment variable.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Database Utilities')
    parser.add_argument('--action', nargs='?', choices=['create', 'drop'], help="Action to perform: 'create' to create all tables or 'drop' to drop all tables")

    args = parser.parse_args()
    action = args.action if args.action else input("Enter 'create' to create all tables or 'drop' to drop all tables: ").strip().lower()
    main(action)