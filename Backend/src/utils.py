import os
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
import gnupg

class EnvManager:
    
    def __init__(self):
        
        # Load the .env file from the root directory
        self.env_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../.env'))
        load_dotenv(self.env_file_path)
    
    # Wrapper for Retrieval Passed variable Name
    def load_env_var(self, var_name):
        return os.getenv(var_name)
    
    # Utility Function to Decrypt and Load the .env File - Now Decrypted
    def load_encrypted_env(self, passphrase):
        gpg = gnupg.GPG()
        with open(self.env_file_path, 'rb') as f:
            decrypted_data = gpg.decrypt_file(f, passphrase=passphrase)
            if decrypted_data.ok:
                with open('.env', 'w') as env_file:
                    env_file.write(str(decrypted_data))
                self.load_dotenv()
            else:
                raise Exception("Failed to decrypt the .env file")

# Base Configuration Class
# Contains the Common Configuration Options 
class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    def __repr__(self):
        return f"Config({self.SQLALCHEMY_DATABASE_URI})"


# Development Configuration Class
# Config Options for AWS RDS
class DevDBConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = URL.create(
        "postgresql",
        password="",  # plain (unescaped) text
        host=EnvManager().load_env_var('RDS_HOSTNAME'),
        port=5432,
        database="Unhinged_DB",
    )

# Test Configuration DB
# Config Options for Local Testing - Uses Local Postgres DB
class TestDBConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = URL.create(
        "postgresql",
        username="postgres",
        password="joshua16",
        host="localhost",
        port=5432,
        database="test_unhinged_db",
    )
    SQLALCHEMY_ECHO = True

