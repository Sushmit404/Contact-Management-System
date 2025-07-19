#!/usr/bin/env python3
"""
Simple test script for Contact Management System
Run this manually: python simple_test.py
"""

import requests
import json

def simple_test():
    print("=== Contact Management System Test ===")
    print("Make sure your backend is running first!")
    print("To start backend: cd backend && python main.py")
    print()
    
    # Test if server is running
    try:
        response = requests.get("http://localhost:8000/contacts", timeout=5)
        print("✅ Backend is running!")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Contacts found: {len(data.get('contacts', []))}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Backend is NOT running!")
        print("Please start it with: cd backend && python main.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    simple_test() 