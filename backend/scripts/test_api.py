"""
Simple script to test the API endpoints.

Run this after starting the server to verify everything works.
"""

import requests
import json

BASE_URL = "http://localhost:8000"
API_KEY = "dev-api-key-12345"  # Match the key from init_db.py or your .env

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json",
}


def test_health():
    """Test health endpoint."""
    print("\n1. Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_create_chatbox():
    """Test creating a chatbox."""
    print("\n2. Testing chatbox creation...")
    data = {
        "name": "Test Chatbox",
        "description": "A test chatbox for demo",
        "allowed_domains": ["https://example.com"],
        "enforce_allowed_domains": False,
    }
    response = requests.post(
        f"{BASE_URL}/v1/chatboxes",
        headers=headers,
        json=data,
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        return response.json()["id"]
    return None


def test_list_chatboxes():
    """Test listing chatboxes."""
    print("\n3. Testing chatbox listing...")
    response = requests.get(f"{BASE_URL}/v1/chatboxes", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_ingest_text(chatbox_id):
    """Test text ingestion."""
    print("\n4. Testing text ingestion...")
    data = {
        "chatbox_id": chatbox_id,
        "text": "FastAPI is a modern, fast web framework for building APIs with Python 3.7+. "
                "It's based on standard Python type hints and provides automatic API documentation.",
        "source_name": "FastAPI Introduction",
    }
    response = requests.post(
        f"{BASE_URL}/v1/ingest/text",
        headers=headers,
        json=data,
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 201


def test_query(chatbox_id):
    """Test querying."""
    print("\n5. Testing query...")
    data = {
        "chatbox_id": chatbox_id,
        "question": "What is FastAPI?",
        "origin": "https://example.com",
    }
    response = requests.post(
        f"{BASE_URL}/v1/query",
        headers=headers,
        json=data,
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def main():
    """Run all tests."""
    print("=" * 60)
    print("Helperly API Test Suite")
    print("=" * 60)
    print(f"\nBase URL: {BASE_URL}")
    print(f"API Key: {API_KEY}")
    
    try:
        # Test health
        if not test_health():
            print("\n❌ Health check failed!")
            return
        
        # Test chatbox creation
        chatbox_id = test_create_chatbox()
        if not chatbox_id:
            print("\n❌ Chatbox creation failed!")
            return
        
        # Test listing
        if not test_list_chatboxes():
            print("\n❌ Chatbox listing failed!")
            return
        
        # Test ingestion
        if not test_ingest_text(chatbox_id):
            print("\n❌ Text ingestion failed!")
            return
        
        # Test query
        if not test_query(chatbox_id):
            print("\n❌ Query failed!")
            return
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server.")
        print("Make sure the server is running:")
        print("  uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
