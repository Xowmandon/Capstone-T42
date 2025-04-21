from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime, timezone
from Backend.src.extensions import db

class UserFcmToken(db.Model):
    __tablename__ = "user_fcm_tokens"

    id = Column(String(64), primary_key=True)
    user_id = Column(String(64), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True,unique=True)
    fcm_token = Column(String(512), nullable=False)
    last_updated = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<UserFcmToken user_id={self.user_id} token={self.fcm_token[:10]}...>"
