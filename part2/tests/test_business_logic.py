"""
Unit tests for business logic models.
Tests validation logic for User, Place, Review, and Amenity entities.
"""
import pytest
from app.business_logic.user import User
from app.business_logic.place import Place
from app.business_logic.review import Review
from app.business_logic.amenity import Amenity
from app.business_logic.validators import require_str, require_float, require_int, require_uuid_str


class TestValidators:
    """Test validation helper functions."""

    def test_require_str_valid(self):
        """Test require_str with valid input."""
        result = require_str("test", "field_name")
        assert result == "test"
        assert result == require_str("  test  ", "field_name")  # Should strip

    def test_require_str_none(self):
        """Test require_str with None raises ValueError."""
        with pytest.raises(ValueError, match="field_name is required"):
            require_str(None, "field_name")

    def test_require_str_not_string(self):
        """Test require_str with non-string raises ValueError."""
        with pytest.raises(ValueError, match="field_name must be a string"):
            require_str(123, "field_name")

    def test_require_str_too_short(self):
        """Test require_str with too short string."""
        with pytest.raises(ValueError, match="must be at least"):
            require_str("", "field_name", min_len=1)

    def test_require_str_too_long(self):
        """Test require_str with too long string."""
        with pytest.raises(ValueError, match="must be at most"):
            require_str("a" * 256, "field_name", max_len=255)

    def test_require_float_valid(self):
        """Test require_float with valid input."""
        assert require_float("123.5", "field_name") == 123.5
        assert require_float(123.5, "field_name") == 123.5

    def test_require_float_none(self):
        """Test require_float with None raises ValueError."""
        with pytest.raises(ValueError, match="field_name is required"):
            require_float(None, "field_name")

    def test_require_float_invalid(self):
        """Test require_float with invalid input raises ValueError."""
        with pytest.raises(ValueError, match="must be a number"):
            require_float("not_a_number", "field_name")

    def test_require_float_min_max(self):
        """Test require_float with min/max constraints."""
        assert require_float(5.0, "field_name", min_v=0.0, max_v=10.0) == 5.0
        with pytest.raises(ValueError, match="must be >="):
            require_float(-1.0, "field_name", min_v=0.0)
        with pytest.raises(ValueError, match="must be <="):
            require_float(11.0, "field_name", max_v=10.0)

    def test_require_int_valid(self):
        """Test require_int with valid input."""
        assert require_int("123", "field_name") == 123
        assert require_int(123, "field_name") == 123

    def test_require_int_none(self):
        """Test require_int with None raises ValueError."""
        with pytest.raises(ValueError, match="field_name is required"):
            require_int(None, "field_name")

    def test_require_int_invalid(self):
        """Test require_int with invalid input raises ValueError."""
        with pytest.raises(ValueError, match="must be an integer"):
            require_int("not_an_int", "field_name")

    def test_require_int_min_max(self):
        """Test require_int with min/max constraints."""
        assert require_int(5, "field_name", min_v=1, max_v=5) == 5
        with pytest.raises(ValueError, match="must be >="):
            require_int(0, "field_name", min_v=1)
        with pytest.raises(ValueError, match="must be <="):
            require_int(6, "field_name", max_v=5)


class TestUser:
    """Test User business logic model."""

    def test_create_user_valid(self):
        """Test creating a valid user."""
        user = User("John", "Doe", "john@example.com")
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john@example.com"
        assert user.id is not None

    def test_create_user_strips_whitespace(self):
        """Test that user creation strips whitespace."""
        user = User("  John  ", "  Doe  ", "  john@example.com  ")
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john@example.com"

    def test_create_user_first_name_too_long(self):
        """Test creating user with first_name too long."""
        with pytest.raises(ValueError, match="first_name must be at most"):
            User("a" * 51, "Doe", "john@example.com")

    def test_create_user_last_name_too_long(self):
        """Test creating user with last_name too long."""
        with pytest.raises(ValueError, match="last_name must be at most"):
            User("John", "a" * 51, "john@example.com")

    def test_create_user_email_too_long(self):
        """Test creating user with email too long."""
        with pytest.raises(ValueError, match="email must be at most"):
            User("John", "Doe", "a" * 256)

    def test_create_user_empty_fields(self):
        """Test creating user with empty fields."""
        with pytest.raises(ValueError):
            User("", "Doe", "john@example.com")
        with pytest.raises(ValueError):
            User("John", "", "john@example.com")
        with pytest.raises(ValueError):
            User("John", "Doe", "")

    def test_update_user(self):
        """Test updating user fields."""
        user = User("John", "Doe", "john@example.com")
        user.update({"first_name": "Jane", "last_name": "Smith"})
        assert user.first_name == "Jane"
        assert user.last_name == "Smith"
        assert user.email == "john@example.com"

    def test_to_dict(self):
        """Test user to_dict method."""
        user = User("John", "Doe", "john@example.com")
        data = user.to_dict()
        assert data["first_name"] == "John"
        assert data["last_name"] == "Doe"
        assert data["email"] == "john@example.com"
        assert "id" in data


