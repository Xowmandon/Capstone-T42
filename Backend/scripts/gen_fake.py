# Author: Joshua Ferguson
# Script for Generating Fake Profiles to Demo Matching and Swiping

import asyncio
import random
from faker import Faker
import os, sys
import logging


# Import DB and Marshmallow Instances
from Backend import app
from Backend.src import services
from Backend.src.extensions import db, ma
from Backend.src.models.user import UserSchema
import Backend.src.routes as routes

# Import the Models and Schemas

#from src.models import User, Match, Swipe, Message
import Backend.src.models as models
from Backend.src.services import swipe_pool_service

user_schema = models.user.UserSchema()
match_schema = models.match.MatchSchema()
swipe_schema = models.swipe.SwipeSchema()


message_schema = models.message.MessageSchema()
message_schema_nested = models.message.MessageSchemaNested()


class GenFake:
    
    def __init__(self):
        """Initialize Faker and logging."""
        Faker.seed(random.randint(0, 1000))
        self.fake = Faker()

        log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs', 'fake_profiles.log'))
        logging.basicConfig(filename=log_file_path, level=logging.INFO)

    def gen_fake_user(self):
        """Generate a single fake user."""
        
        with app.app.app_context():
            user = models.user.User.create_user(
                name=self.fake.name(),
                email=(self.fake.text(max_nb_chars=5) + "_" + self.fake.unique.email()),
                password=self.fake.password(length=12),
            )
            user.fake = True
            user.gender = self.fake.random_element(elements=('male','female'))
            user.age = random.randint(18, 24)
            user.bio = self.fake.text(max_nb_chars=200)
            user.city = "reno"
            user.state_code = "NV"
            
            # Update DB with User Updates
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)
            logging.info(f"✅ Fake user {user} added to DB")
        return user
        

    def gen_fake_dating_preference(self, user_id):
        """Generate fake dating preferences for a user."""
        return models.datingPreference.DatingPreference(
            user_id=user_id,
            interested_in=self.fake.random_element(elements=('male','female','any')),
            age_preference_lower=random.randint(18, 22),
            age_preference_upper=random.randint(20, 24),
        )

    def gen_fake_swipe_pool(self, user_id,limit=20):
        """Generate a fake swipe pool for a user."""
        pool_gen = swipe_pool_service.SwipePoolService()
        pool = pool_gen.generate_swipe_pool(user_id=user_id, limit=limit)
        return pool

    def get_fake_users(self):
        """Retrieve all fake users from the database."""
        return models.user.User.query.filter_by(fake=True).all()

    def get_two_fake_users(self):
        """Retrieve two unique fake users for matchmaking."""
        return tuple(random.sample(self.get_fake_users(), 2))

    def is_matched(self, user1, user2):
        """Check if two users are already matched."""
        return models.match.Match.query.filter(
            ((models.match.Match.matcher == user1.id) & (models.match.Match.matchee == user2.id)) |
            ((models.match.Match.matcher == user2.id) & (models.match.Match.matchee == user1.id))
        ).first() is not None

    def gen_fake_match(self, matcher, matchee):
        """Generate a fake match between two fake users."""
        if not self.is_matched(matcher, matchee):
            return models.match.Match(matcher=matcher.id, matchee=matchee.id, match_date=self.fake.date_time())
        return None

    def gen_fake_swipe(self, swiper, swipee):
        """Generate a fake swipe event between two fake users."""
        return models.swipe.Swipe(
            swiper=swiper.id,
            swipee=swipee.id,
            swipe_result= self.fake.random_int(min=0, max=2),
            swipe_date=self.fake.date_time()
        )

    def gen_fake_message(self, sender, receiver):
        """Generate a fake chat message."""
        return models.message.Message(
            messager=sender.id,
            messagee=receiver.id,
            message_content=self.fake.text(max_nb_chars=200),
            message_date=self.fake.date_time()
        )

    def gen_num_fake_users(self, num_users=100):
        """Generate a batch of fake users."""
        return [self.gen_fake_user() for _ in range(num_users)]

    def write_users_to_csv(self, users):
        """Generate fake users and store them in a CSV and DB."""
        
        # Save users to CSV
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs', 'fake_users.csv'))
        with open(csv_path, 'a') as f:
            for user in users:
                f.write(f"{user}, \n")
        
        print(f"✅ Fake users saved to CSV at {csv_path}")

# CLI Execution
if __name__ == '__main__':
    Generator = GenFake()

    if "--gen-fake-users" in sys.argv:
        with app.app.app_context():
            fake_users = Generator.gen_num_fake_users(5)
            dating_prefs = [Generator.gen_fake_dating_preference(user.id) for user in fake_users]
            db.session.add_all(dating_prefs)
            db.session.commit()
            for pref in dating_prefs:
                db.session.refresh(pref)
            Generator.write_users_to_csv(fake_users)
            ex_swipe_pool = Generator.gen_fake_swipe_pool(fake_users[0].id)
            #control_ex = Generator.gen_fake_swipe_pool("49c4420a-d30a-4b2e-b5bd-0d36ca24ae37")
            
            print("User for Swipe Pool: ", UserSchema().dump(fake_users[0]))
            # PRetty Print Json of Swipe Pool
            print("Swipe Pool: ", ex_swipe_pool)

            #print("Control Swipe Pool: ", control_ex)

    if "--gen-fake-matches" in sys.argv:
        with db.session.no_autoflush:
            matches = []
            for _ in range(25):
                user1, user2 = Generator.get_two_fake_users()
                match = Generator.gen_fake_match(user1, user2)
                if match:
                    matches.append(match)
            db.session.add_all(matches)
        db.session.commit()

    print("✅ Fake data generation complete!")
