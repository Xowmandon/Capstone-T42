
from flask import request, jsonify, current_app

import Backend.src.models as models # Import the Models and Schemas
#from src.routes import app # Blueprin
from Backend.src.extensions import db # Import the DB Instance

#from Backend.app import app


# BUG: Not Picking up the Routes of the App
def generate_route_metadata():
    
    routes = [] # Routes Represented as a List of Dictionaries
    
    # Iterate over all routes in the app and add them to the routes list
    with current_app.app_context():
        for rule in current_app.url_map.iter_rules():
            routes.append({
                "path": rule.rule, # Get the path of the route
                "methods": list(rule.methods) # Get the methods allowed for the route
            })
    return routes


#
def generate_model_metadata():
    """
    Generate model metadata as a list of dictionaries.
    Returns:
        list: List of dictionaries with model names and fields.
    """
    model_columns = []
    for model_name, model in models.__dict__.items():
        if isinstance(model, type) and issubclass(model, db.Model):
            columns = [column.name for column in model.__table__.columns]
            model_columns.append({
                "model_name": model_name,
                "fields": columns
            })
    return model_columns