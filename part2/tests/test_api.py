"""
Integration tests for API endpoints.
Tests HTTP requests and responses using Flask test client.
"""
import pytest
from app import create_app
from app.services import facade
from app.persistence.repository import InMemoryRepository


@pytest.fixture(autouse=True)
def reset_repository():
    """Reset the repository before each test."""
    # Create a fresh repository
    new_repo = InMemoryRepository()
    
    # Import the facade module
    import app.services
    
    # CRITICAL: Directly replace the repository in the facade instance
    # This is the facade that's imported in all API endpoints
    app.services.facade.repo = new_repo
    
    # Also reset the shared references
    app.services._shared_repo = new_repo
    app.services._shared_facade = app.services.facade

@pytest.fixture
def client():
    """Create a Flask test client."""
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client


class TestUsersAPI:
    """Test Users API endpoints."""

    def test_create_user_success(self, client):
        """Test POST /api/v1/users - successful creation."""
        response = client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        }, follow_redirects=True)
        assert response.status_code == 201
        data = response.get_json()
        assert data["first_name"] == "John"
        assert data["last_name"] == "Doe"
        assert data["email"] == "john@example.com"
        assert "id" in data

    def test_create_user_missing_fields(self, client):
        """Test POST /api/v1/users - missing required fields."""
        response = client.post('/api/v1/users/', json={
            "first_name": "John"
        }, follow_redirects=True)
        assert response.status_code == 400

    def test_create_user_duplicate_email(self, client):
        """Test POST /api/v1/users - duplicate email."""
        client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        }, follow_redirects=True)
        response = client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "john@example.com"
        }, follow_redirects=True)
        assert response.status_code == 409

    def test_list_users(self, client):
        """Test GET /api/v1/users - list all users."""
        client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        }, follow_redirects=True)
        client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com"
        }, follow_redirects=True)
        response = client.get('/api/v1/users/', follow_redirects=True)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2

    def test_get_user_success(self, client):
        """Test GET /api/v1/users/<id> - successful retrieval."""
        create_response = client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        }, follow_redirects=True)
        assert create_response.status_code == 201
        data = create_response.get_json()
        assert data is not None
        assert "id" in data
        user_id = data["id"]
        response = client.get(f'/api/v1/users/{user_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data["id"] == user_id

    def test_get_user_not_found(self, client):
        """Test GET /api/v1/users/<id> - user not found."""
        response = client.get('/api/v1/users/non-existent-id')
        assert response.status_code == 404


class TestAmenitiesAPI:
    """Test Amenities API endpoints."""

    def test_create_amenity_success(self, client):
        """Test POST /api/v1/amenities - successful creation."""
        response = client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        }, follow_redirects=True)
        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == "WiFi"
        assert "id" in data

    def test_create_amenity_missing_name(self, client):
        """Test POST /api/v1/amenities - missing name."""
        response = client.post('/api/v1/amenities/', json={}, follow_redirects=True)
        assert response.status_code == 400

    def test_create_amenity_duplicate_name(self, client):
        """Test POST /api/v1/amenities - duplicate name."""
        client.post('/api/v1/amenities/', json={"name": "WiFi"}, follow_redirects=True)
        response = client.post('/api/v1/amenities/', json={"name": "WiFi"}, follow_redirects=True)
        assert response.status_code == 409

    def test_list_amenities(self, client):
        """Test GET /api/v1/amenities - list all amenities."""
        client.post('/api/v1/amenities/', json={"name": "WiFi"}, follow_redirects=True)
        client.post('/api/v1/amenities/', json={"name": "Pool"}, follow_redirects=True)
        response = client.get('/api/v1/amenities/', follow_redirects=True)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2

    def test_get_amenity_success(self, client):
        """Test GET /api/v1/amenities/<id> - successful retrieval."""
        create_response = client.post('/api/v1/amenities/', json={"name": "WiFi"}, follow_redirects=True)
        assert create_response.status_code == 201
        data = create_response.get_json()
        assert data is not None
        assert "id" in data
        amenity_id = data["id"]
        response = client.get(f'/api/v1/amenities/{amenity_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data["id"] == amenity_id

    def test_get_amenity_not_found(self, client):
        """Test GET /api/v1/amenities/<id> - amenity not found."""
        response = client.get('/api/v1/amenities/non-existent-id')
        assert response.status_code == 404

    def test_update_amenity_success(self, client):
        """Test PUT /api/v1/amenities/<id> - successful update."""
        create_response = client.post('/api/v1/amenities/', json={"name": "WiFi"}, follow_redirects=True)
        assert create_response.status_code == 201
        data = create_response.get_json()
        assert data is not None
        assert "id" in data
        amenity_id = data["id"]
        response = client.put(f'/api/v1/amenities/{amenity_id}', json={"name": "Free WiFi"}, follow_redirects=True)
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "Free WiFi"


class TestPlacesAPI:
    """Test Places API endpoints."""

    def test_create_place_success(self, client):
        """Test POST /api/v1/places - successful creation."""
        user_response = client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        }, follow_redirects=True)
        assert user_response.status_code == 201
        user_data = user_response.get_json()
        assert user_data is not None
        assert "id" in user_data
        user_id = user_data["id"]
        
        response = client.post('/api/v1/places/', json={
            "name": "Beautiful Apartment",
            "description": "A nice place",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": user_id
        }, follow_redirects=True)
        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == "Beautiful Apartment"
        assert data["owner"]["id"] == user_id
        assert data["owner"]["first_name"] == "John"
        assert "amenities" in data

    def test_create_place_missing_fields(self, client):
        """Test POST /api/v1/places - missing required fields."""
        response = client.post('/api/v1/places/', json={
            "name": "Place"
        }, follow_redirects=True)
        assert response.status_code == 400

    def test_create_place_invalid_owner(self, client):
        """Test POST /api/v1/places - invalid owner_id."""
        response = client.post('/api/v1/places/', json={
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": "non-existent"
        }, follow_redirects=True)
        assert response.status_code == 404

    def test_create_place_with_amenities(self, client):
        """Test POST /api/v1/places - with amenities."""
        user_response = client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        }, follow_redirects=True)
        user_id = user_response.get_json()["id"]
        
        amenity_response = client.post('/api/v1/amenities/', json={"name": "WiFi"}, follow_redirects=True)
        amenity_id = amenity_response.get_json()["id"]
        
        response = client.post('/api/v1/places/', json={
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": user_id,
            "amenity_ids": [amenity_id]
        }, follow_redirects=True)
        assert response.status_code == 201
        data = response.get_json()
        assert len(data["amenities"]) == 1
        assert data["amenities"][0]["id"] == amenity_id

    def test_list_places(self, client):
        """Test GET /api/v1/places - list all places."""
        user_response = client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        }, follow_redirects=True)
        assert user_response.status_code == 201
        user_data = user_response.get_json()
        assert user_data is not None
        assert "id" in user_data
        user_id = user_data["id"]
        
        client.post('/api/v1/places', json={
            "name": "Place 1",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": user_id
        }, follow_redirects=True)
        response = client.get('/api/v1/places/', follow_redirects=True)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert "owner" in data[0]
        assert "amenities" in data[0]

    def test_get_place_success(self, client):
        """Test GET /api/v1/places/<id> - successful retrieval."""
        user_response = client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        }, follow_redirects=True)
        assert user_response.status_code == 201
        user_data = user_response.get_json()
        assert user_data is not None
        assert "id" in user_data
        user_id = user_data["id"]
        
        create_response = client.post('/api/v1/places/', json={
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": user_id
        }, follow_redirects=True)
        assert create_response.status_code == 201
        place_data = create_response.get_json()
        assert place_data is not None
        assert "id" in place_data
        place_id = place_data["id"]
        response = client.get(f'/api/v1/places/{place_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data["id"] == place_id

    def test_get_place_not_found(self, client):
        """Test GET /api/v1/places/<id> - place not found."""
        response = client.get('/api/v1/places/non-existent-id')
        assert response.status_code == 404

    def test_update_place_success(self, client):
        """Test PUT /api/v1/places/<id> - successful update."""
        user_response = client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        }, follow_redirects=True)
        assert user_response.status_code == 201
        user_data = user_response.get_json()
        assert user_data is not None
        assert "id" in user_data
        user_id = user_data["id"]
        
        create_response = client.post('/api/v1/places/', json={
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": user_id
        }, follow_redirects=True)
        assert create_response.status_code == 201
        place_data = create_response.get_json()
        assert place_data is not None
        assert "id" in place_data
        place_id = place_data["id"]
        
        response = client.put(f'/api/v1/places/{place_id}', json={
            "name": "Updated Place",
            "price": 150.0
        }, follow_redirects=True)
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "Updated Place"
        assert data["price"] == 150.0

    def test_list_place_reviews(self, client):
        """Test GET /api/v1/places/<id>/reviews - list reviews for a place."""
        owner_response = client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        }, follow_redirects=True)
        assert owner_response.status_code == 201
        owner_data = owner_response.get_json()
        assert owner_data is not None
        assert "id" in owner_data
        owner_id = owner_data["id"]
        
        place_response = client.post('/api/v1/places/', json={
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner_id
        }, follow_redirects=True)
        assert place_response.status_code == 201
        place_data = place_response.get_json()
        assert place_data is not None
        assert "id" in place_data
        place_id = place_data["id"]
        
        reviewer_response = client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com"
        }, follow_redirects=True)
        assert reviewer_response.status_code == 201
        reviewer_data = reviewer_response.get_json()
        assert reviewer_data is not None
        assert "id" in reviewer_data
        reviewer_id = reviewer_data["id"]
        
        client.post('/api/v1/reviews/', json={
            "text": "Great!",
            "rating": 5,
            "user_id": reviewer_id,
            "place_id": place_id
        }, follow_redirects=True)
        
        response = client.get(f'/api/v1/places/{place_id}/reviews', follow_redirects=True)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]["place_id"] == place_id


