
from datetime import datetime, timezone
from random import randint
from time import sleep
from openai import OpenAI
from typing import List

import Backend.src.models as models
from Backend.src.utils import EnvManager

# Load Environment Variables
EnvMan = EnvManager()

class LLMPrompts:
    """
    Class to manage LLM prompts for generating user bios and replies.
    """
    def __init__(self):
        
        self.BIO_PROMPT_TEMPLATE = """
            You are a professional copywriter crafting dating‐app bios for A Variety of Individuals. 
            Write a Brief bio or About-Me (450 Char Max) for **User Profile:** {user_profile}:
            - Could be interepreted as Gender Neutral
            - Highlights a couple of genuine (Randomly Generated) interests or hobbies  
            - Shows a dash of personality or humor  
            - COULD End with a light invitation to chat or explore common ground
            - Base the bio off of a perosn archetype like     
                "Creative Maker",
                "Fitness Guru",
                "Foodie Explorer",
                "Music Aficionado",
                "Tech Enthusiast",
                "Bookworm Intellectual",
                "Chill Homebody",
                "Social Butterfly",
                "World Traveler",
                "Environmental Advocate",
            - Make your own archetypes, but make sure they are unique and not generic
            - DO NOT Base the Bio off of "Adventure and Quirky"
            **Note:**
            - Uniquely tailored to the user’s profile, assume and expand upon them based on the profile
            - Introduce Entropy and Randoness into the bio, especially the intro
            - Avoid generic phrases like “I love to travel” or “I enjoy good food.”
            - Use a light-hearted, flirty tone, but not overly cheesy or cliche.
            - JUST RESPOND WITH THE BIO, DO NOT ADD ANYTHING ELSE, DO NOT ASK ANY QUESTIONS to confirm instructions
            """
            
        self.REPLY_PROMPT_TEMPLATE = """
            You are a witty and empathetic conversational partner helping a User reply to messages on a dating app. 
            Use the following:

            • **User Profile: (keys:values)** {user_profile}  
            • **Conversation History (Each Msg on it's own Line):**  
            {conversation_history}  
            • **Latest Incoming Message (from the other User):** "{incoming_message}"

            **Task:** Write a 1–3 sentence response that  
            1. Acknowledges something from the incoming message.  
            2. Shows genuine interest or shares a relatable anecdote.  
            3. Ends with a light-hearted question or invitation to keep the conversation going.  

            Keep the tone upbeat, authentic, and flirty—but not over-the-top. Avoid generic responses like “Cool!” or “That’s nice.”  
            Make it feel like a natural continuation of the conversation.  
            **Notes:** 
            Use the user profile and conversation history to inform your response.
            JUST REPLY WITH THE MESSAGE, DO NOT ADD ANYTHING ELSE, DO NOT ASK ANY QUESTIONS to confirm instructions
            Keep the response short and sweet (Keep a SImiliar length to the conversation history, not significantly different), 
            like a text message, or one that would feel natural in a dating App. 
            RESPOND IN THE FIRST PERSON, AS IF YOU ARE THE USER, Natural
            """
        self.GAME_REPLY_PROMPT_TEMPLATE = """
            You are an intelligent and strategic game-playing assistant that communicates in JSON-based game messages exchanged between two users. You are helping the user play a game of **Tic-Tac-Toe** against another person.

            The game is played using **JSON-encoded messages**, and each move is passed as a gameState. You always respond with a new `game_state` that reflects your move.

            Here’s what you’ll receive:
            - The full current gameState (as JSON string).
            - You’ll be Player 2 (`O`) and your task is to play a valid move.
            - The board is a list of 9 elements representing positions 0–8:
            - ["X", "", "", "", "", "", "", "", ""] means 'X' is at position 0.
            - Do NOT change previous moves.
            - Play your move by placing `"O"` in the first available empty spot that’s not already taken.
            - ONLY RETURN the updated JSON-encoded `game_state` string inside the `"content"` field, like this:

            **BELOW IS THE JSON(Interpret Double Curly as Single Curly, DO NOT ADD ```JSON or any Wrapping, Just the PURE JSON )**
            
            
            {{
            "game_name": "TicTacToe",
            "game_state": "{{\"currentState\":{{\"result\":\"\",\"winner\":\"\",\"boardState\":[\"X\", \"O\", \"\", \"\", \"\", \"\", \"\", \"\", \"\"]}},\"startingData\":{{\"nameP1\":\"Bob\",\"nameP2\":\"Mary\",\"playerNum\":1}}}}"
            }}
            
            ** END JSON**
            
            **LAST MOVE/ Current Game State:**
            {last_move}
            
            **NOTE:**
            - Just return the JSON string with no additional text or explanation.
            - Do not add any extra information or context.
            - Do not ask any questions to confirm instructions.
        
        """

