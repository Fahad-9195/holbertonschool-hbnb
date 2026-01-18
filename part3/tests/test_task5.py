"""
Test suite for Task 5: Administrator Access Endpoints
Tests admin-only endpoints and admin bypass of ownership restrictions
"""

import pytest
import json
from app import create_app, bcrypt
from app.models.base_model import db, User, Place, Review, Amenity
from app.persistence.repository import UserRepository, PlaceRepository, ReviewRepository, AmenityRepository
from config import TestingConfig
from flask_jwt_extended import create_access_token


@pytest.fixture
def app():
    """Create and configure a test app."""
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def admin_user(app):
    """Create an admin user for testing."""
    with app.app_context():
        repo = UserRepository()
        admin = User(
            first_name="Admin",
            last_name="User",
            email="admin@test.com",
            is_admin=True
        )
        admin.hash_password("admin123")
        return repo.add(admin)


@pytest.fixture
def regular_user(app):
    """Create a regular user for testing."""
    with app.app_context():
        repo = UserRepository()
        user = User(
            first_name="Regular",
            last_name="User",
            email="user@test.com",
            is_admin=False
        )
        user.hash_password("user123")
        return repo.add(user)


@pytest.fixture
def another_user(app):
    """Create another regular user for testing."""
    with app.app_context():
        repo = UserRepository()
        user = User(
            first_name="Another",
            last_name="User",
            email="another@test.com",
            is_admin=False
        )
        user.hash_password("another123")
        return repo.add(user)


@pytest.fixture
def admin_token(app, admin_user):
    """Generate admin JWT token."""
    with app.app_context():
        token = create_access_token(
            identity=str(admin_user.id),
            additional_claims={"is_admin": True}
        )
        return token


@pytest.fixture
def user_token(app, regular_user):
    """Generate regular user JWT token."""
    with app.app_context():
        token = create_access_token(
            identity=str(regular_user.id),
            additional_claims={"is_admin": False}
        )
        return token


@pytest.fixture
def another_user_token(app, another_user):
    """Generate another user's JWT token."""
    with app.app_context():
        token = create_access_token(
            identity=str(another_user.id),
            additional_claims={"is_admin": False}
        )
        return token


class TestAdminUserCreation:
    """Test admin-only user creation endpoint"""
    
    def test_admin_can_create_user(self, client, admin_token):
        """Test that admin can create a new user"""
        response = client.post(
            '/api/v1/users/',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'first_name': 'New',
                'last_name': 'User',
                'email': 'newuser@test.com',
                'password': 'newpass123'
            }
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['first_name'] == 'New'
        assert data['last_name'] == 'User'
        assert data['email'] == 'newuser@test.com'
        assert data['is_admin'] == False
    
    def test_admin_can_create_admin_user(self, client, admin_token):
        """Test that admin can create another admin user"""
        response = client.post(
            '/api/v1/users/',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'first_name': 'New',
                'last_name': 'Admin',
                'email': 'newadmin@test.com',
                'password': 'newpass123',
                'is_admin': True
            }
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['is_admin'] == True
    
    def test_non_admin_cannot_create_user(self, client, user_token):
        """Test that non-admin user cannot create users"""
        response = client.post(
            '/api/v1/users/',
            headers={'Authorization': f'Bearer {user_token}'},
            json={
                'first_name': 'New',
                'last_name': 'User',
                'email': 'newuser@test.com',
                'password': 'newpass123'
            }
        )
        assert response.status_code == 403
        data = json.loads(response.data)
        assert 'Admin access required' in data.get('message', '')
    
    def test_unauthenticated_cannot_create_user(self, client):
        """Test that unauthenticated user cannot create users"""
        response = client.post(
            '/api/v1/users/',
            json={
                'first_name': 'New',
                'last_name': 'User',
                'email': 'newuser@test.com',
                'password': 'newpass123'
            }
        )
        assert response.status_code == 401
    
    def test_admin_cannot_create_duplicate_email(self, client, admin_token, regular_user):
        """Test that admin cannot create user with existing email"""
        response = client.post(
            '/api/v1/users/',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={
                'first_name': 'Duplicate',
                'last_name': 'User',
                'email': 'user@test.com',  # Already exists
                'password': 'newpass123'
            }
        )
        assert response.status_code == 409


