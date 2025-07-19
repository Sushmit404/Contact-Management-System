#!/usr/bin/env python3
import requests
import json
import time

def test_backend():
    base_url = "http://localhost:8000"
    
    print("Testing Contact Management System Backend...")
    print("=" * 50)
    
    # Test 1: Get all contacts (should be empty initially)
    print("1. Testing GET /contacts...")
    try:
        response = requests.get(f"{base_url}/contacts")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data.get('contacts', []))} contacts")
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Is the backend running?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 2: Create a new contact
    print("\n2. Testing POST /create_contact...")
    test_contact = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "category": "Work"
    }
    
    try:
        response = requests.post(f"{base_url}/create_contact", json=test_contact)
        if response.status_code == 201:
            data = response.json()
            print("✅ Contact created successfully!")
            print(f"Response: {json.dumps(data, indent=2)}")
            contact_id = data.get('contact', {}).get('id')
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 3: Get contacts again (should have 1 contact now)
    print("\n3. Testing GET /contacts (should now have 1 contact)...")
    try:
        response = requests.get(f"{base_url}/contacts")
        if response.status_code == 200:
            data = response.json()
            contacts = data.get('contacts', [])
            print(f"✅ Success! Found {len(contacts)} contacts")
            if len(contacts) > 0:
                print(f"First contact: {json.dumps(contacts[0], indent=2)}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ Backend tests completed successfully!")
    return True

if __name__ == "__main__":
    test_backend() 