
from flask import request
from Backend.src.extensions import socketio

connected_users = {}

@socketio.on('connect')
def handle_connect():
    # Assuming the client sends its email upon connection
    email = request.args.get('email')
    if email:
        connected_users[email] = request.sid
    print(f"User {email} connected with session ID {request.sid}")


@socketio.on('disconnect')
def handle_disconnect():
    
    # logger.info("A client disconnected.")
    print(f"User {request.args.get('email')} disconnected.")
    connected_users.pop(request.args.get('email'))
    

