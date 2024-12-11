# Websocket Handlers for Getting New Messages
from flask import request, jsonify, Blueprint
import Backend.src.models as models
from Backend.src.extensions import db #socketio

# Generates Room Name for Socket.IO of Two Matching Users in Chat
def generate_room_name(user1_email, user2_email):
    # Generate a consistent room name by sorting the emails alphabetically
    return f"{min(user1_email, user2_email)}-{max(user1_email, user2_email)}"


"""# Handle New Match Event
#@socketio.on('new_swipe')
def handle_swipe_event():
    
     # Fields Allowed to be Updated
    # TODO: Standardize the Fields that can be Updated to a Single Location
    changable_fields = ['swipe_result', 'swipe_date']
     
    # Payload from Request
    data = request.get_json()
    
    # Parse Payload for Emails
    swipe_schema = models.swipe.SwipeSchema()
 
    # Load and Validate the Swipe Payload
    new_swipe = swipe_schema.load(data)
    
    # Both Users Swiped Right, Create a New Match
    if new_swipe.swipe_result == models.swipe.SwipeResult.ACCEPTED:
        return
        
    # Retrieve Swipe from Database
    swipe = models.swipe.Swipe.query.filter_by(swiper=new_swipe.swiper.email, swipee=new_swipe.swipee_email).first()
    
    if swipe is None:
        return jsonify({"error": "Swipe not found."}), 404
    # Update User Data with New User Data, Excluding the Email and ID
    # Only Updates Values Sent in payload with Validated Data (Not None)
     
    for field in changable_fields:
        new_attr = getattr(new_swipe, field)
        if new_attr is not None:
            setattr(swipe, field, new_attr)
            
               
    # Commit the changes to the database
    db.session.commit()
             
    # Return the updated Swipe and a success message
    return jsonify({"success": "Swipe updated successfully.", "Swipe": swipe_schema.dump(swipe)}), 200
"""