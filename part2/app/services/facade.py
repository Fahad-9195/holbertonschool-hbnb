from app.persistence.repository import InMemoryRepository
from app.business_logic.user import User
from app.business_logic.amenity import Amenity
from app.common.exceptions import ValidationError, ConflictError

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
