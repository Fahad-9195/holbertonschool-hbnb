from app.business_logic.base import BaseModel
from app.business_logic.validators import require_str

class User(BaseModel):
    def __init__(self, first_name: str, last_name: str, email: str):
        super().__init__()
        self.first_name = require_str(first_name, "first_name", max_len=50)
        self.last_name = require_str(last_name, "last_name", max_len=50)
        self.email = require_str(email, "email", max_len=255)

    def update(self, data: dict):
        if "first_name" in data:
            self.first_name = require_str(data["first_name"], "first_name", max_len=50)
        if "last_name" in data:
            self.last_name = require_str(data["last_name"], "last_name", max_len=50)
        if "email" in data:
            self.email = require_str(data["email"], "email", max_len=255)
        self.touch()
        return self

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
