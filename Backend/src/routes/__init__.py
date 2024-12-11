from flask import Blueprint


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

#app = Blueprint('app', __name__)
