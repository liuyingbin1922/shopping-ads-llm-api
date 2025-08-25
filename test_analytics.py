#!/usr/bin/env python3
"""
Analytics Testing Script

This script tests the analytics functionality by sending various events.
"""

import requests
import json
import time
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def test_analytics_endpoints():
    """Test various analytics endpoints"""
    
    print("🧪 Testing Analytics Endpoints...")
    
    # Test data
    test_events = [
        {
            "event_type": "page_view",
            "event_name": "homepage_visited",
            "page_url": "https://example.com/",
            "properties": {
                "page_title": "Homepage",
                "referrer": "https://google.com"
            }
        },
        {
            "event_type": "product_view",
            "event_name": "product_viewed",
            "properties": {
                "product_id": 1,
                "product_name": "iPhone 15 Pro",
                "category": "Electronics",
                "price": 999.99
            }
        },
        {
            "event_type": "click",
            "event_name": "add_to_cart_clicked",
            "properties": {
                "product_id": 1,
                "product_name": "iPhone 15 Pro",
                "button_text": "Add to Cart"
            }
        },
        {
            "event_type": "purchase",
            "event_name": "order_completed",
            "properties": {
                "order_id": 12345,
                "total_amount": 999.99,
                "product_ids": [1],
                "payment_method": "credit_card"
            }
        }
    ]
    
    # Test single event tracking
    print("\n📊 Testing single event tracking...")
    for event in test_events:
        try:
            response = requests.post(
                f"{BASE_URL}/analytics/track",
                json=event,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print(f"✅ {event['event_name']}: {response.json()}")
            else:
                print(f"❌ {event['event_name']}: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Error testing {event['event_name']}: {e}")
    
    # Test batch event tracking
    print("\n📦 Testing batch event tracking...")
    try:
        batch_data = {"events": test_events}
        response = requests.post(
            f"{BASE_URL}/analytics/track/batch",
            json=batch_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Batch tracking: {result['message']}")
        else:
            print(f"❌ Batch tracking: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing batch tracking: {e}")
    
    # Test convenience endpoints
    print("\n🎯 Testing convenience endpoints...")
    
    # Test page view
    try:
        response = requests.post(
            f"{BASE_URL}/analytics/page-view",
            params={"page_url": "https://example.com/products"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print(f"✅ Page view: {response.json()}")
        else:
            print(f"❌ Page view: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing page view: {e}")
    
    # Test product view
    try:
        response = requests.post(
            f"{BASE_URL}/analytics/product-view",
            params={
                "product_id": 1,
                "product_name": "iPhone 15 Pro"
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print(f"✅ Product view: {response.json()}")
        else:
            print(f"❌ Product view: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing product view: {e}")
    
    # Test purchase
    try:
        response = requests.post(
            f"{BASE_URL}/analytics/purchase",
            params={
                "order_id": 12345,
                "total_amount": 999.99,
                "product_ids": [1]
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print(f"✅ Purchase: {response.json()}")
        else:
            print(f"❌ Purchase: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing purchase: {e}")


def test_rabbitmq_connection():
    """Test RabbitMQ connection"""
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
            
    except Exception as e:
        print(f"❌ Error testing RabbitMQ: {e}")


def main():
    """Main test function"""
    print("🚀 Starting Analytics System Tests...")
    print("=" * 50)
    
    # Test RabbitMQ connection first
    test_rabbitmq_connection()
    
    # Wait a moment for any setup
    time.sleep(1)
    
    # Test analytics endpoints
    test_analytics_endpoints()
    
    print("\n" + "=" * 50)
    print("🏁 Analytics System Tests Completed!")
    print("\n📝 Next steps:")
    print("1. Start the analytics consumer: python analytics_consumer.py")
    print("2. Check the consumer logs for processed events")
    print("3. Monitor RabbitMQ queue for message processing")


if __name__ == "__main__":
    main()