class LLMService:
    """LLM Agent Service for generating user bios and messages using the OpenAI API."""
    def __init__(self):
        api_key = EnvMan.load_env_var("OPENAI_API_KEY")
        self.client = OpenAI(
            api_key= api_key,
            base_url="https://api.openai.com/v1",
            timeout=10,
   
        )
        self.prompts = LLMPrompts()
        
    def gen_client_completion(self, prompt: str) -> str:
        """
        Generate a completion using the OpenAI API and Prompt
        """
        resp = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return resp.choices[0].message.content

    def gen_bio_llm(self, user_profile: {str, str}, prompt: str) -> str:
        """
        Generate a bio using the context-aware prompt.
        """
        prompt = self.prompts.BIO_PROMPT_TEMPLATE.format(
            user_profile=user_profile,
        )
        return self.gen_client_completion(prompt)

    def reply_to_message(self,
                         user_profile: {str, str},
                         conversation_history: List[str],
                         incoming_message: str,
                         kind: str = "text",
                         ) -> str:
        """
        Generate a 1–3 sentence reply using the context-aware prompt.
        """
         # Convert user_profile dictionary to a string
        user_profile_str = ", ".join(f"{key}: {value}" for key, value in user_profile.items())

        # Convert conversation history list to a formatted string
        conversation_history_str = "\n".join(conversation_history)
            
            
        # Debugging: Print the inputs
        print(f"Messager Profile: {user_profile}")
        print(f"Formatted User Profile: {user_profile_str}")
        print(f"Conversation History: {conversation_history_str}")
        print(f"Incoming Message: {incoming_message}")
        
        if kind == "game":
            prompt = self.prompts.GAME_REPLY_PROMPT_TEMPLATE.format(
                last_move=incoming_message
            )
        else:
            prompt =  self.prompts.REPLY_PROMPT_TEMPLATE.format(
                user_profile=user_profile_str,
                conversation_history=conversation_history_str,
                incoming_message=incoming_message,
            )
        print(f"Message Prompt: {prompt}")
        return self.gen_client_completion(prompt)
   
    def reply_needed(self, match,main_user_id) -> str:
        """Check if a reply is needed for a conversation with the main user."""
       
        # Fetch the last message in the match
        match_helper = models.match.MatchModelHelper(match.id)
        lst_msg =  match_helper.get_last_message()    
        if not lst_msg:
            print(f"match ID {match.id} - No messages found")
            return None
        
        # Check if the last message is from the main user
        #main_user_id = "000519.f1637da8f2c14d39b61d3653a8797532.1310"
        messager_id = lst_msg.messager_id
        
         # Check if the last message is from the main user
        if messager_id == main_user_id:
            messager_id = match.matchee_id
        
        # Last Messafe is From Last User
        else:
            print(f"match ID {match.id} - No Reply Needed, Main User is the Messagee")
            return None
        
        # Check if the messager is a fake user
        messagee_id = match.matchee_id if messager_id == match.matcher_id else match.matcher_id
        #messagee_fake = models.user.User.query.filter_by(id=messagee_id).first().is_fake   
        messager_fake = models.user.User.query.filter_by(id=messager_id).first().is_fake
        if not messager_fake:
            print(f"match ID {match.id} - No Reply Needed, Messager is a Real User")
        
        #if not messagee_fake:
            #print(f"match ID {match.id} - No Reply Needed, Messagee is a Real User")
            #return None
         
        return messager_id   
    
    def create_reply(self, match,main_user_id,messager_id=None,check_need_reply=True):
        """Create Reply for a Conversation With Main User"""
    
        # Check if a reply is needed
        if check_need_reply:
            messager_id = self.reply_needed(match,main_user_id)
            if not messager_id:
                print("Create_reply Failed: No reply needed.")
                return
        
        # Get Other User's Information
        messager = models.user.User.query.filter_by(id=messager_id).first()
        
        
        if messager is None:
            print(f"Messager with ID {messager_id} not found.")
            
       # Construct Messager_profile for LLM Context, Avoiding None Values
        messager_profile = {
            "age": str(messager.age) if messager.age else "Unknown age",
            "name": messager.name if messager.name else "Unknown name",
            "gender": messager.gender if messager.gender else "Unknown gender",
            "state": messager.state if messager.state else "Unknown state",
            "city": messager.city if messager.city else "Unknown city",
            "bio": messager.bio if messager.bio else "No bio available",
        }
        
        match_helper = models.match.MatchModelHelper(match.id)
        conversation_hist = match_helper.get_messages(limit=5)["messages"]
        conversation_hist = [msg.message_content for msg in conversation_hist]
        last_msg = match_helper.get_last_message()
        # Generate a reply using the LLM service
        new_message = models.message.Message(
            match_id= match.id,
            messager_id = messager_id ,
            message_content = self.reply_to_message(
                user_profile = messager_profile,
                conversation_history= conversation_hist,
                incoming_message = last_msg.message_content,
                kind=last_msg.kind,
            ),
            kind= last_msg.kind,
            message_date= datetime.now(timezone.utc),
        )
        
        # Add the new message to the database
        from Backend.src.extensions import db
        db.session.add(new_message)
        db.session.commit()
        
        print(f"Reply created for match ID {match.id} - Message ID: {new_message.id}")
        return new_message
        
        
    def auto_reply(self,user_id,timeout_mins=10):
        
        """Enable LLM auto-reply for match Conversations"""
        
        #Timeout for the loop
        start_time = datetime.now()
        timeout_seconds = (60 * timeout_mins)  # Set a timeout for the loop (e.g., 60 seconds)

        while True:
            # Check for new messages and Matches Every 10 Seconds
            sleep(10)
            
            # Fetch all matches for the user
            matches = models.match.Match.query.filter(
                (models.match.Match.matcher_id == user_id) | (models.match.Match.matchee_id == user_id)
                ).all()
            
            for match in matches:
                
                # Check if a reply is needed
                # If no reply is needed (Messager_id == user_id), 
                # continue to the next match
                messager_id = self.reply_needed(match, user_id)
                if not messager_id:
                    continue
                
                # Reply is Needed, Wait Randomly Between 5 and 10 Seconds
                # to Prevent Overlapping Replies
                # This is to simulate human behavior and Avoid spamming
                sleep(randint(5, 10))
                
                # Create Reply
                new_message = self.create_reply(
                    match=match,
                    main_user_id=user_id,
                    messager_id=messager_id,
                    check_need_reply=False
                )
                    
                print(f"Reply created for match ID {match.id} - Message ID: {new_message.id}")

            # Exit condition: Check if the timeout has been reached
            elapsed_time = (datetime.now() - start_time).total_seconds()
            if elapsed_time > timeout_seconds:
                print("Exiting auto-reply loop due to timeout.")
                break
   