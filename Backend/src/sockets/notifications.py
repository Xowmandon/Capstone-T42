# Author: Joshua Ferguson

from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room

# WIP
class NotificationNamespace(Namespace):
     def on_connect(self):
         pass