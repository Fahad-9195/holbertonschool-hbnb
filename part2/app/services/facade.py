from app.persistence.repository import InMemoryRepository
from app.business_logic.user import User
from app.common.exceptions import ValidationError

class HBnBFacade:
    def __init__(self, repo=None):
        self.repo = repo or InMemoryRepository()

    # ---------- Users ----------
    def create_user(self, data: dict):
        # validation بسيطة
        for f in ("first_name", "last_name", "email"):
            if f not in data or not str(data[f]).strip():
                raise ValidationError(f"Missing field: {f}")

        user = User(
            first_name=data["first_name"].strip(),
            last_name=data["last_name"].strip(),
            email=data["email"].strip(),
        )

        # email لازم يكون unique
        return self.repo.add("users", user, unique_fields=["email"])

    def list_users(self):
        return self.repo.list("users")

    def get_user(self, user_id: str):
        return self.repo.get("users", user_id)
