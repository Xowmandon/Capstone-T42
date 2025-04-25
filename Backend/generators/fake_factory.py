
from datetime import datetime, time, timezone
from random import choice, randint
from time import sleep
from typing import List
from faker import Faker
from flask_jwt_extended import create_access_token
from openai import OpenAI
import requests

from Backend import app
import Backend.src.models as models
from Backend.src.extensions import (
    db, 
    llm_service, 
    media_storage_service, 
    AWS_MEDIA_MAIN_PHOTO_FOLDER, 
    AWS_MEDIA_USER_PHOTO_FOLDER,
)

from Backend.generators.User_factory import UserFactory
from Backend.generators.DatingPreferences_factory import DatingPreferencesFactory
from Backend.generators.photo_factory import PhotoFactory


fake = Faker()

fake.seed_instance(16)



class FactoryManager:
    def __init__(self):
        self.jwts = []
        self.user_ids = []
        self.match_ids = []
        self.fake = Faker()
        self.fake.seed_instance(16)
        self.page = 1
    
    # Add User IDs to the list
    def add_user_ids(self, user_ids: List[str]):
        for user_id in user_ids:
            if not isinstance(user_id, str):
                raise ValueError("User ID must be a string.")
            if not user_id:
                raise ValueError("User ID cannot be empty.")
            if user_id in self.user_ids:
                raise ValueError(f"User ID {user_id} already exists in the list.")
            self.user_ids.append(user_id)
            self.add_jwt(user_id)


    # Generate JWTs for the user IDs
    def add_jwt(self,user_id) -> str:
   
        if not user_id:
            raise ValueError("No user IDs provided.")
    
        access_token = create_access_token(identity=user_id)
        self.jwts.append(access_token)
      
    def gen_fake_swipe(self,swiper,swipee,result): 
        """Generate a fake swipe between two users."""
        new_swipe = models.swipe.Swipe(
            swiper_id=swiper,
            swipee_id=swipee,
            swipe_result=result
        )
        db.session.add(new_swipe)
        db.session.commit()

    def create_swipable_user(self, user_id: str,swipe_result=None):
        
        # fetch existing user
        existing_user = models.user.User.query.filter_by(id=user_id).first()
        if not existing_user:
            print("Main Test User Not Found...Exiting")
            exit(1)

        # fetch their preferences
        test_user_prefs = models.datingPreference.DatingPreference.query.filter_by(
            user_id=existing_user.id
        ).first()
        if not test_user_prefs:
            print("Test User Preferences Not Found...Exiting")
            exit(1)
        

        # create new user, overriding location fields and attaching existing prefs
        new_user = UserFactory.create(
            city=existing_user.city,
            state=existing_user.state,
            gender=test_user_prefs.interested_in,
            age=test_user_prefs.age_preference_lower + 1,
            country_code=existing_user.country_code,
        )
        
        # Create a new DatingPreference object with the same user_id as the New User
        custom_built_prefs = DatingPreferencesFactory.create(
            user_id=new_user.id,
            interested_in=existing_user.gender,
            age_preference_lower=existing_user.age ,
            age_preference_upper=existing_user.age + 2,
        )

        
        # Print Existing and New User Details Side by Side for Validation

        # Existing user
        print("Validating Existing User and New User Creation")
        print("=========================================")
        print("Existing User:")
        print(f"  ID     : {existing_user.id}")
        print(f"  Name   : {existing_user.name}")
        print(f"  Gender : {existing_user.gender}")
        print(f"  Age    : {existing_user.age}")
        print(f"  Location: {existing_user.city}, {existing_user.state}, {existing_user.country_code}")
        print(f"  Interested In        : {test_user_prefs.interested_in}")
        print(f"  Age Preference Lower  : {test_user_prefs.age_preference_lower}")
        print(f"  Age Preference Upper  : {test_user_prefs.age_preference_upper}")
        print(f"  Bio    : {existing_user.bio}")
        print()

        # New user
        print("\nNew User:")
        print(f"  ID                   : {new_user.id}")
        print(f"  Name                 : {new_user.name}")
        print(f"  Gender               : {new_user.gender}")
        print(f"  Age                  : {new_user.age}")
        print(f"  Location             : {new_user.city}, {new_user.state}, {new_user.country_code}")
        print(f"  Interested In        : {custom_built_prefs.interested_in}")
        print(f"  Age Preference Lower  : {custom_built_prefs.age_preference_lower}")
        print(f"  Age Preference Upper  : {custom_built_prefs.age_preference_upper}")
        
        print(f"  Bio        : {new_user.bio}")
        print("=========================================")
        

        # Add User IDs to the list
        self.add_user_ids([new_user.id])
        
        # Generate a fake swipe between the existing user and the new user
        if swipe_result is None:
            return new_user.id
        
        
        self.gen_fake_swipe(new_user.id, existing_user.id,result=swipe_result)
        
        return new_user.id
 
    def create_match(self, user1_id: str, user2_id: str):
        """Create a match between two users."""
        if not user1_id or not user2_id:
            raise ValueError("User IDs cannot be empty.")
        
        # Check if the match already exists
        existing_match = models.match.Match.query.filter(
            (models.match.Match.matcher == user1_id) & (models.match.Match.matchee == user2_id)
        ).first()
        
        if existing_match:
            print(f"Match already exists between {user1_id} and {user2_id}.")
            return
        
        # Create a new match
        new_match = models.match.Match(
            matcher=user1_id,
            matchee=user2_id,
        )
        db.session.add(new_match)
        db.session.commit()
        self.match_ids.append(new_match.id)
        print(f"Match created between {user1_id} and {user2_id}.")
         
    def create_photos(self, is_main_photo, style, N_tot=10):
        """Create main photos for users."""
        photo_factory = PhotoFactory()
        
        if is_main_photo:
            print("Creating Main Photos...")
            file_paths = photo_factory.gen_photos(
                is_main_photo=is_main_photo,
                style=style,
                is_fake_photo=True,
                seed=None,
                count=N_tot
            )
            return file_paths
        else:
            print("Bulk Creating Gallery Photos for User...")
            
            if len(self.user_ids) == 0:
                raise ValueError("No user IDs provided.")
            if N_tot <= 0:
                raise ValueError("N_tot must be greater than 0.")
            
            
            # Each User Gets N_tot Photos
            for user_id in self.user_ids:
                # Create a new user photo
                photos = photo_factory.gen_gallery_photos(
                    query=style, 
                    per_page=N_tot, # Photos Per User
                    api="pexels",
                    page=self.page,
                )
                
                if len(photos) != (N_tot):
                    print(f"Not enough photos generated for user {user_id}.")
                    print(f"Generated {len(photos)} photos, expected {N_tot}.")
                    continue    
                
                db_urls = [
                    _photo.url for _photo in models.photo.UserPhoto.query.filter_by(user_id=user_id).all()
                ]
                if set([photo.url for photo in photos]) & set(db_urls):
                    print(f"Duplicate URLs found in DB for user {user_id}.")
                    # Skip this user and Photos
                    continue
                
                # Add the user ID to each photo
                # and add it to the session DB
                for photo in photos: 
                    
                    photo.user_id = user_id
                    
                    try:
                        db.session.add(photo)
                    except Exception as e:
                        print(f"Error adding Gallery photo for user {user_id}: {e}")
                        continue
                    
                # Add the new user photo to the session
                db.session.add_all(photos)
                db.session.commit()
                
                # Increment Page to Avoid Duplicates
                # and to get new photos
                self.page += 1
                        
                print(f"Gallery photos created for user {user_id}")
                print(f"URLS: " + str([photo.url for photo in photos]))
                print(f"LENGTH: {len(photos)}")
        
            print("Final Page: " + str(page))
            return page
                
    def populate_main_photos(self,file_paths, file_names, user_ids):
        """Populate the main photos for a user."""
        # Fetch the user

        urls = []
        
        for idx,(file_path,user_id) in enumerate(zip(file_paths, user_ids)):
            
            user = models.user.User.query.filter_by(id=user_id).first()
            if not user:
                print(f"User with ID {user_id} not found.")
                return
            
            files = {
                "profile_picture": open(file_path, "rb"),
            }
            
            url = media_storage_service.upload_user_photo(
                file=file_path,
                file_name=file_names[idx],
                user_id=user_id,
                folder=AWS_MEDIA_MAIN_PHOTO_FOLDER, 
                is_main_photo=True,
                content_type="image/svg+xml",
            )
            
            if url:
                print(f"Main photo for user {user_id} updated successfully.")
                urls.append(url)
            else:
                print(f"Failed to populate main photo for user {user_id}.")  
        
        return urls

