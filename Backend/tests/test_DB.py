import os, sys


# Add the parent directory to the system path
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from src.utils import DevDBConfig, LocalDBConfig, EnvManager

# TODO: Implement Real Unit Tests  
class DBTester():
    # Test the Database Connection
    def test_db_connection(self):
        # Test the Database Connection
        pass
    
    def test_load_config(self):
        
        Dev_Config = DevDBConfig()
        Test_Config = LocalDBConfig()
        
        print(Dev_Config)
        print(Test_Config)
        
        pass
    
Tester = DBTester()
Tester.test_load_config()