class TestAdminUserUpdate:
    """Test admin-only user update endpoint"""
    
    def test_admin_can_update_user_email(self, client, admin_token, another_user):
        """Test that admin can update another user's email"""
        response = client.put(
            f'/api/v1/users/{another_user.id}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={'email': 'updated@test.com'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['email'] == 'updated@test.com'
    
    def test_admin_can_update_user_password(self, client, app, admin_token, another_user):
        """Test that admin can update another user's password"""
        response = client.put(
            f'/api/v1/users/{another_user.id}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={'password': 'newpassword123'}
        )
        assert response.status_code == 200
        
        # Verify password was actually changed
        with app.app_context():
            repo = UserRepository()
            user = repo.get(another_user.id)
            assert user.verify_password('newpassword123')
            assert not user.verify_password('another123')
    
    def test_admin_can_update_is_admin_flag(self, client, admin_token, regular_user):
        """Test that admin can update is_admin flag"""
        response = client.put(
            f'/api/v1/users/{regular_user.id}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={'is_admin': True}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['is_admin'] == True
    
    def test_non_admin_cannot_update_other_user(self, client, user_token, another_user):
        """Test that non-admin cannot update other user's profile"""
        response = client.put(
            f'/api/v1/users/{another_user.id}',
            headers={'Authorization': f'Bearer {user_token}'},
            json={'email': 'hacker@test.com'}
        )
        assert response.status_code == 403
    
    def test_non_admin_can_update_own_profile(self, client, user_token, regular_user):
        """Test that non-admin can update own profile"""
        response = client.put(
            f'/api/v1/users/{regular_user.id}',
            headers={'Authorization': f'Bearer {user_token}'},
            json={'first_name': 'Updated'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['first_name'] == 'Updated'
    
    def test_non_admin_cannot_update_own_email(self, client, user_token, regular_user):
        """Test that non-admin cannot update own email"""
        response = client.put(
            f'/api/v1/users/{regular_user.id}',
            headers={'Authorization': f'Bearer {user_token}'},
            json={'email': 'newemail@test.com'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        # Email should NOT be updated
        assert data['email'] == 'user@test.com'
    
    def test_admin_cannot_update_to_duplicate_email(self, client, admin_token, another_user, regular_user):
        """Test that admin cannot update email to one that already exists"""
        response = client.put(
            f'/api/v1/users/{another_user.id}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={'email': 'user@test.com'}  # regular_user's email
        )
        assert response.status_code == 409


class TestAdminPlaceAccess:
    """Test admin bypass of place ownership restrictions"""
    
    @pytest.fixture
    def place(self, app, regular_user):
        """Create a place owned by regular_user"""
        with app.app_context():
            place = Place(
                name='Test Place',
                description='A test place',
                price=100.0,
                latitude=40.7128,
                longitude=-74.0060,
                owner_id=regular_user.id
            )
            repo = PlaceRepository()
            return repo.add(place)
    
    def test_admin_can_update_other_user_place(self, client, admin_token, place):
        """Test that admin can update place they don't own"""
        response = client.put(
            f'/api/v1/places/{place.id}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={'price': 150.0}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['price'] == 150.0
    
    def test_admin_can_delete_other_user_place(self, client, admin_token, place):
        """Test that admin can delete place they don't own"""
        response = client.delete(
            f'/api/v1/places/{place.id}',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert response.status_code == 200
    
    def test_non_admin_cannot_update_other_user_place(self, client, another_user_token, place):
        """Test that non-admin cannot update place they don't own"""
        response = client.put(
            f'/api/v1/places/{place.id}',
            headers={'Authorization': f'Bearer {another_user_token}'},
            json={'price': 200.0}
        )
        assert response.status_code == 403
    
    def test_non_admin_cannot_delete_other_user_place(self, client, another_user_token, place):
        """Test that non-admin cannot delete place they don't own"""
        response = client.delete(
            f'/api/v1/places/{place.id}',
            headers={'Authorization': f'Bearer {another_user_token}'}
        )
        assert response.status_code == 403
    
    def test_owner_can_update_own_place(self, client, user_token, place):
        """Test that owner can update their own place"""
        response = client.put(
            f'/api/v1/places/{place.id}',
            headers={'Authorization': f'Bearer {user_token}'},
            json={'price': 125.0}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['price'] == 125.0


class TestAdminReviewAccess:
    """Test admin bypass of review ownership restrictions"""
    
    @pytest.fixture
    def place_and_review(self, app, regular_user, another_user):
        """Create a place and review for testing"""
        with app.app_context():
            place = Place(
                name='Test Place',
                description='A test place',
                price=100.0,
                latitude=40.7128,
                longitude=-74.0060,
                owner_id=regular_user.id
            )
            place_repo = PlaceRepository()
            place = place_repo.add(place)
            
            review = Review(
                text='Great place!',
                rating=5,
                user_id=another_user.id,
                place_id=place.id
            )
            review_repo = ReviewRepository()
            review = review_repo.add(review)
            
            return place, review
    
    def test_admin_can_update_other_user_review(self, client, admin_token, place_and_review):
        """Test that admin can update review they didn't write"""
        _, review = place_and_review
        response = client.put(
            f'/api/v1/reviews/{review.id}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={'text': 'Updated by admin', 'rating': 3}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['text'] == 'Updated by admin'
        assert data['rating'] == 3
    
    def test_admin_can_delete_other_user_review(self, client, admin_token, place_and_review):
        """Test that admin can delete review they didn't write"""
        _, review = place_and_review
        response = client.delete(
            f'/api/v1/reviews/{review.id}',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert response.status_code == 200
    
    def test_non_admin_cannot_update_other_user_review(self, client, user_token, place_and_review):
        """Test that non-admin cannot update review they didn't write"""
        _, review = place_and_review
        response = client.put(
            f'/api/v1/reviews/{review.id}',
            headers={'Authorization': f'Bearer {user_token}'},
            json={'text': 'Hacked', 'rating': 1}
        )
        assert response.status_code == 403
    
    def test_non_admin_cannot_delete_other_user_review(self, client, user_token, place_and_review):
        """Test that non-admin cannot delete review they didn't write"""
        _, review = place_and_review
        response = client.delete(
            f'/api/v1/reviews/{review.id}',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        assert response.status_code == 403
    
    def test_reviewer_can_update_own_review(self, client, another_user_token, place_and_review):
        """Test that reviewer can update their own review"""
        _, review = place_and_review
        response = client.put(
            f'/api/v1/reviews/{review.id}',
            headers={'Authorization': f'Bearer {another_user_token}'},
            json={'text': 'Still great!', 'rating': 4}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['text'] == 'Still great!'
        assert data['rating'] == 4


class TestAdminAmenityAccess:
    """Test admin-only amenity endpoints"""
    
    def test_admin_can_create_amenity(self, client, admin_token):
        """Test that admin can create amenity"""
        response = client.post(
            '/api/v1/amenities/',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={'name': 'Swimming Pool'}
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'Swimming Pool'
    
    def test_non_admin_cannot_create_amenity(self, client, user_token):
        """Test that non-admin cannot create amenity"""
        response = client.post(
            '/api/v1/amenities/',
            headers={'Authorization': f'Bearer {user_token}'},
            json={'name': 'Hot Tub'}
        )
        assert response.status_code == 403
    
    def test_unauthenticated_cannot_create_amenity(self, client):
        """Test that unauthenticated user cannot create amenity"""
        response = client.post(
            '/api/v1/amenities/',
            json={'name': 'Gym'}
        )
        assert response.status_code == 401
    
    def test_admin_can_update_amenity(self, client, app, admin_token):
        """Test that admin can update amenity"""
        with app.app_context():
            amenity = Amenity(name='Original Name')
            repo = AmenityRepository()
            amenity = repo.add(amenity)
        
        response = client.put(
            f'/api/v1/amenities/{amenity.id}',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={'name': 'Updated Name'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Updated Name'
    
    def test_non_admin_cannot_update_amenity(self, client, app, user_token):
        """Test that non-admin cannot update amenity"""
        with app.app_context():
            amenity = Amenity(name='Original Name')
            repo = AmenityRepository()
            amenity = repo.add(amenity)
        
        response = client.put(
            f'/api/v1/amenities/{amenity.id}',
            headers={'Authorization': f'Bearer {user_token}'},
            json={'name': 'Hacked Name'}
        )
        assert response.status_code == 403
    
    def test_admin_can_delete_amenity(self, client, app, admin_token):
        """Test that admin can delete amenity"""
        with app.app_context():
            amenity = Amenity(name='To Delete')
            repo = AmenityRepository()
            amenity = repo.add(amenity)
        
        response = client.delete(
            f'/api/v1/amenities/{amenity.id}',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert response.status_code == 200
    
    def test_non_admin_cannot_delete_amenity(self, client, app, user_token):
        """Test that non-admin cannot delete amenity"""
        with app.app_context():
            amenity = Amenity(name='Original')
            repo = AmenityRepository()
            amenity = repo.add(amenity)
        
        response = client.delete(
            f'/api/v1/amenities/{amenity.id}',
            headers={'Authorization': f'Bearer {user_token}'}
        )
        assert response.status_code == 403


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
