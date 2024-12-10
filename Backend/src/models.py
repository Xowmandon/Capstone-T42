from flask import app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



db = SQLAlchemy()
ma = Marshmallow(app)


# TODO - TODO: Consider Using FlaskMarshmallow for Serialization/Deserialization
# - Can also Include Validation and Error Handling Easier than Manual Methods like to_dict

#----If Flask-Marshmallow is  Not Used, Add the Following Code----
# TODO: ADD def to_dict for Each Model to Serialize to JSON
# TODO: ADD def from_dict for Each Model to Deserialize from JSON

# TODO: ADD def to_csv for Each Model to Serialize to CSV
# TODO: ADD def from_csv for Each Model to Deserialize from CSV

#------------------------------------------------------------

# TODO: Add more fields to the User Model to Match the Frontend and ERD
class User(db.Model):
    __tablename__ = 'users' # Define the table name
    
    # Fields of Users, data types provided - May need to change
    id = db.Column(db.Integer, primary_key=True) # Primary Key
    
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    #password = db.Column(db.String(100), nullable=False)   # TODO: Hash + Salt Password
    email = db.Column(db.String(100), unique=True, nullable=False) # Unique Email Address
    
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    
    fake = db.Column(db.Boolean, nullable=False) # Flag to Indicate Fake User
    
    # to_dict Method to Serialize User Object to JSON
    # TODO: Correlate with Self Attributes
    """def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'gender': self.gender
        }
        
    # TODO: Correlate with Self Attributes
    # Consider __dir__ for User Object
    def to_csv(self):
        return f"{self.name}, {self.username}, {self.email}, {self.gender}"
        
    # Convert User Object to String Format, or CSV Format
    # TODO: Correlate with Self Attributes
    #def __str__(self):
        #return f"{self.id},{self.name},{self.username},{self.email}"

    # String representation of a User, Outputting each Field Associated
    # TODO: Correlate with Self Attributes
    def __repr__(self):
        return f"<User id={self.id}, name={self.name}, username={self.username}, email={self.email}, {self.gender}>"

    #def __dir__(self):
        #return ['id', 'name', 'username', 'email']
    """

class Match(db.Model):
    __tablename__ = 'matches' # Define the table name
    
    # Foreign Keys - User ID's in the Successful Match
    matcher = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    matchee = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    
    # ---Dimensional Fields---
    match_date = db.Column(db.DateTime, nullable=False)
    
    # Dictionary Representation of Match Object
    # Returns the Matcher and Matchee Email Addresses and Match Date
    def to_dict(self):
        return {
            'matcher': User.query.get(self.matcher),
            'matchee': User.query.get(self.matchee),
            'match_date': self.match_date
        }

    # String representation of a User, Outputting each Field Associated
    def __repr__(self):
        return f"<Match matcher={self.matcher}, matchee={self.matchee}, match_date={self.match_date}>"
    
    
    
class Message(db.Model):
    __tablename__ = 'messages' # Define the table name
    
    # Supplementary ID for Messages
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys - User ID's  of Sender and Receiver
    messager = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    messagee = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Message Content as String
    message = db.Column(db.String(500), nullable=False)
    
    # ---Dimensional Fields---
    message_date = db.Column(db.DateTime, nullable=False)

    message_read = db.Column(db.Boolean, nullable=False) #Indicate if Message has been Read
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'sender': User.query.get(self.sender),
            'receiver': User.query.get(self.receiver),
            'message': self.message,
            'message_date': self.message_date,
            'message_read': self.message_read
        }

    def __repr__(self):
        return f"<Message id={self.id}, sender={self.sender}, receiver={self.receiver}, message={self.message}, message_date={self.message_date}>"


