import random
import uuid

import factory  # Factory Boy
from faker import Faker

import Backend.src.models as models
from Backend.src.extensions import bcrypt, db, llm_service

faker = Faker()
# faker.seed_instance(16)


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.user.User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    # Core identification & auth
    id = factory.Faker("uuid4")
    email = email = factory.LazyAttribute(
        lambda o: str(uuid.uuid4())[:8] + "__" + faker.email()
    )
    password_hash = factory.LazyAttribute(
        lambda o: bcrypt.generate_password_hash(
            faker.password(length=10, digits=True, upper_case=True, lower_case=True)
        ).decode("utf-8")
    )
    auth_provider = "email"
    username = factory.LazyAttribute(lambda o: faker.user_name())

    # Personal details
    name = factory.LazyAttribute(lambda o: faker.name_female())
    gender = factory.LazyAttribute(lambda o: random.choice(["male", "female", "any"]))
    age = factory.LazyAttribute(lambda o: random.randint(18, 24))
    city = factory.LazyAttribute(lambda o: faker.city().lower())
    state = factory.LazyAttribute(lambda o: faker.state_abbr().upper())
    country_code = factory.LazyAttribute(lambda o: faker.country_code().upper())
    is_fake = True

    # **Generate a fun, youthful bio via LLMService**
    bio = factory.LazyAttribute(
        lambda o: llm_service.gen_bio_llm(
            user_profile=(f"{o.name}, {str(o.age)}, {faker.job()}, {faker.emoji()} "),
            prompt=None,  # will be ignored; BIO_PROMPT_TEMPLATE is used internally
        )
    )
