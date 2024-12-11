# Desc: Report Model and Schema for Reports Table
# Schema for Deserializing and Serializing
from marshmallow import ValidationError, validates

from Backend.src.extensions import db, ma # DB and Marshmallow Instances

from Backend.src.models.user import User # User Model
from Backend.src.models.message import Message # Message Model
from Backend.src.validators.text import TextValidator # Custom Validators

REPORT_CONTENT_LENGTH = 300


# Report Model for Reports Table
class Report(db.Model):
    __tablename__ = 'reports' 
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys - User ID's of Reporter and Reportee
    # On Delete of User - Cascade to Remove Associated Reports
    reporter = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    reportee = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True,  nullable=False)
    
    # Report Reason and Associated Message
    report_reason = db.Column(db.String(REPORT_CONTENT_LENGTH), primary_key=True, nullable=False)
    report_message = db.Column(db.Integer, db.ForeignKey('messages.id'),nullable=True) # Optional
    
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
        load_instance = True
        include_relationships = True
        
    
    @validates("report_reason")
    def validate_report_reason(self, reason):
        # Length and Profanity Filter
        TextValidator.val_length(reason, upper_bound=REPORT_CONTENT_LENGTH)
    
class ReportSchemaNested(ReportSchema):
    class Meta:
        model = Report
        load_instance = True
        include_relationships = True
        
    reporter = ma.Nested(User)
    reportee = ma.Nested(User)
    report_message = ma.Nested(Message)
    
    