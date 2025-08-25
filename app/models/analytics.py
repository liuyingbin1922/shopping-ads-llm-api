from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Index
from sqlalchemy.sql import func
from app.core.database import Base


class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False, index=True)
    event_name = Column(String, nullable=False, index=True)
    user_id = Column(Integer, nullable=True, index=True)
    session_id = Column(String, nullable=True, index=True)
    page_url = Column(String, nullable=True)
    referrer = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)
    ip_address = Column(String, nullable=True)
    properties = Column(JSON, nullable=True)  # Additional event properties
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Composite index for efficient querying
    __table_args__ = (
        Index('idx_event_type_timestamp', 'event_type', 'timestamp'),
        Index('idx_user_id_timestamp', 'user_id', 'timestamp'),
    )
