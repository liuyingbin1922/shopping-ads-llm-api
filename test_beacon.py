#!/usr/bin/env python3
"""
Beacon API Test Script

This script tests the beacon endpoints for navigator.sendBeacon support.
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000/api/v1/beacon"

def test_beacon_endpoints():
    """Test beacon endpoints"""
    
    print("🧪 Testing Beacon Endpoints...")
    
    # Test 1: Basic beacon endpoint
    print("\n📊 Testing basic beacon endpoint...")
    test_data = {
        "event_type": "test",
        "event_name": "beacon_test",
        "user_id": 123,
        "session_id": "session_123",
        "page_url": "https://example.com/test",
        "properties": {
            "test": True,
            "timestamp": datetime.utcnow().isoformat()
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/beacon",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 204:
            print("✅ Basic beacon endpoint: Success (204 No Content)")
        else:
            print(f"❌ Basic beacon endpoint: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing basic beacon: {e}")
    
    # Test 2: Simple beacon endpoint
    print("\n🎯 Testing simple beacon endpoint...")
    try:
        response = requests.post(
            f"{BASE_URL}/simple",
            params={
                "type": "page_view",
                "name": "simple_test",
                "url": "https://example.com/simple",
                "uid": "123"
            }
        )
        
        if response.status_code == 204:
            print("✅ Simple beacon endpoint: Success (204 No Content)")
        else:
            print(f"❌ Simple beacon endpoint: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing simple beacon: {e}")
    
    # Test 3: Form data beacon
    print("\n📝 Testing form data beacon...")
    try:
        form_data = {
            "event_type": "form",
            "event_name": "form_submit",
            "user_id": "123",
            "page_url": "https://example.com/form",
            "properties": json.dumps({"form_id": "test_form"})
        }
        
        response = requests.post(
            f"{BASE_URL}/beacon",
            data=form_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 204:
            print("✅ Form data beacon: Success (204 No Content)")
        else:
            print(f"❌ Form data beacon: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing form data beacon: {e}")


def test_health_check():
    """Test health check endpoint"""
    print("\n🏥 Testing health check...")
    
    try:
        response = requests.get("http://localhost:8000/health")
        
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check: {health_data['status']}")
            print(f"   Analytics: {health_data['analytics']['enabled']}")
            print(f"   RabbitMQ: {health_data['analytics']['rabbitmq']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing health check: {e}")


def check_database():
    """Check if beacon events are stored in database"""
    print("\n📋 Checking database for beacon events...")
    
    try:
        import sqlite3
        
        conn = sqlite3.connect('shopping_api.db')
        cursor = conn.cursor()
        
        # Check total events
        cursor.execute("SELECT COUNT(*) FROM analytics_events")
        total_events = cursor.fetchone()[0]
        print(f"✅ Total events in database: {total_events}")
        
        # Check beacon events
        cursor.execute("SELECT COUNT(*) FROM analytics_events WHERE properties LIKE '%beacon%'")
        beacon_events = cursor.fetchone()[0]
        print(f"✅ Beacon events in database: {beacon_events}")
        
        # Show recent beacon events
        cursor.execute("""
            SELECT event_name, event_type, page_url, created_at 
            FROM analytics_events 
            WHERE properties LIKE '%beacon%' 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        
        recent_events = cursor.fetchall()
        if recent_events:
            print("\n📝 Recent beacon events:")
            for event in recent_events:
                print(f"  - {event[0]} ({event[1]}) at {event[3]}")
        else:
            print("📝 No beacon events found in database")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")


def main():
    """Main test function"""
    print("🚀 Starting Beacon API Tests...")
    print("=" * 50)
    
    # Test health check first
    test_health_check()
    
    # Test beacon endpoints
    test_beacon_endpoints()
    
    # Check database
    check_database()
    
    print("\n" + "=" * 50)
    print("🏁 Beacon API Tests Completed!")
    print("\n📝 Next steps:")
    print("1. Open static/demo.html in a browser")
    print("2. Test navigator.sendBeacon functionality")
    print("3. Check the browser console for logs")
    print("4. Verify events are stored in the database")


if __name__ == "__main__":
    main()
