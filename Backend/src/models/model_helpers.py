# Author: Joshua Ferguson

import Backend.src.models as models
from Backend.src.extensions import db
from Backend.src.models.message import MessageSchema

class UserModelHelper:
    
    def __init__(self,user_id):
        self.user_id = user_id

    def get_user_matches(user_id):

        user_matches = models.match.Match.query.filter(
            (models.match.Match.matcher_id == user_id) | (models.match.Match.matchee_id == user_id)
        ).all()
        
        return user_matches
    
    def get_user_matches_ids(self):
        """
        Get the User Matches for the User
        """
        return [match.id for match in self.get_user_matches_()]
    
class MatchModelHelper:
    
    def __init__(self,match_id):
        self.match_id = match_id

    def get_messages(match_id, limit=10, page=1, get_all_messages=False): 
    
        """
        Retrieve messages exchanged between two users in a match.

        Parameters:
        - match: Match object containing user1_id and user2_id.
        - limit: Number of messages per page.
        - page: Page number for pagination.
        - get_all_messages: If True, returns all messages without pagination.

        Returns:
        - Dictionary containing messages and pagination metadata.
        """

        # Filter: Get messages where one user is the sender and the other is the recipient
        #conversation_filter = or_(
            #and_(models.message.Message.messager_id == user1_id, models.message.Message.messagee_id == user2_id),
            #and_(models.message.Message.messager_id == user2_id, models.message.Message.messagee_id == user1_id)
        #)
        
        # Get the messages marked with the match ID
        # ...
        conversation_filter = models.message.Message.match_id == match_id

        conversation_query = (
            db.session.query(models.message.Message)
            .filter(conversation_filter)
            .order_by(models.message.Message.message_date.desc())  # Order by newest first
        )
        
        conversation = conversation_query.all()

        # Fetch all messages if `get_all_messages` is True
        if get_all_messages:
            return {"messages": conversation, "total_messages": len(conversation)}

        # Paginate Results
        paginated_results = conversation_query.paginate(page=page, per_page=limit, error_out=False)

        return {
            "messages": paginated_results.items,  # List of messages on the current page
            "total_messages": paginated_results.total,  # Total messages in the conversation
            "total_pages": paginated_results.pages,  # Total number of pages
            "current_page": paginated_results.page,  # Current page number
            "has_next": paginated_results.has_next,  # Whether there is a next page
            "has_prev": paginated_results.has_prev,  # Whether there is a previous page
        }
        
    def save_message_to_match_chat(self, user_id, message_content):
        """
        Save a message to the database.
        """
        try:
            data_message = models.message.Message(
                match_id=self.match_id,
                messager_id=user_id,
                message_content=message_content
            )
            # Extract the values from the data
            message = MessageSchema().load(data_message)

            # Add the new message to the session
            db.session.add(message)
            # Commit the changes to the database
            db.session.commit()

            return message
        except Exception as e:
            print(f"Error saving message: {str(e)}")
            return None
