#!/usr/bin/env python3
"""
Simple Analytics Test Script

This script tests the analytics functionality without requiring authentication.
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def test_basic_analytics():
    """Test basic analytics endpoints without authentication"""
    
    print("🧪 Testing Basic Analytics Endpoints...")
    
    # Test data
    test_event = {
        "event_type": "test",
        "event_name": "simple_test",
        "page_url": "https://example.com/test",
        "properties": {
            "test": True,
            "timestamp": datetime.utcnow().isoformat()
        }
    }
    
    # Test single event tracking (no auth required)
    print("\n📊 Testing single event tracking...")
    try:
        response = requests.post(
            f"{BASE_URL}/analytics/track",
            json=test_event,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print(f"✅ Event tracked: {response.json()}")
        else:
            print(f"❌ Event tracking failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing event tracking: {e}")
    
    # Test batch event tracking
    print("\n📦 Testing batch event tracking...")
    try:
        batch_data = {
            "events": [
                {
                    "event_type": "page_view",
                    "event_name": "test_page_view",
                    "page_url": "https://example.com/page1"
                },
                {
                    "event_type": "click",
                    "event_name": "test_button_click",
                    "properties": {"button_id": "test_button"}
                }
            ]
        }
        
        response = requests.post(
            f"{BASE_URL}/analytics/track/batch",
            json=batch_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Batch tracking: {result['message']}")
        else:
            print(f"❌ Batch tracking failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing batch tracking: {e}")


def test_health_check():
    """Test health check endpoint"""
    print("\n🏥 Testing health check...")
    
    try:
        response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health")
        
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check: {health_data['status']}")
            print(f"   Analytics enabled: {health_data['analytics']['enabled']}")
            print(f"   RabbitMQ status: {health_data['analytics']['rabbitmq']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing health check: {e}")


def test_rabbitmq_connection():
    """Test RabbitMQ connection directly"""
    print("\n🐰 Testing RabbitMQ Connection...")
    
    try:
        # Import and test RabbitMQ manager
        from app.core.rabbitmq import rabbitmq_manager
        
        if rabbitmq_manager.is_connected():
            print("✅ RabbitMQ connection successful")
            
            # Test publishing a message
            test_message = {
                "event_type": "test",
                "event_name": "connection_test",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Testing RabbitMQ connection"
            }
            
            if rabbitmq_manager.publish_event(test_message):
                print("✅ Message published to RabbitMQ successfully")
            else:
                print("❌ Failed to publish message to RabbitMQ")
        else:
            print("❌ RabbitMQ connection failed")
            print("   Note: This is expected if RabbitMQ is not running")
            
    except Exception as e:
        print(f"❌ Error testing RabbitMQ: {e}")


def main():
    """Main test function"""
    print("🚀 Starting Simple Analytics Tests...")
    print("=" * 50)
    
    # Test health check first
    test_health_check()
    
    # Test RabbitMQ connection
    test_rabbitmq_connection()
    
    # Test analytics endpoints
    test_basic_analytics()
    
    print("\n" + "=" * 50)
    print("🏁 Simple Analytics Tests Completed!")
    print("\n📝 Notes:")
    print("- Events are stored in the database even if RabbitMQ is not available")
    print("- To test with RabbitMQ, start it with: docker run -d --name rabbitmq -p 5672:5672 rabbitmq:3")
    print("- To view analytics data, check the database: sqlite3 shopping_api.db 'SELECT * FROM analytics_events;'")


if __name__ == "__main__":
    main()
