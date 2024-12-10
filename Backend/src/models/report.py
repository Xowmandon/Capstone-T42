# Desc: Report Model and Schema for Reports Table
# Schema for Deserializing and Serializing

from src.extensions import db, ma # DB and Marshmallow Instances

from src.models.user import User # User Model
from src.models.message import Message # Message Model

# Report Model for Reports Table
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

# Marshmallow Schema for the Report

class ReportSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Report
  