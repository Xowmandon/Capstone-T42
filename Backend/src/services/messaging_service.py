import json
import firebase_admin
from firebase_admin import credentials, messaging

import Backend.src.models as models  # Import the Models and Schemas



class GCPService:
    """
    A service class for interacting with Google Cloud Platform (GCP) services.  
    """
    def __init__(self):
        # Initialize the GCPManager by loading credentials from environment variables
        from Backend.src.extensions import EnvMan
        cred_str = EnvMan.load_env_var("GOOGLE_APPLICATION_CREDENTIALS")
        cred_dict = eval(cred_str.replace("'", '"'))
        if not cred_dict:
            raise ValueError("Google Application Credentials not found.")
        self._credentials = credentials.Certificate(cred_dict)
        self.app = firebase_admin.initialize_app(self._credentials)

    def get_app(self):
        # Initialize and return the Firebase app
        return self.app


def user_to_fcmToken(user_id: str):
    """Convert user_id to FCM token."""
    fcm_token = models.UserFcmToken.query.filter_by(user_id=user_id).first()
    if fcm_token:
        return fcm_token.fcm_token
    else:
        return None

def send_fcm_notification(user_id: str, title: str, body: str, data_payload: dict = None):
    fcm_token = user_to_fcmToken(user_id)
    if not fcm_token:
        raise ValueError("FCM token not found for user.")

    message = messaging.Message(
        token=fcm_token,
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data_payload or {},
    )

    try:
        response = messaging.send(message)
        print(f"\u2705 Successfully sent FCM message: {response}")
    except Exception as e:
        print(f"\u274C FCM error: {e}")
        raise Exception(f"Failed to send FCM message: {e}")