class CLIGenerator:
    def __init__(self, factory_manager: FactoryManager):
        self.factory_manager = factory_manager
        self.page = None
        self.commands = {
            "help": self.display_help,
            "create --users": self.handle_create_swipable_users,
            "create --matches": self.handle_create_matches,
            "show --jwts": self.handle_show_jwts,
            "push --main-photos": self.handle_populate_main_photos,
            "create --main-photos": self.handle_create_main_photos,          
            "create --gallery-photos": self.handle_create_gallery_photos,       
        }

   
    def display_help(self):
            """Display available commands."""
            print("Available commands:")
            print()
            print("  stream --users                - Create a Creation Stream of users (Profile, Main & Gallery Photos)")
            print("  create --users                - Create n swipable users with PENDING state")
            print("  create --matches              - Create n matches between users")
            print("  create --reply                - Create LLM Reply For MatchID")
            print("  create --main-photos          - Save Main Photos to Local Storage")
            print("  create --gallery-photos       - Save Gallery Photos to Local Storage") 
            print("  push --main-photos            - Populate main photos for users")
            print("  show --gen-matches            - Show generated match IDs")
            print("  show --user-matches           - Show matches for a Main user")
            print("  show --users                  - Show user IDs")
            print("  show --jwts                   - Show generated JWTs")
            print("  enable --auto-reply           - Enable LLM auto-reply for matches")
            print("  help                          - Show this help message")
            print("  exit                          - Exit the CLI")

    def handle_create_swipable_users(self):
        """Handle the creation of swipable users."""
        try:
            count = int(input("Enter the number of swipable users to create: ").strip())
            result = input("Enter the swipe result (y for PENDING, r for Rejected, a for Accepted): ").strip().lower()
            if result == "y":
                swipe_result = "PENDING"
            elif result == "r":
                swipe_result = "REJECTED"
            elif result == "a":
                swipe_result = "ACCEPTED"
            else:
                swipe_result = None
                
            print(f"Creating {count} swipable users...")
            existing_user_id = "000519.f1637da8f2c14d39b61d3653a8797532.1310"
            
            for _ in range(count):
                self.factory_manager.create_swipable_user(existing_user_id, swipe_result=swipe_result)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def handle_create_matches(self,user1_id):
        """Handle the creation of matches between users."""
        try:
            count = int(input("Enter the number of matches to create: ").strip())
            
            print(f"Creating {count} matches...")
            if len(factory_manager.user_ids) < 2:
                print("Not enough users to create matches. Please create more swipable users first.")
                return
            match_ids = []
            for i in range(count):
                user2_id = self.factory_manager.user_ids[(i + 1) % len(factory_manager.user_ids)]
                self.factory_manager.create_match(user1_id, user2_id)
                match_ids.append((user1_id, user2_id))
            print("\nGenerated Matches:")
            for matcher, matchee in match_ids:
                print(f"Match: {matcher} -> {matchee}")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def handle_create_reply(self,main_user_id):
        """Handle the creation of messages between users."""
        try:
            match_id = input("Enter the match ID for the messages: ").strip()
            if not match_id:
                print("Match ID cannot be empty.")
                return
                
            # Fetch the match
            match = models.match.Match.query.filter_by(id=match_id).first()
            if not match:
                print(f"Match with ID {match_id} not found.")
                return
        
            llm_service.create_reply(match, main_user_id)
            
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred Replying to Message: {e}")

    def handle_show_jwts(self):
        """Display generated JWTs."""
        print("\nGenerated JWTs:")
        for jwt in self.factory_manager.jwts:
            print(jwt)

    def handle_populate_main_photos(self,file_paths,N_tot: int):
        """Populate main photos for users."""
        if file_paths is None:
            print("No file paths provided.")
            print("Please Call create --main-photos to generate file paths.")
            return
        # Check if the number of file paths matches the number of user IDs
        if len(file_paths) < len(self.factory_manager.user_ids):
            print("Number of file paths is Less than number of user IDs.")
            return
        
        responses = self.factory_manager.populate_main_photos(
            file_paths=file_paths, 
            file_names=[f"Fake_main_photo_{i}.svg" for i in range(N_tot)],
            user_ids=factory_manager.user_ids
        )
        
        if responses:
            print("Main photos populated successfully.")
        else:
            print("Failed to populate main photos.")

    def handle_create_main_photos(self):
        """Create main photos for users."""
        # Create main photos for users
        styles = {
            "1": "notionist-neutral",
            "2": "lorelei-neutral",
            "3": "avataaars-neutral",
        }

        print("Choose an avatar style:")
        for num, name in styles.items():
            print(f"{num}. {name}")

        style_choice = input("Enter the # for main photo style (default: 1): ").strip()
        selected_style = styles.get(style_choice, "notionist-neutral")

        file_paths = self.factory_manager.create_photos(style=selected_style,is_main_photo=True)
        if len(file_paths) == 0:
            print("No file paths returned from the photo factory.")
            return
        print("Main photos created successfully.")
        print(f"File Photos: {file_paths}")
        return file_paths
    
    def handle_create_gallery_photos(self):
        """Create gallery photos for users."""
        
        query = input("Enter the query for gallery photos: ").strip()
        total = int(input("Enter the number of gallery photos to create per User Generated: ").strip())
        
        if not query or total <= 0:
            print("Invalid input. Please enter a valid query and number of photos.")
  
        page = self.factory_manager.create_photos(
            is_main_photo=False,
            style=query,
            N_tot=total
        )
        
        print("Gallery photos created successfully.")
        print("Last Page: " + str(page))
        print("=========================================")
        

    def handle_show_user_matches(self,user_id):
        """Display matches for each user."""
        matches = models.match.Match.query.filter(
            (models.match.Match.matcher_id == user_id) | (models.match.Match.matchee_id == user_id)
            ).all()
        
        if matches:
            print(f"Matches for user {user_id}:")
            
            # Display Match Data For User
            for match in matches:
                match_helper = models.match.MatchModelHelper(match.id)
                other_user_id = match.matchee_id if match.matcher_id == user_id else match.matcher_id
                other_user_name = models.user.User.query.filter_by(id=other_user_id).first().name
                lst_msg = match_helper.get_last_message()

                print(f"Match ID: {match.id}, Other User ID: {other_user_id}")
                print(f"Other User Name: {other_user_name}")
                print(f"Last Messager ID: {lst_msg.messager_id if lst_msg else 'No messages yet'}")

            print("Matches displayed successfully.")
            print("=========================================")
        else:
            print(f"No matches found for user {user_id}.")
            


