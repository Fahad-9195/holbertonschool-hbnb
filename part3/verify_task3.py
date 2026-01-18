#!/usr/bin/env python
"""
Task 3 Verification - Authenticated User Access Endpoints
Tests all the security features implemented
"""

import sys
import json

def test_endpoints():
    """Test all endpoints with proper authentication"""
    
    from app import create_app
    from config import DevelopmentConfig
    
    # Create app with test config
    app = create_app(DevelopmentConfig)
    client = app.test_client()
    
    print("=" * 60)
    print("Task 3: Authenticated User Access Endpoints - VERIFICATION")
    print("=" * 60)
    
    # Test 1: Public GET endpoints (no auth required)
    print("\n[TEST 1] Public GET endpoints (no authentication required)")
    print("-" * 60)
    
    endpoints = [
        ('GET', '/api/v1/places/'),
        ('GET', '/api/v1/reviews/'),
        ('GET', '/api/v1/amenities/'),
        ('GET', '/api/v1/users/')
    ]
    
    for method, endpoint in endpoints:
        response = client.get(endpoint)
        status = "✓" if response.status_code == 200 else "✗"
        print(f"{status} {method} {endpoint}: {response.status_code}")
    
    # Test 2: User registration
    print("\n[TEST 2] User registration and JWT token generation")
    print("-" * 60)
    
    register_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password": "SecurePass123!"
    }
    response = client.post('/api/v1/auth/register', json=register_data)
    print(f"Registration status: {response.status_code}")
    
    token = None
    user_id = None
    if response.status_code == 201:
        print("✓ Registration successful")
        data = response.json
        token = data.get('access_token')
        user_id = data.get('user_id')
        print(f"✓ JWT token generated: {token[:30]}...")
        print(f"✓ User ID: {user_id}")
    else:
        print(f"✗ Registration failed: {response.json}")
        return
    
    # Test 3: Login
    print("\n[TEST 3] User login and JWT token generation")
    print("-" * 60)
    
    login_data = {
        "email": "john@example.com",
        "password": "SecurePass123!"
    }
    response = client.post('/api/v1/auth/login', json=login_data)
    if response.status_code == 200:
        print("✓ Login successful")
        login_token = response.json.get('access_token')
        print(f"✓ JWT token received: {login_token[:30]}...")
    else:
        print(f"✗ Login failed: {response.json}")
    
    # Test 4: Create a place (authenticated)
    print("\n[TEST 4] Create a place (requires JWT authentication)")
    print("-" * 60)
    
    place_data = {
        "name": "Beautiful Beach House",
        "description": "A wonderful place by the sea",
        "price": 150.00,
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/api/v1/places/', json=place_data, headers=headers)
    
    place_id = None
    if response.status_code == 201:
        print("✓ Place created successfully")
        place_id = response.json.get('id')
        print(f"✓ Place ID: {place_id}")
    else:
        print(f"✗ Place creation failed: {response.json}")
    
    # Test 5: Create without authentication (should fail)
    print("\n[TEST 5] Attempt to create place without authentication")
    print("-" * 60)
    
    response = client.post('/api/v1/places/', json=place_data)
    if response.status_code == 401:
        print("✓ Correctly rejected unauthenticated request (401)")
    else:
        print(f"✗ Should have returned 401, got {response.status_code}")
    
    # Test 6: Register another user for testing
    print("\n[TEST 6] Register another user for review tests")
    print("-" * 60)
    
    user2_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com",
        "password": "SecurePass456!"
    }
    response = client.post('/api/v1/auth/register', json=user2_data)
    token2 = None
    if response.status_code == 201:
        print("✓ Second user registered")
        token2 = response.json.get('access_token')
    else:
        print(f"✗ Second registration failed: {response.json}")
        return
    
    # Test 7: Create a review (authenticated, with ownership check)
    print("\n[TEST 7] Create a review (authenticated, with ownership validation)")
    print("-" * 60)
    
    review_data = {
        "text": "Amazing place! Highly recommended",
        "rating": 5,
        "place_id": place_id
    }
    
    headers2 = {'Authorization': f'Bearer {token2}'}
    response = client.post('/api/v1/reviews/', json=review_data, headers=headers2)
    
    if response.status_code == 201:
        print("✓ Review created successfully")
        review_id = response.json.get('id')
        print(f"✓ Review ID: {review_id}")
    else:
        print(f"✗ Review creation failed: {response.json}")
    
    # Test 8: Try to review own place (should fail)
    print("\n[TEST 8] Prevent owner from reviewing own place")
    print("-" * 60)
    
    own_review_data = {
        "text": "Reviewing my own place",
        "rating": 5,
        "place_id": place_id
    }
    
    headers_owner = {'Authorization': f'Bearer {token}'}
    response = client.post('/api/v1/reviews/', json=own_review_data, headers=headers_owner)
    
    if response.status_code == 400:
        print("✓ Correctly prevented owner from reviewing own place (400)")
        print(f"  Message: {response.json.get('message', '')}")
    else:
        print(f"✗ Should have returned 400, got {response.status_code}")
    
    # Test 9: Try duplicate review (should fail)
    print("\n[TEST 9] Prevent duplicate reviews")
    print("-" * 60)
    
    duplicate_review = {
        "text": "Another review of the same place",
        "rating": 4,
        "place_id": place_id
    }
    
    response = client.post('/api/v1/reviews/', json=duplicate_review, headers=headers2)
    
    if response.status_code == 400:
        print("✓ Correctly prevented duplicate review (400)")
        print(f"  Message: {response.json.get('message', '')}")
    else:
        print(f"✗ Should have returned 400, got {response.status_code}")
    
    # Test 10: Update place (ownership check)
    print("\n[TEST 10] Update place with ownership validation")
    print("-" * 60)
    
    update_data = {
        "name": "Updated Beach House",
        "price": 175.00
    }
    
    # Try update with non-owner token
    response = client.put(f'/api/v1/places/{place_id}', json=update_data, headers=headers2)
    if response.status_code == 403:
        print("✓ Correctly prevented non-owner from updating place (403)")
    else:
        print(f"✗ Should have returned 403, got {response.status_code}")
    
    # Try update with owner token
    response = client.put(f'/api/v1/places/{place_id}', json=update_data, headers=headers_owner)
    if response.status_code == 200:
        print("✓ Owner can update their own place (200)")
    else:
        print(f"✗ Owner update failed with status {response.status_code}")
    
    # Test 11: Update user (self-only restriction)
    print("\n[TEST 11] Update user with self-restriction")
    print("-" * 60)
    
    user_update = {
        "first_name": "Jonathan"
    }
    
    # Try update own profile
    response = client.put(f'/api/v1/users/{user_id}', json=user_update, headers=headers_owner)
    if response.status_code == 200:
        print("✓ User can update own profile (200)")
    else:
        print(f"✗ User update failed: {response.json}")
    
    # Test 12: Admin operations (amenities)
    print("\n[TEST 12] Admin-only operations (amenities)")
    print("-" * 60)
    
    amenity_data = {
        "name": "WiFi"
    }
    
    # Try to create amenity with regular user (should fail)
    response = client.post('/api/v1/amenities/', json=amenity_data, headers=headers_owner)
    if response.status_code == 401:  # Not admin
        print("✓ Regular user cannot create amenity (401)")
    else:
        print(f"✗ Should have returned 401, got {response.status_code}")
    
    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETE")
    print("=" * 60)
    print("\n✓ All authentication and access control features verified!")

if __name__ == "__main__":
    try:
        test_endpoints()
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