class TestReviewsAPI:
    """Test Reviews API endpoints."""

    def test_create_review_success(self, client):
        """Test POST /api/v1/reviews - successful creation."""
        owner_response = client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        }, follow_redirects=True)
        assert owner_response.status_code == 201
        owner_data = owner_response.get_json()
        assert owner_data is not None
        assert "id" in owner_data
        owner_id = owner_data["id"]
        
        place_response = client.post('/api/v1/places/', json={
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner_id
        }, follow_redirects=True)
        assert place_response.status_code == 201
        place_data = place_response.get_json()
        assert place_data is not None
        assert "id" in place_data
        place_id = place_data["id"]
        
        reviewer_response = client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com"
        }, follow_redirects=True)
        assert reviewer_response.status_code == 201
        reviewer_data = reviewer_response.get_json()
        assert reviewer_data is not None
        assert "id" in reviewer_data
        reviewer_id = reviewer_data["id"]
        
        response = client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": reviewer_id,
            "place_id": place_id
        }, follow_redirects=True)
        assert response.status_code == 201
        data = response.get_json()
        assert data["text"] == "Great place!"
        assert data["rating"] == 5
        assert data["user"]["id"] == reviewer_id
        assert data["place"]["id"] == place_id

    def test_create_review_missing_fields(self, client):
        """Test POST /api/v1/reviews - missing required fields."""
        response = client.post('/api/v1/reviews/', json={
            "text": "Great!"
        }, follow_redirects=True)
        assert response.status_code == 400

    def test_create_review_invalid_user(self, client):
        """Test POST /api/v1/reviews - invalid user_id."""
        owner_response = client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        }, follow_redirects=True)
        assert owner_response.status_code == 201
        owner_data = owner_response.get_json()
        assert owner_data is not None
        assert "id" in owner_data
        owner_id = owner_data["id"]
        
        place_response = client.post('/api/v1/places/', json={
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner_id
        })
        place_id = place_response.get_json()["id"]
        
        response = client.post('/api/v1/reviews/', json={
            "text": "Great!",
            "rating": 5,
            "user_id": "non-existent",
            "place_id": place_id
        })
        assert response.status_code == 404

    def test_create_review_invalid_place(self, client):
        """Test POST /api/v1/reviews - invalid place_id."""
        reviewer_response = client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com"
        }, follow_redirects=True)
        assert reviewer_response.status_code == 201
        reviewer_data = reviewer_response.get_json()
        assert reviewer_data is not None
        assert "id" in reviewer_data
        reviewer_id = reviewer_data["id"]
        
        response = client.post('/api/v1/reviews/', json={
            "text": "Great!",
            "rating": 5,
            "user_id": reviewer_id,
            "place_id": "non-existent"
        })
        assert response.status_code == 404

    def test_list_reviews(self, client):
        """Test GET /api/v1/reviews - list all reviews."""
        owner_response = client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        }, follow_redirects=True)
        assert owner_response.status_code == 201
        owner_data = owner_response.get_json()
        assert owner_data is not None
        assert "id" in owner_data
        owner_id = owner_data["id"]
        
        place_response = client.post('/api/v1/places/', json={
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner_id
        }, follow_redirects=True)
        assert place_response.status_code == 201
        place_data = place_response.get_json()
        assert place_data is not None
        assert "id" in place_data
        place_id = place_data["id"]
        
        reviewer_response = client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com"
        }, follow_redirects=True)
        assert reviewer_response.status_code == 201
        reviewer_data = reviewer_response.get_json()
        assert reviewer_data is not None
        assert "id" in reviewer_data
        reviewer_id = reviewer_data["id"]
        
        client.post('/api/v1/reviews/', json={
            "text": "Great!",
            "rating": 5,
            "user_id": reviewer_id,
            "place_id": place_id
        }, follow_redirects=True)
        
        response = client.get('/api/v1/reviews/', follow_redirects=True)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert "user" in data[0]
        assert "place" in data[0]

    def test_get_review_success(self, client):
        """Test GET /api/v1/reviews/<id> - successful retrieval."""
        owner_response = client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        }, follow_redirects=True)
        assert owner_response.status_code == 201
        owner_data = owner_response.get_json()
        assert owner_data is not None
        assert "id" in owner_data
        owner_id = owner_data["id"]
        
        place_response = client.post('/api/v1/places/', json={
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner_id
        }, follow_redirects=True)
        assert place_response.status_code == 201
        place_data = place_response.get_json()
        assert place_data is not None
        assert "id" in place_data
        place_id = place_data["id"]
        
        reviewer_response = client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com"
        }, follow_redirects=True)
        assert reviewer_response.status_code == 201
        reviewer_data = reviewer_response.get_json()
        assert reviewer_data is not None
        assert "id" in reviewer_data
        reviewer_id = reviewer_data["id"]
        
        create_response = client.post('/api/v1/reviews/', json={
            "text": "Great!",
            "rating": 5,
            "user_id": reviewer_id,
            "place_id": place_id
        }, follow_redirects=True)
        assert create_response.status_code == 201
        review_data = create_response.get_json()
        assert review_data is not None
        assert "id" in review_data
        review_id = review_data["id"]
        
        response = client.get(f'/api/v1/reviews/{review_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data["id"] == review_id

    def test_get_review_not_found(self, client):
        """Test GET /api/v1/reviews/<id> - review not found."""
        response = client.get('/api/v1/reviews/non-existent-id')
        assert response.status_code == 404

    def test_update_review_success(self, client):
        """Test PUT /api/v1/reviews/<id> - successful update."""
        owner_response = client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        }, follow_redirects=True)
        assert owner_response.status_code == 201
        owner_data = owner_response.get_json()
        assert owner_data is not None
        assert "id" in owner_data
        owner_id = owner_data["id"]
        
        place_response = client.post('/api/v1/places/', json={
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner_id
        }, follow_redirects=True)
        assert place_response.status_code == 201
        place_data = place_response.get_json()
        assert place_data is not None
        assert "id" in place_data
        place_id = place_data["id"]
        
        reviewer_response = client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com"
        }, follow_redirects=True)
        assert reviewer_response.status_code == 201
        reviewer_data = reviewer_response.get_json()
        assert reviewer_data is not None
        assert "id" in reviewer_data
        reviewer_id = reviewer_data["id"]
        
        create_response = client.post('/api/v1/reviews/', json={
            "text": "Great!",
            "rating": 5,
            "user_id": reviewer_id,
            "place_id": place_id
        }, follow_redirects=True)
        assert create_response.status_code == 201
        review_data = create_response.get_json()
        assert review_data is not None
        assert "id" in review_data
        review_id = review_data["id"]
        
        response = client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Updated text",
            "rating": 4
        }, follow_redirects=True)
        assert response.status_code == 200
        data = response.get_json()
        assert data["text"] == "Updated text"
        assert data["rating"] == 4

    def test_delete_review_success(self, client):
        """Test DELETE /api/v1/reviews/<id> - successful deletion."""
        owner_response = client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        }, follow_redirects=True)
        assert owner_response.status_code == 201
        owner_data = owner_response.get_json()
        assert owner_data is not None
        assert "id" in owner_data
        owner_id = owner_data["id"]
        
        place_response = client.post('/api/v1/places/', json={
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner_id
        }, follow_redirects=True)
        assert place_response.status_code == 201
        place_data = place_response.get_json()
        assert place_data is not None
        assert "id" in place_data
        place_id = place_data["id"]
        
        reviewer_response = client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com"
        }, follow_redirects=True)
        assert reviewer_response.status_code == 201
        reviewer_data = reviewer_response.get_json()
        assert reviewer_data is not None
        assert "id" in reviewer_data
        reviewer_id = reviewer_data["id"]
        
        create_response = client.post('/api/v1/reviews/', json={
            "text": "Great!",
            "rating": 5,
            "user_id": reviewer_id,
            "place_id": place_id
        }, follow_redirects=True)
        assert create_response.status_code == 201
        review_data = create_response.get_json()
        assert review_data is not None
        assert "id" in review_data
        review_id = review_data["id"]
        
        response = client.delete(f'/api/v1/reviews/{review_id}')
        assert response.status_code == 200
        
        # Verify deletion
        get_response = client.get(f'/api/v1/reviews/{review_id}')
        assert get_response.status_code == 404
