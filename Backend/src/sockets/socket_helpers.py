# Author: Joshua Ferguson

from Backend.src.services.auth_service import get_user_from_token
   
def auth_connecting_user(auth_request_header):
    """
    Authenticates the connecting user based on the provided authorization header.

    Args:
        auth_request_header (str): The authorization header containing the bearer token.

    Returns:
        int or None: The ID of the authenticated user if the token is valid, None otherwise.
    """
    if not auth_request_header:
        print("Missing Authorization header. Connection refused.")
        return None

    # Extract Bearer Token
    token = auth_request_header.replace("Bearer ", "").strip()
    user = get_user_from_token(token)
    if user is None:
        print("User not found or Invalid Token. Connection refused.")
        return None

    return user.id


def standardize_room_name(room_name, prefix):
    """
    Adds a prefix to a room name.

    Args:
        room_name (str): The name of the room.
        prefix (str): The prefix to add to the room name.

    Returns:
        str: The room name with the prefix added.
    """
    return f"{prefix}_{str(room_name)}"

def gen_match_room_name(match_id):
    """
    Generates a match room name based on the match ID with "match_" prefix.
    """
    return standardize_room_name(match_id, "match")

#TOOD: Implement Game Room Name Generation Function and WEbsocket Namespace
#def gen_game_room_name(game_id):
   # """
   # Generates a game room name based on the game ID with "game_" prefix.
    #"""
    #return standardize_room_name(game_id, "game")