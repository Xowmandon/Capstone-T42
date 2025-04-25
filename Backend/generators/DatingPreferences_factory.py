

import uuid
import factory # Factory Boy
import random
from faker import Faker
import bcrypt
import faker


from Backend.src.extensions import db
import Backend.src.models as models



class DatingPreferencesFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.datingPreference.DatingPreference
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
        

    interested_in = factory.LazyFunction(lambda: random.choice(['male', 'female', 'any']))

    #Generate the lower bound
    age_preference_lower = factory.LazyFunction(lambda: random.randint(18, 22))

    # Ensure the upper bound is strictly greater than the lower
    age_preference_upper = factory.LazyAttribute(
        lambda obj: random.randint(obj.age_preference_lower + 1, 24)
    )

    # Link back to User
    #from Backend.Generators.User_factory import UserFactory
    user_id = factory.LazyAttribute(lambda o: uuid.uuid4())

