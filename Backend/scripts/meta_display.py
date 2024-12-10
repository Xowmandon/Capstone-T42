# This script is used to generate metadata for the routes and models in the application
# The metadata is written to JSON files in the config directory

import Backend.scripts.meta_info as meta
from Backend.app import app
import json
from flask import Response


if __name__ == '__main__':
    
    with app.app_context():
    
        # Retrieve the Routes and Models
        routes_metadata = meta.generate_route_metadata()
        
        # Write the Routes to a Config Files
        with open('./Backend/config/routes.json', 'w') as routes_file:
            json.dump(routes_metadata, routes_file, indent=4)
            print("Routes metadata has been written to ./config/routes.json")
        
    
    # Generate models metadata
    models_metadata = meta.generate_model_metadata()

    # Write to a JSON file
    with open('./Backend/config/models.json', 'w') as models_file:
        json.dump(models_metadata, models_file, indent=4)
        print("Models metadata has been written to ./config/models.json")