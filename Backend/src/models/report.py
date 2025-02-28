# Desc: Report Model and Schema for Reports Table
# Schema for Deserializing and Serializing

from datetime import datetime, timezone

from marshmallow import ValidationError, validates
from sqlalchemy import Enum, CheckConstraint
from sqlalchemy.orm import relationship

from Backend.src.extensions import db, ma # DB and Marshmallow Instances

from Backend.src.models.user import User # User Model
from Backend.src.models.message import Message # Message Model
from Backend.src.validators.text_val import TextValidator # Custom Validators

REPORT_CONTENT_LENGTH = 300

# Define the ReportStatus Enum
class ReportStatus(Enum):
    PENDING = "Pending"
    RESOLVED = "Resolved"
    REJECTED = "Rejected"
    

# Report Model for Reports Table
class Report(db.Model):
    __tablename__ = 'reports' 

    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys - User ID's of Reporter and Reportee
    # On Delete of User - Cascade to Remove Associated Reports
    reporter = db.Column(db.String(64), db.ForeignKey('users.id'), primary_key=True, nullable=False)
    reportee = db.Column(db.String(64), db.ForeignKey('users.id'), primary_key=True,  nullable=False)
    
    # Report Reason and Associated Message
    report_reason = db.Column(db.String(REPORT_CONTENT_LENGTH), primary_key=True, nullable=False)
    report_message = db.Column(db.Integer, db.ForeignKey('messages.id'),nullable=True) # Optional
    
    report_date = db.Column(db.DateTime, nullable=False,default=datetime.now(timezone.utc))
    
    # Report Status - Enum of Pending, Resolved, Rejected
    status = db.Column(db.String, nullable=False, default="PENDING") # Report Status
    
    # Check Constraint for status, either Pending, Resolved, or Rejected
    __table_args__ = (
        CheckConstraint(status.in_(['PENDING', 'RESOLVED', 'REJECTED']), name='report_status_check'),
    )
    #-----Relationships-----
    """
    reports_as_reporter = relationship("User",  foreign_keys=[reporter], backref="reports_by_user")
    reports_on_reportee = relationship("User",  foreign_keys=[reportee], backref="reports_on_user")
    reports_on_message = relationship("Message", back_populates="reports")
    """

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
    
    