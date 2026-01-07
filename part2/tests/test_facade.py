"""
Unit tests for the HBnBFacade service layer.
Tests business logic operations and relationships between entities.
"""
import pytest
from app.services.facade import HBnBFacade
from app.persistence.repository import InMemoryRepository
from app.common.exceptions import ValidationError, ConflictError, NotFoundError


@pytest.fixture
def facade():
    """Create a fresh facade instance for each test."""
    repo = InMemoryRepository()
    return HBnBFacade(repo)


class TestUserFacade:
    """Test user-related facade operations."""

    def test_create_user_success(self, facade):
        """Test successfully creating a user."""
        user = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john@example.com"

    def test_create_user_missing_fields(self, facade):
        """Test creating user with missing required fields."""
        with pytest.raises(ValidationError):
            facade.create_user({"first_name": "John"})
        with pytest.raises(ValidationError):
            facade.create_user({"first_name": "John", "last_name": "Doe"})

    def test_create_user_empty_fields(self, facade):
        """Test creating user with empty fields."""
        with pytest.raises(ValidationError):
            facade.create_user({
                "first_name": "",
                "last_name": "Doe",
                "email": "john@example.com"
            })

    def test_create_user_duplicate_email(self, facade):
        """Test creating user with duplicate email."""
        facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        with pytest.raises(ConflictError):
            facade.create_user({
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "john@example.com"
            })

    def test_list_users(self, facade):
        """Test listing all users."""
        facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        facade.create_user({
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com"
        })
        users = facade.list_users()
        assert len(users) == 2

    def test_get_user_success(self, facade):
        """Test getting a user by ID."""
        user = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        retrieved = facade.get_user(user.id)
        assert retrieved.id == user.id
        assert retrieved.email == user.email

    def test_get_user_not_found(self, facade):
        """Test getting non-existent user."""
        with pytest.raises(NotFoundError):
            facade.get_user("non-existent-id")

    def test_update_user_success(self, facade):
        """Test updating a user."""
        user = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        updated = facade.update_user(user.id, {"first_name": "Jane"})
        assert updated.first_name == "Jane"
        assert updated.last_name == "Doe"  # Unchanged

    def test_update_user_duplicate_email(self, facade):
        """Test updating user with duplicate email."""
        user1 = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        user2 = facade.create_user({
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com"
        })
        with pytest.raises(ConflictError):
            facade.update_user(user1.id, {"email": "jane@example.com"})


class TestAmenityFacade:
    """Test amenity-related facade operations."""

    def test_create_amenity_success(self, facade):
        """Test successfully creating an amenity."""
        amenity = facade.create_amenity({"name": "WiFi"})
        assert amenity.name == "WiFi"

    def test_create_amenity_missing_name(self, facade):
        """Test creating amenity without name."""
        with pytest.raises(ValidationError):
            facade.create_amenity({})

    def test_create_amenity_duplicate_name(self, facade):
        """Test creating amenity with duplicate name."""
        facade.create_amenity({"name": "WiFi"})
        with pytest.raises(ConflictError):
            facade.create_amenity({"name": "WiFi"})

    def test_list_amenities(self, facade):
        """Test listing all amenities."""
        facade.create_amenity({"name": "WiFi"})
        facade.create_amenity({"name": "Pool"})
        amenities = facade.list_amenities()
        assert len(amenities) == 2

    def test_get_amenity_success(self, facade):
        """Test getting an amenity by ID."""
        amenity = facade.create_amenity({"name": "WiFi"})
        retrieved = facade.get_amenity(amenity.id)
        assert retrieved.id == amenity.id

    def test_get_amenity_not_found(self, facade):
        """Test getting non-existent amenity."""
        with pytest.raises(NotFoundError):
            facade.get_amenity("non-existent-id")

    def test_update_amenity_success(self, facade):
        """Test updating an amenity."""
        amenity = facade.create_amenity({"name": "WiFi"})
        updated = facade.update_amenity(amenity.id, {"name": "Free WiFi"})
        assert updated.name == "Free WiFi"

    def test_update_amenity_duplicate_name(self, facade):
        """Test updating amenity with duplicate name."""
        amenity1 = facade.create_amenity({"name": "WiFi"})
        amenity2 = facade.create_amenity({"name": "Pool"})
        with pytest.raises(ConflictError):
            facade.update_amenity(amenity1.id, {"name": "Pool"})


class TestPlaceFacade:
    """Test place-related facade operations."""

    def test_create_place_success(self, facade):
        """Test successfully creating a place."""
        owner = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        place = facade.create_place({
            "name": "Beautiful Apartment",
            "description": "A nice place",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner.id
        })
        assert place["name"] == "Beautiful Apartment"
        assert place["owner"]["id"] == owner.id
        assert place["owner"]["first_name"] == "John"

    def test_create_place_missing_fields(self, facade):
        """Test creating place with missing required fields."""
        owner = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        with pytest.raises(ValidationError):
            facade.create_place({
                "name": "Place",
                "owner_id": owner.id
            })

    def test_create_place_invalid_owner(self, facade):
        """Test creating place with non-existent owner."""
        with pytest.raises(NotFoundError):
            facade.create_place({
                "name": "Place",
                "description": "Desc",
                "price": 100.0,
                "latitude": 40.7128,
                "longitude": -74.0060,
                "owner_id": "non-existent"
            })

    def test_create_place_with_amenities(self, facade):
        """Test creating place with amenities."""
        owner = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        amenity1 = facade.create_amenity({"name": "WiFi"})
        amenity2 = facade.create_amenity({"name": "Pool"})
        place = facade.create_place({
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner.id,
            "amenity_ids": [amenity1.id, amenity2.id]
        })
        assert len(place["amenities"]) == 2

    def test_create_place_invalid_amenity(self, facade):
        """Test creating place with non-existent amenity."""
        owner = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        with pytest.raises(NotFoundError):
            facade.create_place({
                "name": "Place",
                "description": "Desc",
                "price": 100.0,
                "latitude": 40.7128,
                "longitude": -74.0060,
                "owner_id": owner.id,
                "amenity_ids": ["non-existent"]
            })

    def test_list_places(self, facade):
        """Test listing all places."""
        owner = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        facade.create_place({
            "name": "Place 1",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner.id
        })
        places = facade.list_places()
        assert len(places) == 1
        assert "owner" in places[0]
        assert "amenities" in places[0]

    def test_get_place_success(self, facade):
        """Test getting a place by ID."""
        owner = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        place = facade.create_place({
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner.id
        })
        retrieved = facade.get_place(place["id"])
        assert retrieved["id"] == place["id"]
        assert retrieved["owner"]["id"] == owner.id

    def test_update_place_success(self, facade):
        """Test updating a place."""
        owner = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        place = facade.create_place({
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner.id
        })
        updated = facade.update_place(place["id"], {"name": "New Name", "price": 150.0})
        assert updated["name"] == "New Name"
        assert updated["price"] == 150.0


