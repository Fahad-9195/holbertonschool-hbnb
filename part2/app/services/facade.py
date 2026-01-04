from app.persistence.repository import InMemoryRepository
from app.business_logic.user import User
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

        # تحقق email unique لو انرسل
        if "email" in data and str(data["email"]).strip():
            new_email = data["email"].strip()
            for other in self.repo.list("users"):
                if other.id != user_id and getattr(other, "email", None) == new_email:
                    raise ConflictError("users.email must be unique")

        user.update(data)  # validation داخل الكلاس
        return user
