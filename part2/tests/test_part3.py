"""
Test suite for HBnB Part 3 - Authentication, Authorization, and Database Integration
"""

import pytest
import json
from app import create_app
from app.models import db, User, Place, Review, Amenity
from app.auth import hash_password

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    """Get authentication headers with admin token"""
    response = client.post('/api/v1/auth/register', json={
        'first_name': 'Admin',
        'last_name': 'User',
        'email': 'admin@test.com',
        'password': 'admin123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def regular_user_headers(client):
    """Get authentication headers for regular user"""
    response = client.post('/api/v1/auth/register', json={
        'first_name': 'User',
        'last_name': 'Test',
        'email': 'user@test.com',
        'password': 'user123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

# ==================== Authentication Tests ====================

def test_user_registration(client):
    """Test user registration"""
    response = client.post('/api/v1/auth/register', json={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 201
    data = response.json
    assert 'access_token' in data
    assert 'user_id' in data

def test_user_registration_duplicate_email(client, auth_headers):
    """Test registration with duplicate email"""
    response = client.post('/api/v1/auth/register', json={
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'admin@test.com',
        'password': 'test123'
    })
    
    assert response.status_code == 409

def test_user_login(client):
    """Test user login"""
    # Register first
    client.post('/api/v1/auth/register', json={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'password': 'password123'
    })
    
    # Login
    response = client.post('/api/v1/auth/login', json={
        'email': 'john@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    data = response.json
    assert 'access_token' in data
    assert 'user_id' in data

def test_user_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post('/api/v1/auth/login', json={
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 401

def test_user_login_wrong_password(client):
    """Test login with wrong password"""
    # Register first
    client.post('/api/v1/auth/register', json={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'password': 'password123'
    })
    
    # Try wrong password
    response = client.post('/api/v1/auth/login', json={
        'email': 'john@example.com',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 401

# ==================== User Endpoints Tests ====================

def test_list_users(client):
    """Test listing all users"""
    client.post('/api/v1/auth/register', json={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'password': 'password123'
    })
    
    response = client.get('/api/v1/users')
    
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_user(client, auth_headers):
    """Test getting a specific user"""
    # Get user list to find ID
    response = client.get('/api/v1/users')
    user_id = response.json[0]['id']
    
    # Get specific user
    response = client.get(f'/api/v1/users/{user_id}')
    
    assert response.status_code == 200
    data = response.json
    assert data['id'] == user_id
    assert 'email' in data

def test_update_own_user(client, auth_headers):
    """Test user updating own profile"""
    # Get current user ID from headers
    response = client.get('/api/v1/users', headers=auth_headers)
    user_id = response.json[0]['id']
    
    # Update profile
    response = client.put(
        f'/api/v1/users/{user_id}',
        json={
            'first_name': 'NewName',
            'last_name': 'NewLast',
            'email': 'admin@test.com'
        },
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json
    assert data['first_name'] == 'NewName'

def test_delete_user_requires_auth(client):
    """Test that deleting user requires authentication"""
    response = client.get('/api/v1/users')
    user_id = response.json[0]['id']
    
    # Try delete without auth
    response = client.delete(f'/api/v1/users/{user_id}')
    
    assert response.status_code == 401

# ==================== Place Endpoints Tests ====================

def test_list_places(client):
    """Test listing all places"""
    response = client.get('/api/v1/places')
    
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)

def test_create_place_requires_auth(client):
    """Test that creating place requires authentication"""
    response = client.post('/api/v1/places', json={
        'name': 'Test Place',
        'description': 'A test place',
        'price': 100.0,
        'latitude': 40.7128,
        'longitude': -74.0060
    })
    
    assert response.status_code == 401

def test_create_place(client, auth_headers):
    """Test creating a place"""
    response = client.post(
        '/api/v1/places',
        json={
            'name': 'Cozy Apartment',
            'description': 'A beautiful cozy apartment',
            'price': 100.0,
            'latitude': 40.7128,
            'longitude': -74.0060
        },
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json
    assert data['name'] == 'Cozy Apartment'
    assert data['price'] == 100.0

def test_get_place(client, auth_headers):
    """Test getting a specific place"""
    # Create place first
    response = client.post(
        '/api/v1/places',
        json={
            'name': 'Test Place',
            'description': 'Test description',
            'price': 100.0,
            'latitude': 40.7128,
            'longitude': -74.0060
        },
        headers=auth_headers
    )
    place_id = response.json['id']
    
    # Get place
    response = client.get(f'/api/v1/places/{place_id}')
    
    assert response.status_code == 200
    data = response.json
    assert data['id'] == place_id

def test_update_own_place(client, auth_headers):
    """Test updating own place"""
    # Create place
    response = client.post(
        '/api/v1/places',
        json={
            'name': 'Original Name',
            'description': 'Original description',
            'price': 100.0,
            'latitude': 40.7128,
            'longitude': -74.0060
        },
        headers=auth_headers
    )
    place_id = response.json['id']
    
    # Update place
    response = client.put(
        f'/api/v1/places/{place_id}',
        json={
            'name': 'Updated Name',
            'description': 'Updated description',
            'price': 150.0,
            'latitude': 40.7128,
            'longitude': -74.0060
        },
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json
    assert data['name'] == 'Updated Name'
    assert data['price'] == 150.0

def test_delete_own_place(client, auth_headers):
    """Test deleting own place"""
    # Create place
    response = client.post(
        '/api/v1/places',
        json={
            'name': 'Test Place',
            'description': 'Test description',
            'price': 100.0,
            'latitude': 40.7128,
            'longitude': -74.0060
        },
        headers=auth_headers
    )
    place_id = response.json['id']
    
    # Delete place
    response = client.delete(
        f'/api/v1/places/{place_id}',
        headers=auth_headers
    )
    
    assert response.status_code == 200
    
    # Verify deletion
    response = client.get(f'/api/v1/places/{place_id}')
    assert response.status_code == 404

# ==================== Amenity Endpoints Tests ====================

def test_list_amenities(client):
    """Test listing all amenities"""
    response = client.get('/api/v1/amenities')
    
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)

def test_create_amenity_admin_only(client, auth_headers, regular_user_headers):
    """Test that only admins can create amenities"""
    # Try as regular user
    response = client.post(
        '/api/v1/amenities',
        json={'name': 'WiFi'},
        headers=regular_user_headers
    )
    
    assert response.status_code == 403

def test_create_amenity(client, app):
    """Test creating amenity as admin"""
    with app.app_context():
        # Create admin user
        admin = User(
            first_name='Admin',
            last_name='User',
            email='admin@example.com',
            password=hash_password('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        
        # Login as admin
        response = client.post('/api/v1/auth/login', json={
            'email': 'admin@example.com',
            'password': 'admin123'
        })
        token = response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create amenity
        response = client.post(
            '/api/v1/amenities',
            json={'name': 'WiFi'},
            headers=headers
        )
        
        assert response.status_code == 201
        data = response.json
        assert data['name'] == 'WiFi'

# ==================== Review Endpoints Tests ====================

def test_create_review_requires_auth(client, app):
    """Test that creating review requires authentication"""
    with app.app_context():
        # Create a place first
        place = Place(
            name='Test Place',
            description='Test',
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id='test-owner-id'
        )
        db.session.add(place)
        db.session.commit()
        
        # Try review without auth
        response = client.post('/api/v1/reviews', json={
            'text': 'Great place!',
            'rating': 5,
            'place_id': place.id
        })
        
        assert response.status_code == 401

def test_create_review(client, auth_headers, app):
    """Test creating a review"""
    with app.app_context():
        # Create a place first
        user = User.query.filter_by(email='admin@test.com').first()
        place = Place(
            name='Test Place',
            description='Test',
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=user.id
        )
        db.session.add(place)
        db.session.commit()
        place_id = place.id
        
        # Create review
        response = client.post(
            '/api/v1/reviews',
            json={
                'text': 'Great place!',
                'rating': 5,
                'place_id': place_id
            },
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json
        assert data['text'] == 'Great place!'
        assert data['rating'] == 5

def test_invalid_review_rating(client, auth_headers, app):
    """Test that review rating must be between 1-5"""
    with app.app_context():
        user = User.query.filter_by(email='admin@test.com').first()
        place = Place(
            name='Test Place',
            description='Test',
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=user.id
        )
        db.session.add(place)
        db.session.commit()
        place_id = place.id
        
        # Try invalid rating
        response = client.post(
            '/api/v1/reviews',
            json={
                'text': 'Great place!',
                'rating': 10,  # Invalid
                'place_id': place_id
            },
            headers=auth_headers
        )
        
        assert response.status_code == 400

# ==================== Database Integration Tests ====================

def test_database_user_storage(app):
    """Test that users are stored in database"""
    with app.app_context():
        user = User(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password=hash_password('password123'),
            is_admin=False
        )
        db.session.add(user)
        db.session.commit()
        
        # Retrieve user
        retrieved_user = User.query.filter_by(email='test@example.com').first()
        assert retrieved_user is not None
        assert retrieved_user.first_name == 'Test'

def test_place_ownership(app):
    """Test place-owner relationship"""
    with app.app_context():
        user = User(
            first_name='Owner',
            last_name='User',
            email='owner@example.com',
            password=hash_password('password123'),
            is_admin=False
        )
        db.session.add(user)
        db.session.commit()
        
        place = Place(
            name='Test Place',
            description='Test',
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=user.id
        )
        db.session.add(place)
        db.session.commit()
        
        # Test relationship
        retrieved_place = Place.query.first()
        assert retrieved_place.owner.id == user.id
        assert len(user.places) == 1

def test_place_amenities_relationship(app):
    """Test many-to-many relationship between places and amenities"""
    with app.app_context():
        amenity = Amenity(name='WiFi')
        db.session.add(amenity)
        db.session.commit()
        
        user = User(
            first_name='Owner',
            last_name='User',
            email='owner@example.com',
            password=hash_password('password123'),
            is_admin=False
        )
        db.session.add(user)
        db.session.commit()
        
        place = Place(
            name='Test Place',
            description='Test',
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=user.id
        )
        place.amenities.append(amenity)
        db.session.add(place)
        db.session.commit()
        
        # Test relationship
        retrieved_place = Place.query.first()
        assert len(retrieved_place.amenities) == 1
        assert retrieved_place.amenities[0].name == 'WiFi'

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
