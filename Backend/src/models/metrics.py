# Author: Joshua Ferguson

from datetime import datetime, timezone
from Backend.src.extensions import db, ma


class ActivityMetric(db.Model):
        
    __tablename__ = 'activitymetrics' 
        
    ## TODO
    # ?? Update to ActivityMetrics on Event or A Type of Chron Job Ran on Backend ??
    # If Chron Job, Aggregate Metrics from Associated Tables Store in RDS
    # ?? There Might be a Way to Automate this with a Trigger or Stored Procedure ??
    
    # Consider Backrefs with Model Relationships for User to Access Activity Metrics
    
    # TODO: Implement CASCADE on User Deletion
        
    # Supplementary Primary ID 
    id = db.Column(db.Integer, primary_key=True)
        
    # Foreign Keys - User To Track Activity Metrics
    # On Delete of User - Cascade to Remove Associated Activity Metrics
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'), nullable=False)
        
    # Activity Metrics
    # TODO: Implement Aggregation of Metrics from Associated Tables - Automatically 
    total_swipes = db.Column(db.Integer, nullable=False)
    total_matches = db.Column(db.Integer, nullable=False)
    total_messages = db.Column(db.Integer, nullable=False)
    total_reports = db.Column(db.Integer, nullable=False)
    
    # ---Dimensional Fields---
    activity_date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    
    
    
    # -----Relationships-----
    """
    user_activity_metrics = db.relationship("User", foreign_keys=[user_id], backref="activity_metrics")
    """
        
    def __repr__(self):
        return f"<ActivityMetrics id={self.id}, user_id={self.user_id}, total_swipes={self.total_swipes}, total_matches={self.total_matches}, total_messages={self.total_messages}, total_reports={self.total_reports}, activity_date={self.activity_date}>"
                    
                    
class GameMetric(db.Model):
            
    __tablename__ = 'GameMetrics' 
            
    ## TODO
    # ?? Update to GameMetrics on Event Occurence or A Chron Job Ran on Backend ??
    # If Chron Job, Aggregate Metrics from Associated Tables Store in RDS
    # ?? There Might be a Way to Automate this with a Trigger or Stored Procedure ??
        
            
    # Supplementary Primary ID 
    id = db.Column(db.Integer, primary_key=True)
            
    # Foreign Keys - User To Track Game Metrics
    # TODO - Ensure Unique Constraint is Enforced/Works Correctly
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'), unique=True, nullable=False)
            
    # ---Dimensional Fields---
            
    total_games = db.Column(db.Integer, nullable=False)
    total_wins = db.Column(db.Integer, nullable=False)
    total_losses = db.Column(db.Integer, nullable=False)
            
    game_metrics_date = db.Column(db.DateTime, nullable=False)
    
    """
    user_game_metrics = db.relationship("User",  foreign_keys=[user_id], back_populates="game_metrics")
    """   
    def __repr__(self):
        return f"<GameMetrics id={self.id}, user_id={self.user_id}, total_games={self.total_games}, total_wins={self.total_wins}, total_losses={self.total_losses}, game_metrics_date={self.game_metrics_date}>"