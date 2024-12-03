from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# TODO: Add more fields to the User Model to Match the Frontend and ERD
class User(db.Model):
    __tablename__ = 'users' # Define the table name
    
    # Fields of Users, data types provided - May need to change
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # String representation of a User, Outputting each Field Associated
    def __repr__(self):
        return f"<User id={self.id}, name={self.name}, email={self.email}>"


class Match(db.Model):
    __tablename__ = 'matches' # Define the table name
    
    # Fields of Users, data types provided - May need to change
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys - User ID's in the Successful Match
    matcher = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    matchee = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Composite Primary Key - UNIQUE(Matcher and Matchee)
    db.PrimaryKeyConstraint(matcher, matchee)
    
    # ---Dimensional Fields---
    match_date = db.Column(db.DateTime, nullable=False)

    # String representation of a User, Outputting each Field Associated
    def __repr__(self):
        return f"<Match id={self.id}, user_id={self.user_id}, match_id={self.match_id}, match_date={self.match_date}>"
    
class Message(db.Model):
    __tablename__ = 'messages' # Define the table name
    
    # Supplementary ID for Messages
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys - User ID's  of Sender and Receiver
    sender = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Message Content as String
    message = db.Column(db.String(500), nullable=False)
    
    # ---Dimensional Fields---
    message_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Message id={self.id}, sender={self.sender}, receiver={self.receiver}, message={self.message}, message_date={self.message_date}>"


class Swipe(db.model):
    
    __tablename__ = 'swipes'
    
    # Supplementary Primary ID
    id = db.Column(db.Integer, primary_key=True)
    
    # ----Foreign Keys---
    swiper = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    swipee = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Composite Primary Key - UNIQUE(swiper and swipee)
    db.PrimaryKeyConstraint(swiper, swipee)
    
    # ---Dimensional Fields---
   
    # TODO: Refactor with Enum for Swipe Result
    # 0 - Pending (Swiper Swiped Right, Swipee Hasn't Swiped Back Yet), 
    # 1 - Accepted (Both Swiped Right),
    # 2 - Rejected (Swiper Swipped Right, Swipee Swiped Left)
    swipe_result = db.Column(db.Integer, nullable=False)
    
    # ---Dimensional Fields---
    swipe_date = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f"<Swipe id={self.id}, swiper={self.swiper}, swipee={self.swipee}, swipe_result={self.swipe_result}, swipe_date={self.swipe_date}>"

class Report(db.model):
    
    __tablename__ = 'reports' 
    
    # Supplementary Primary ID 
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys - User ID's  of Reporter and Reportee
    reporter = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reportee = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    report_message = db.Column(db.Integer, db.ForeignKey('messages.id'),  nullable=True) # Optional
    
    report_date = db.Column(db.DateTime, nullable=False)
    
    # Reason for Report - Either Enterted by User or Selected from a List of Message
    report_reason = db.Column(db.String(500), nullable=False)
    
    # TODO - Normalize Report Reason to a Table? or Enforce Different Composite Key
            # OR Get Rid of Unique Constrant
    # Composite Primary Key - UNIQUE(reporter and reportee and report_reason)
    db.primaryKeyConstraint(reporter, reportee, report_reason)
    
    def __repr__(self):
        return f"<Report id={self.id}, reporter={self.reporter}, reportee={self.reportee}, report_date={self.report_date}, report_reason={self.report_reason}>"



class ActivityMetrics(db.model):
        
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
            return f"<
                    ActivityMetrics id={self.id}, 
                    user_id={self.user_id}, 
                    total_swipes={self.total_swipes}, 
                    total_matches={self.total_matches}, 
                    total_messages={self.total_messages}, 
                    total_reports={self.total_reports}, 
                    activity_date={self.activity_date}
                    >"
                    
                    
class GameMetrics(db.model):
            
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
                return f"<
                        GameMetrics id={self.id}, 
                        user_id={self.user_id}, 
                        total_games={self.total_games}, 
                        total_wins={self.total_wins}, 
                        total_losses={self.total_losses}, 
                        total_draws={self.total_draws}, 
                        total_points={self.total_points}, 
                        game_date={self.game_date}
                        >"