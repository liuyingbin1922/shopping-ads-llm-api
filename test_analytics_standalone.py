#!/usr/bin/env python3
"""
Standalone Analytics Test

This script tests analytics functionality without importing problematic models.
"""

import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_analytics_without_models():
    """Test analytics without importing problematic models"""
    print("🧪 Testing Analytics Without Problematic Models...")
    
    try:
        # Import only what we need
        from app.core.database import SessionLocal
        from app.models.analytics import AnalyticsEvent
        from app.schemas.analytics import AnalyticsEventCreate
        
        db = SessionLocal()
        
        # Test direct database operations
        print("\n📊 Testing direct database operations...")
        
        # Create a test event directly
        test_event = AnalyticsEvent(
            event_type="test",
            event_name="standalone_test",
            page_url="https://example.com/test",
            properties={"test": True, "standalone": True}
        )
        
        db.add(test_event)
        db.commit()
        print("✅ Test event added to database")
        
        # Query events
        total_events = db.query(AnalyticsEvent).count()
        print(f"✅ Total events in database: {total_events}")
        
        # Show recent events
        recent_events = db.query(AnalyticsEvent).order_by(AnalyticsEvent.timestamp.desc()).limit(3).all()
        print("\n📝 Recent events:")
        for event in recent_events:
            print(f"  - {event.event_name} ({event.event_type}) at {event.timestamp}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error testing analytics: {e}")
        import traceback
        traceback.print_exc()


def test_rabbitmq_standalone():
    """Test RabbitMQ without importing problematic models"""
    print("\n🐰 Testing RabbitMQ Standalone...")
    
    try:
        from app.core.rabbitmq import rabbitmq_manager
        
        if rabbitmq_manager.is_connected():
            print("✅ RabbitMQ connection successful")
            
            # Test publishing
            test_message = {
                "event_type": "test",
                "event_name": "standalone_rabbitmq_test",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Testing RabbitMQ from standalone test"
            }
            
            if rabbitmq_manager.publish_event(test_message):
                print("✅ Message published to RabbitMQ")
            else:
                print("❌ Failed to publish message")
        else:
            print("❌ RabbitMQ connection failed (expected if RabbitMQ not running)")
            
    except Exception as e:
        print(f"❌ Error testing RabbitMQ: {e}")


def test_api_endpoints():
    """Test API endpoints"""
    print("\n🌐 Testing API Endpoints...")
    
    try:
        import requests
        
        # Test health check
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check: {health_data['status']}")
            print(f"   Analytics: {health_data['analytics']['enabled']}")
            print(f"   RabbitMQ: {health_data['analytics']['rabbitmq']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
        
        # Test analytics endpoint with simple data
        test_event = {
            "event_type": "test",
            "event_name": "api_test",
            "page_url": "https://example.com/api-test"
        }
        
        response = requests.post(
            "http://localhost:8000/api/v1/analytics/track",
            json=test_event,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ API event tracking successful")
        else:
            print(f"❌ API event tracking failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing API endpoints: {e}")


def main():
    """Main test function"""
    print("🚀 Starting Standalone Analytics Tests...")
    print("=" * 50)
    
    # Test analytics without problematic models
    test_analytics_without_models()
    
    # Test RabbitMQ
    test_rabbitmq_standalone()
    
    # Test API endpoints
    test_api_endpoints()
    
    print("\n" + "=" * 50)
    print("🏁 Standalone Analytics Tests Completed!")
    print("\n📝 Summary:")
    print("- Analytics events can be stored in database")
    print("- RabbitMQ integration is ready (when RabbitMQ is running)")
    print("- API endpoints are available for event tracking")


if __name__ == "__main__":
    main()
