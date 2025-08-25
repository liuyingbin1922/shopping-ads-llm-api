from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class AnalyticsEventBase(BaseModel):
    event_type: str = Field(..., description="Event type (page_view, click, purchase, etc.)")
    event_name: str = Field(..., description="Specific event name")
    user_id: Optional[int] = Field(None, description="User ID if authenticated")
    session_id: Optional[str] = Field(None, description="Session identifier")
    page_url: Optional[str] = Field(None, description="Current page URL")
    referrer: Optional[str] = Field(None, description="Referrer URL")
    user_agent: Optional[str] = Field(None, description="User agent string")
    ip_address: Optional[str] = Field(None, description="IP address")
    properties: Optional[Dict[str, Any]] = Field(None, description="Additional event properties")


class AnalyticsEventCreate(AnalyticsEventBase):
    pass


class AnalyticsEventResponse(AnalyticsEventBase):
    id: int
    timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class AnalyticsEventBatch(BaseModel):
    events: list[AnalyticsEventCreate] = Field(..., description="Batch of events to track")


class AnalyticsQuery(BaseModel):
    event_type: Optional[str] = Field(None, description="Filter by event type")
    user_id: Optional[int] = Field(None, description="Filter by user ID")
    start_date: Optional[datetime] = Field(None, description="Start date for filtering")
    end_date: Optional[datetime] = Field(None, description="End date for filtering")
    limit: int = Field(100, description="Number of events to return")
    offset: int = Field(0, description="Number of events to skip")


class AnalyticsSummary(BaseModel):
    total_events: int
    unique_users: int
    event_types: Dict[str, int]
    top_pages: Dict[str, int]
    time_period: str
