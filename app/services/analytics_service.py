import uuid
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.analytics import AnalyticsEvent
from app.schemas.analytics import AnalyticsEventCreate, AnalyticsQuery, AnalyticsSummary
from app.core.rabbitmq import rabbitmq_manager
from app.core.config import settings

logger = logging.getLogger(__name__)


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def _generate_session_id(self) -> str:
        """Generate a unique session ID"""
        return str(uuid.uuid4())

    def _enrich_event_data(self, event_data: AnalyticsEventCreate, request_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Enrich event data with additional context"""
        enriched_data = event_data.dict()
        
        # Add timestamp
        enriched_data['timestamp'] = datetime.utcnow().isoformat()
        
        # Add request information if provided
        if request_info:
            enriched_data.update({
                'ip_address': request_info.get('ip_address'),
                'user_agent': request_info.get('user_agent'),
                'referrer': request_info.get('referrer'),
                'page_url': request_info.get('page_url'),
            })
        
        # Add session ID if not provided
        if not enriched_data.get('session_id'):
            enriched_data['session_id'] = self._generate_session_id()
            
        return enriched_data

    def track_event(self, event_data: AnalyticsEventCreate, request_info: Dict[str, Any] = None) -> bool:
        """Track a single analytics event"""
        try:
            # Enrich event data
            enriched_data = self._enrich_event_data(event_data, request_info)
            
            # Save to database
            db_event = AnalyticsEvent(**enriched_data)
            self.db.add(db_event)
            self.db.commit()
            
            # Publish to RabbitMQ if enabled
            if settings.ANALYTICS_ENABLED:
                rabbitmq_manager.publish_event(enriched_data)
            
            logger.debug(f"Tracked event: {event_data.event_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to track event: {e}")
            self.db.rollback()
            return False

    def track_batch(self, events: List[AnalyticsEventCreate], request_info: Dict[str, Any] = None) -> int:
        """Track multiple analytics events"""
        tracked_count = 0
        enriched_events = []
        
        try:
            for event_data in events:
                # Enrich event data
                enriched_data = self._enrich_event_data(event_data, request_info)
                enriched_events.append(enriched_data)
                
                # Save to database
                db_event = AnalyticsEvent(**enriched_data)
                self.db.add(db_event)
                tracked_count += 1
            
            self.db.commit()
            
            # Publish batch to RabbitMQ if enabled
            if settings.ANALYTICS_ENABLED:
                rabbitmq_manager.publish_batch(enriched_events)
            
            logger.info(f"Tracked {tracked_count} events")
            return tracked_count
            
        except Exception as e:
            logger.error(f"Failed to track batch events: {e}")
            self.db.rollback()
            return 0

    def get_events(self, query: AnalyticsQuery) -> List[AnalyticsEvent]:
        """Get analytics events with filtering"""
        query_builder = self.db.query(AnalyticsEvent)
        
        if query.event_type:
            query_builder = query_builder.filter(AnalyticsEvent.event_type == query.event_type)
            
        if query.user_id:
            query_builder = query_builder.filter(AnalyticsEvent.user_id == query.user_id)
            
        if query.start_date:
            query_builder = query_builder.filter(AnalyticsEvent.timestamp >= query.start_date)
            
        if query.end_date:
            query_builder = query_builder.filter(AnalyticsEvent.timestamp <= query.end_date)
        
        return query_builder.order_by(AnalyticsEvent.timestamp.desc()).offset(query.offset).limit(query.limit).all()

    def get_analytics_summary(self, days: int = 7) -> AnalyticsSummary:
        """Get analytics summary for the specified time period"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get total events
        total_events = self.db.query(AnalyticsEvent).filter(
            AnalyticsEvent.timestamp >= start_date,
            AnalyticsEvent.timestamp <= end_date
        ).count()
        
        # Get unique users
        unique_users = self.db.query(AnalyticsEvent.user_id).filter(
            AnalyticsEvent.timestamp >= start_date,
            AnalyticsEvent.timestamp <= end_date,
            AnalyticsEvent.user_id.isnot(None)
        ).distinct().count()
        
        # Get event types count
        event_types_result = self.db.query(
            AnalyticsEvent.event_type,
            func.count(AnalyticsEvent.id)
        ).filter(
            AnalyticsEvent.timestamp >= start_date,
            AnalyticsEvent.timestamp <= end_date
        ).group_by(AnalyticsEvent.event_type).all()
        
        event_types = {event_type: count for event_type, count in event_types_result}
        
        # Get top pages
        top_pages_result = self.db.query(
            AnalyticsEvent.page_url,
            func.count(AnalyticsEvent.id)
        ).filter(
            AnalyticsEvent.timestamp >= start_date,
            AnalyticsEvent.timestamp <= end_date,
            AnalyticsEvent.page_url.isnot(None)
        ).group_by(AnalyticsEvent.page_url).order_by(
            func.count(AnalyticsEvent.id).desc()
        ).limit(10).all()
        
        top_pages = {page_url: count for page_url, count in top_pages_result}
        
        return AnalyticsSummary(
            total_events=total_events,
            unique_users=unique_users,
            event_types=event_types,
            top_pages=top_pages,
            time_period=f"Last {days} days"
        )

    def get_user_events(self, user_id: int, limit: int = 100) -> List[AnalyticsEvent]:
        """Get events for a specific user"""
        return self.db.query(AnalyticsEvent).filter(
            AnalyticsEvent.user_id == user_id
        ).order_by(AnalyticsEvent.timestamp.desc()).limit(limit).all()

    def get_popular_products(self, days: int = 7, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most viewed products"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        result = self.db.query(
            AnalyticsEvent.properties['product_id'].label('product_id'),
            AnalyticsEvent.properties['product_name'].label('product_name'),
            func.count(AnalyticsEvent.id).label('view_count')
        ).filter(
            AnalyticsEvent.event_type == 'product_view',
            AnalyticsEvent.timestamp >= start_date,
            AnalyticsEvent.timestamp <= end_date,
            AnalyticsEvent.properties.isnot(None)
        ).group_by(
            AnalyticsEvent.properties['product_id'],
            AnalyticsEvent.properties['product_name']
        ).order_by(
            func.count(AnalyticsEvent.id).desc()
        ).limit(limit).all()
        
        return [
            {
                'product_id': row.product_id,
                'product_name': row.product_name,
                'view_count': row.view_count
            }
            for row in result
        ]