class TestAmenity:
    """Test Amenity business logic model."""

    def test_create_amenity_valid(self):
        """Test creating a valid amenity."""
        amenity = Amenity("WiFi")
        assert amenity.name == "WiFi"
        assert amenity.id is not None

    def test_create_amenity_strips_whitespace(self):
        """Test that amenity creation strips whitespace."""
        amenity = Amenity("  WiFi  ")
        assert amenity.name == "WiFi"

    def test_create_amenity_name_too_long(self):
        """Test creating amenity with name too long."""
        with pytest.raises(ValueError, match="name must be at most"):
            Amenity("a" * 51)

    def test_create_amenity_empty_name(self):
        """Test creating amenity with empty name."""
        with pytest.raises(ValueError):
            Amenity("")

    def test_update_amenity(self):
        """Test updating amenity."""
        amenity = Amenity("WiFi")
        amenity.update({"name": "Pool"})
        assert amenity.name == "Pool"

    def test_to_dict(self):
        """Test amenity to_dict method."""
        amenity = Amenity("WiFi")
        data = amenity.to_dict()
        assert data["name"] == "WiFi"
        assert "id" in data


class TestPlace:
    """Test Place business logic model."""

    def test_create_place_valid(self):
        """Test creating a valid place."""
        place = Place("My Place", "Description", 100.0, 40.7128, -74.0060, "owner-123")
        assert place.name == "My Place"
        assert place.description == "Description"
        assert place.price == 100.0
        assert place.latitude == 40.7128
        assert place.longitude == -74.0060
        assert place.owner_id == "owner-123"
        assert place.amenity_ids == []
        assert place.review_ids == []

    def test_create_place_name_too_long(self):
        """Test creating place with name too long."""
        with pytest.raises(ValueError, match="name must be at most"):
            Place("a" * 101, "Description", 100.0, 40.7128, -74.0060, "owner-123")

    def test_create_place_description_too_long(self):
        """Test creating place with description too long."""
        with pytest.raises(ValueError, match="description must be at most"):
            Place("Name", "a" * 1001, 100.0, 40.7128, -74.0060, "owner-123")

    def test_create_place_negative_price(self):
        """Test creating place with negative price."""
        with pytest.raises(ValueError, match="price must be >="):
            Place("Name", "Description", -10.0, 40.7128, -74.0060, "owner-123")

    def test_create_place_invalid_latitude(self):
        """Test creating place with invalid latitude."""
        with pytest.raises(ValueError, match="latitude must be"):
            Place("Name", "Description", 100.0, 91.0, -74.0060, "owner-123")
        with pytest.raises(ValueError, match="latitude must be"):
            Place("Name", "Description", 100.0, -91.0, -74.0060, "owner-123")

    def test_create_place_invalid_longitude(self):
        """Test creating place with invalid longitude."""
        with pytest.raises(ValueError, match="longitude must be"):
            Place("Name", "Description", 100.0, 40.7128, 181.0, "owner-123")
        with pytest.raises(ValueError, match="longitude must be"):
            Place("Name", "Description", 100.0, 40.7128, -181.0, "owner-123")

    def test_add_amenity(self):
        """Test adding amenity to place."""
        place = Place("Name", "Description", 100.0, 40.7128, -74.0060, "owner-123")
        place.add_amenity("amenity-1")
        assert "amenity-1" in place.amenity_ids
        place.add_amenity("amenity-1")  # Should not duplicate
        assert place.amenity_ids.count("amenity-1") == 1

    def test_add_review(self):
        """Test adding review to place."""
        place = Place("Name", "Description", 100.0, 40.7128, -74.0060, "owner-123")
        place.add_review("review-1")
        assert "review-1" in place.review_ids

    def test_update_place(self):
        """Test updating place fields."""
        place = Place("Name", "Description", 100.0, 40.7128, -74.0060, "owner-123")
        place.update({"name": "New Name", "price": 150.0})
        assert place.name == "New Name"
        assert place.price == 150.0

    def test_to_dict(self):
        """Test place to_dict method."""
        place = Place("Name", "Description", 100.0, 40.7128, -74.0060, "owner-123")
        data = place.to_dict()
        assert data["name"] == "Name"
        assert data["price"] == 100.0
        assert "id" in data
        assert "amenity_ids" in data
        assert "review_ids" in data


class TestReview:
    """Test Review business logic model."""

    def test_create_review_valid(self):
        """Test creating a valid review."""
        review = Review("Great place!", 5, "user-123", "place-123")
        assert review.text == "Great place!"
        assert review.rating == 5
        assert review.user_id == "user-123"
        assert review.place_id == "place-123"

    def test_create_review_text_too_long(self):
        """Test creating review with text too long."""
        with pytest.raises(ValueError, match="text must be at most"):
            Review("a" * 1001, 5, "user-123", "place-123")

    def test_create_review_rating_too_low(self):
        """Test creating review with rating too low."""
        with pytest.raises(ValueError, match="rating must be >="):
            Review("Text", 0, "user-123", "place-123")

    def test_create_review_rating_too_high(self):
        """Test creating review with rating too high."""
        with pytest.raises(ValueError, match="rating must be <="):
            Review("Text", 6, "user-123", "place-123")

    def test_create_review_rating_valid_range(self):
        """Test creating review with valid rating range."""
        for rating in [1, 2, 3, 4, 5]:
            review = Review("Text", rating, "user-123", "place-123")
            assert review.rating == rating

    def test_update_review(self):
        """Test updating review fields."""
        review = Review("Text", 3, "user-123", "place-123")
        review.update({"text": "New text", "rating": 4})
        assert review.text == "New text"
        assert review.rating == 4

    def test_to_dict(self):
        """Test review to_dict method."""
        review = Review("Text", 5, "user-123", "place-123")
        data = review.to_dict()
        assert data["text"] == "Text"
        assert data["rating"] == 5
        assert data["user_id"] == "user-123"
        assert data["place_id"] == "place-123"
        assert "id" in data