if __name__ == "__main__":
    
    main_user_id = "000519.f1637da8f2c14d39b61d3653a8797532.1310"
    file_paths = []
    
    with app.app.app_context():
        factory_manager = FactoryManager()
        cli_generator = CLIGenerator(factory_manager)
        
        
        # Create the CLI interface
        print("FactoryManager CLI")
        cli_generator.display_help()
        print("=========================================")

        while True:
            # Prompt for user input
            command = input(">> ").strip().lower()
            if command == "exit":
                print("Goodbye!")
                break
            elif command == "help":
                cli_generator.display_help()
            elif command == "create --users":
                cli_generator.handle_create_swipable_users()
            elif command == "create --matches":
                cli_generator.handle_create_matches(main_user_id)
            elif command =="create --reply":
                cli_generator.handle_create_reply(main_user_id)
            elif command =="enable --auto-reply":
               llm_service.auto_reply(main_user_id,timeout_mins=10)
            elif command == "push --main-photos":
                cli_generator.handle_populate_main_photos()
            elif command == "create --main-photos":
                paths = cli_generator.handle_create_main_photos()
                file_paths.extend(paths)
            elif command == "create --gallery-photos":
                cli_generator.handle_create_gallery_photos()
            elif command == "show --jwts":
                cli_generator.handle_show_jwts()
            elif command == "show --gen-matches":
                print("Match IDs:")
                for match_id in factory_manager.match_ids:
                    print(match_id)
                    
            elif command == "show --user-matches":
                cli_generator.handle_show_user_matches(main_user_id)
            elif command == "show --users":
                print("User IDs:")
                for user_id in factory_manager.user_ids:
                    print(user_id)
                    
            elif command == "stream --users":
                # Create a pipeline of users
                count = int(input("Enter the number of users to create: ").strip())
                for _ in range(count):
                    factory_manager.create_swipable_user(
                        main_user_id, 
                        swipe_result=choice(["PENDING", None, None, None])
                    )
                # Print the user IDs
                print(f"User IDs: {factory_manager.user_ids}")
                
                
                # Populate Main Photos for Users
                paths = cli_generator.handle_create_main_photos()
                file_paths.extend(paths)
                print(f"File Paths: {file_paths}")
                cli_generator.handle_populate_main_photos(file_paths,N_tot=len(factory_manager.user_ids))

                # Create Gallery Photos for These Users
                cli_generator.handle_create_gallery_photos()
                
                
            else:
                print("Unknown command. Type 'help' for a list of commands.")