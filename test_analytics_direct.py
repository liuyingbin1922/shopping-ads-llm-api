#!/usr/bin/env python3
"""
Direct Analytics Service Test

This script tests the analytics service directly without going through the API.
"""

import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import AnalyticsEventCreate
from app.models import user, product, order, analytics

def test_analytics_service():
    """Test analytics service directly"""
    print("🧪 Testing Analytics Service Directly...")
    
    db = SessionLocal()
    analytics_service = AnalyticsService(db)
    
    try:
        # Test single event
        print("\n📊 Testing single event tracking...")
        event_data = AnalyticsEventCreate(
            event_type="test",
            event_name="direct_test",
            page_url="https://example.com/test",
            properties={"test": True, "direct": True}
        )
        
        success = analytics_service.track_event(event_data)
        if success:
            print("✅ Single event tracked successfully")
        else:
            print("❌ Single event tracking failed")
        
        # Test batch events
        print("\n📦 Testing batch event tracking...")
        batch_events = [
            AnalyticsEventCreate(
                event_type="page_view",
                event_name="test_page_view",
                page_url="https://example.com/page1"
            ),
            AnalyticsEventCreate(
                event_type="click",
                event_name="test_button_click",
                properties={"button_id": "test_button"}
            )
        ]
        
        tracked_count = analytics_service.track_batch(batch_events)
        print(f"✅ Batch tracking: {tracked_count}/{len(batch_events)} events tracked")
        
        # Check database
        print("\n📋 Checking database...")
        from app.models.analytics import AnalyticsEvent
        total_events = db.query(AnalyticsEvent).count()
        print(f"✅ Total events in database: {total_events}")
        
        # Show recent events
        recent_events = db.query(AnalyticsEvent).order_by(AnalyticsEvent.timestamp.desc()).limit(5).all()
        print("\n📝 Recent events:")
        for event in recent_events:
            print(f"  - {event.event_name} ({event.event_type}) at {event.timestamp}")
        
    except Exception as e:
        print(f"❌ Error testing analytics service: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def test_rabbitmq_manager():
    """Test RabbitMQ manager directly"""
    print("\n🐰 Testing RabbitMQ Manager...")
    
    try:
        from app.core.rabbitmq import rabbitmq_manager
        
        if rabbitmq_manager.is_connected():
            print("✅ RabbitMQ connection successful")
            
            # Test publishing
            test_message = {
                "event_type": "test",
                "event_name": "direct_rabbitmq_test",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            if rabbitmq_manager.publish_event(test_message):
                print("✅ Message published to RabbitMQ")
            else:
                print("❌ Failed to publish message")
        else:
            print("❌ RabbitMQ connection failed (expected if RabbitMQ not running)")
            
    except Exception as e:
        print(f"❌ Error testing RabbitMQ manager: {e}")


def main():
    """Main test function"""
    print("🚀 Starting Direct Analytics Tests...")
    print("=" * 50)
    
    # Test analytics service
    test_analytics_service()
    
    # Test RabbitMQ manager
    test_rabbitmq_manager()
    
    print("\n" + "=" * 50)
    print("🏁 Direct Analytics Tests Completed!")


if __name__ == "__main__":
    main()
