from flask import request

# Middleware - Log and Validate Requests

#@app.before_request
def before_request():
    """
    This function runs before each request.
    Logging the request method, path, and body.
    Validating Request Body and Headers.
    """
    # Log the request method, path, and body
    # TODO - Implement logging
    pass