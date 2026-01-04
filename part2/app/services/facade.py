from app.persistence.repository import InMemoryRepository
from app.business_logic.user import User
from app.business_logic.amenity import Amenity
from app.business_logic.place import Place
from app.common.exceptions import ValidationError, ConflictError, NotFoundError

class HBnBFacade:
    def __init__(self, repo=None):
        self.repo = repo or InMemoryRepository()

    # ---------- Users ----------
    def create_user(self, data: dict):
        for f in ("first_name", "last_name", "email"):
            if f not in data or not str(data[f]).strip():
                raise ValidationError(f"Missing field: {f}")

        user = User(
            first_name=data["first_name"].strip(),
            last_name=data["last_name"].strip(),
            email=data["email"].strip(),
        )
        return self.repo.add("users", user, unique_fields=["email"])

    def list_users(self):
        return self.repo.list("users")

    def get_user(self, user_id: str):
        return self.repo.get("users", user_id)

    def update_user(self, user_id: str, data: dict):
        user = self.repo.get("users", user_id)

        if "email" in data and str(data["email"]).strip():
            new_email = data["email"].strip()
            for other in self.repo.list("users"):
                if other.id != user_id and getattr(other, "email", None) == new_email:
                    raise ConflictError("users.email must be unique")

        user.update(data)
        return user

    # ---------- Amenities ----------
    def create_amenity(self, data: dict):
        if "name" not in data or not str(data["name"]).strip():
            raise ValidationError("Missing field: name")

        amenity = Amenity(name=data["name"].strip())
        return self.repo.add("amenities", amenity, unique_fields=["name"])

    def list_amenities(self):
        return self.repo.list("amenities")

    def get_amenity(self, amenity_id: str):
        return self.repo.get("amenities", amenity_id)

    def update_amenity(self, amenity_id: str, data: dict):
        amenity = self.repo.get("amenities", amenity_id)

        if "name" in data and str(data["name"]).strip():
            new_name = data["name"].strip()
            for other in self.repo.list("amenities"):
                if other.id != amenity_id and getattr(other, "name", None) == new_name:
                    raise ConflictError("amenities.name must be unique")

        amenity.update(data)
        return amenity

    # ---------- Places ----------
    def _place_out(self, place: Place):
        """Return place with owner + amenities expanded (no reviews in this task)."""
        p = place.to_dict()

        owner = self.get_user(p["owner_id"])
        p["owner"] = {
            "id": owner.id,
            "first_name": owner.first_name,
            "last_name": owner.last_name
        }

        amenities = []
        for aid in p.get("amenity_ids", []):
            a = self.get_amenity(aid)
            amenities.append(a.to_dict())
        p["amenities"] = amenities

        return p

    def create_place(self, data: dict):
        # required fields
        required = ("name", "description", "price", "latitude", "longitude", "owner_id")
        for f in required:
            if f not in data:
                raise ValidationError(f"Missing field: {f}")

        # owner must exist
        self.get_user(data["owner_id"])

        place = Place(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            owner_id=data["owner_id"]
        )

        # amenities (optional)
        amenity_ids = data.get("amenity_ids") or []
        if not isinstance(amenity_ids, list):
            raise ValidationError("amenity_ids must be a list")

        for aid in amenity_ids:
            self.get_amenity(aid)     # must exist
            place.add_amenity(aid)    # dedupe handled inside

        place = self.repo.add("places", place)
        return self._place_out(place)

    def list_places(self):
        return [self._place_out(p) for p in self.repo.list("places")]

    def get_place(self, place_id: str):
        place = self.repo.get("places", place_id)
        return self._place_out(place)

    def update_place(self, place_id: str, data: dict):
        place = self.repo.get("places", place_id)

        # allow updating basic fields (validation inside Place.update)
        place.update(data)

        # allow updating amenities list (optional)
        if "amenity_ids" in data:
            amenity_ids = data.get("amenity_ids") or []
            if not isinstance(amenity_ids, list):
                raise ValidationError("amenity_ids must be a list")

            # reset then re-add (simple behavior)
            place.amenity_ids = []
            for aid in amenity_ids:
                self.get_amenity(aid)
                place.add_amenity(aid)

        return self._place_out(place)