class Swipe(db.Model):
    __tablename__ = 'swipes'
    
    # Foreign Keys - User ID's of Swiper and Swipee
    swiper = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    swipee = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    
    # ---Dimensional Fields---
   
    # TODO: Refactor with Enum for Swipe Result
    # 0 - Pending (Swiper Swiped Right, Swipee Hasn't Swiped Back Yet), 
    # 1 - Accepted (Both Swiped Right),
    # 2 - Rejected (Swiper Swipped Right, Swipee Swiped Left)
    swipe_result = db.Column(db.Integer, nullable=False)
    
    # ---Dimensional Fields---
    swipe_date = db.Column(db.DateTime, nullable=False)
    
    
    """Example Dictionary Representation of Swipe Object
    {
        'swiper': { 'id': self.id,
                    'name': self.name,
                    'username': self.username,
                    'email': self.email
                },
        'swipee': { 'id': self.id,
                    'name': self.name,
                    'username': self.username,
                    'email': self.email
                },
        'swipe_result': 0,
        'swipe_date': "2025-01-01
    }
    
    """
    def to_dict(self):
        return {
            'swiper': User.query.get(self.swiper),
            'swipee': User.query.get(self.swipee),
            'swipe_result': self.swipe_result,
            'swipe_date': self.swipe_date
        }
    
    
    def __repr__(self):
        return f"<Swipe swiper={self.swiper}, swipee={self.swipee}, swipe_result={self.swipe_result}, swipe_date={self.swipe_date}>"

class Report(db.Model):
    __tablename__ = 'reports' 
    
    # Foreign Keys - User ID's of Reporter and Reportee
    reporter = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    reportee = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    report_reason = db.Column(db.String(500), primary_key=True, nullable=False)
    report_message = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=True) # Optional
    
    report_date = db.Column(db.DateTime, nullable=False)
    
    def to_dict(self):
        return {
            'reporter': User.query.get(self.reporter),
            'reportee': User.query.get(self.reportee),
            'report_reason': self.report_reason,
            'report_message': Message.query.get(self.report_message),
            'report_date': self.report_date
        }
    
    def __repr__(self):
        return f"<Report reporter={self.reporter}, reportee={self.reportee}, report_reason={self.report_reason}, report_date={self.report_date}>"



class ActivityMetrics(db.Model):
        
    __tablename__ = 'activity_metrics' 
        
    ## TODO
    # ?? Update to ActivityMetrics on Event or A Type of Chron Job Ran on Backend ??
    # If Chron Job, Aggregate Metrics from Associated Tables Store in RDS
    # ?? There Might be a Way to Automate this with a Trigger or Stored Procedure ??
        
    # Supplementary Primary ID 
    id = db.Column(db.Integer, primary_key=True)
        
    # Foreign Keys - User To Track Activity Metrics
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        
    # Activity Metrics
    total_swipes = db.Column(db.Integer, nullable=False)
    total_matches = db.Column(db.Integer, nullable=False)
    total_messages = db.Column(db.Integer, nullable=False)
    total_reports = db.Column(db.Integer, nullable=False)
   
    # ---Dimensional Fields---
    activity_date = db.Column(db.DateTime, nullable=False)
        
    def __repr__(self):
        return f"<ActivityMetrics id={self.id}, user_id={self.user_id}, total_swipes={self.total_swipes}, total_matches={self.total_matches}, total_messages={self.total_messages}, total_reports={self.total_reports}, activity_date={self.activity_date}>"
                    
                    
class GameMetrics(db.Model):
            
    __tablename__ = 'game_metrics' 
            
    ## TODO
    # ?? Update to GameMetrics on Event Occurence or A Chron Job Ran on Backend ??
    # If Chron Job, Aggregate Metrics from Associated Tables Store in RDS
    # ?? There Might be a Way to Automate this with a Trigger or Stored Procedure ??
        
            
    # Supplementary Primary ID 
    id = db.Column(db.Integer, primary_key=True)
            
    # Foreign Keys - User To Track Game Metrics
    # TODO - Ensure Unique Constraint is Enforced/Works Correctly
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
            
    # ---Dimensional Fields---
            
    total_games = db.Column(db.Integer, nullable=False)
    total_wins = db.Column(db.Integer, nullable=False)
    total_losses = db.Column(db.Integer, nullable=False)
            
    game_metrics_date = db.Column(db.DateTime, nullable=False)
            
    def __repr__(self):
        return f"<GameMetrics id={self.id}, user_id={self.user_id}, total_games={self.total_games}, total_wins={self.total_wins}, total_losses={self.total_losses}, game_metrics_date={self.game_metrics_date}>"