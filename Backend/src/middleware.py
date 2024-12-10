from flask import request
from src.routes import app

import logging

#-------- Middleware - Log and Validate Requests-------

#logger = logging.getLogger(__name__)

#@app.before_request
def before_request():
    """
    This function runs before each request.
    
    Logging the request method, path, and body.
    Validating Request Body and Headers.
    
    """

    # Log the request method, path, and body
    # TODO: Validate Request Body and Headers
    # TODO: Implement Security Measures
    #logger.info(f"Request Path: {request.path}")
    #logger.info(f"Request Method: {request.method}")
    #logger.info(f"Request Headers: {request.headers}")
    #logger.info(f"Request Body: {request.json}")
    
    pass


#@app.after_request
def after_request():
    """
    This function runs after each request.
    
    Logging the response status code and body.
    """
    