class TestReviewFacade:
    """Test review-related facade operations."""

    def test_create_review_success(self, facade):
        """Test successfully creating a review."""
        owner = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        place = facade.create_place({
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner.id
        })
        reviewer = facade.create_user({
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com"
        })
        review = facade.create_review({
            "text": "Great place!",
            "rating": 5,
            "user_id": reviewer.id,
            "place_id": place["id"]
        })
        assert review["text"] == "Great place!"
        assert review["rating"] == 5
        assert review["user"]["id"] == reviewer.id
        assert review["place"]["id"] == place["id"]

    def test_create_review_missing_fields(self, facade):
        """Test creating review with missing required fields."""
        with pytest.raises(ValidationError):
            facade.create_review({"text": "Great!"})

    def test_create_review_invalid_user(self, facade):
        """Test creating review with non-existent user."""
        owner = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        place = facade.create_place({
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner.id
        })
        with pytest.raises(NotFoundError):
            facade.create_review({
                "text": "Great!",
                "rating": 5,
                "user_id": "non-existent",
                "place_id": place["id"]
            })

    def test_create_review_invalid_place(self, facade):
        """Test creating review with non-existent place."""
        reviewer = facade.create_user({
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com"
        })
        with pytest.raises(NotFoundError):
            facade.create_review({
                "text": "Great!",
                "rating": 5,
                "user_id": reviewer.id,
                "place_id": "non-existent"
            })

    def test_list_reviews(self, facade):
        """Test listing all reviews."""
        owner = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        place = facade.create_place({
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner.id
        })
        reviewer = facade.create_user({
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com"
        })
        facade.create_review({
            "text": "Great!",
            "rating": 5,
            "user_id": reviewer.id,
            "place_id": place["id"]
        })
        reviews = facade.list_reviews()
        assert len(reviews) == 1
        assert "user" in reviews[0]
        assert "place" in reviews[0]

    def test_get_review_success(self, facade):
        """Test getting a review by ID."""
        owner = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        place = facade.create_place({
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner.id
        })
        reviewer = facade.create_user({
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com"
        })
        review = facade.create_review({
            "text": "Great!",
            "rating": 5,
            "user_id": reviewer.id,
            "place_id": place["id"]
        })
        retrieved = facade.get_review(review["id"])
        assert retrieved["id"] == review["id"]

    def test_update_review_success(self, facade):
        """Test updating a review."""
        owner = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        place = facade.create_place({
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner.id
        })
        reviewer = facade.create_user({
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com"
        })
        review = facade.create_review({
            "text": "Great!",
            "rating": 5,
            "user_id": reviewer.id,
            "place_id": place["id"]
        })
        updated = facade.update_review(review["id"], {"text": "Updated text", "rating": 4})
        assert updated["text"] == "Updated text"
        assert updated["rating"] == 4

    def test_delete_review_success(self, facade):
        """Test deleting a review."""
        owner = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        place = facade.create_place({
            "name": "Place",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner.id
        })
        reviewer = facade.create_user({
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com"
        })
        review = facade.create_review({
            "text": "Great!",
            "rating": 5,
            "user_id": reviewer.id,
            "place_id": place["id"]
        })
        result = facade.delete_review(review["id"])
        assert result["message"] == "Review deleted successfully"
        with pytest.raises(NotFoundError):
            facade.get_review(review["id"])

    def test_list_reviews_by_place(self, facade):
        """Test listing reviews for a specific place."""
        owner = facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        place1 = facade.create_place({
            "name": "Place 1",
            "description": "Desc",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner.id
        })
        place2 = facade.create_place({
            "name": "Place 2",
            "description": "Desc",
            "price": 200.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner.id
        })
        reviewer = facade.create_user({
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com"
        })
        review1 = facade.create_review({
            "text": "Great!",
            "rating": 5,
            "user_id": reviewer.id,
            "place_id": place1["id"]
        })
        review2 = facade.create_review({
            "text": "Nice!",
            "rating": 4,
            "user_id": reviewer.id,
            "place_id": place1["id"]
        })
        facade.create_review({
            "text": "OK",
            "rating": 3,
            "user_id": reviewer.id,
            "place_id": place2["id"]
        })
        place1_reviews = facade.list_reviews_by_place(place1["id"])
        assert len(place1_reviews) == 2
        assert all(r["place_id"] == place1["id"] for r in place1_reviews)
