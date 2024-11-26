

from sqlalchemy.engine.url import URL

class Config:
    SQLALCHEMY_DATABASE_URI = URL.create(
        "postgresql",
        password="",  # plain (unescaped) text
        host="captstone-db.cvkkwcai4hfp.us-west-1.rds.amazonaws.com",
        port=5432,
        database="Unhinged_DB",
    )
    
    # Track modifications of objects and emit signals
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Echo SQL Queries into the Console
    SQLALCHEMY_ECHO = False
    
# TODO - Refactor/Test Config for Test Environment
class ConfigTestLocal:
    SQLALCHEMY_DATABASE_URI = URL.create(
        "postgresql",
        password="",  # plain (unescaped) text
        host="localhost",
        port=5432,
        database="Unhinged_DB_Test",
    )
    
    # Echo SQL Queries into the Console
    SQLALCHEMY_ECHO = True