from app.business_logic.base import BaseModel
from app.business_logic.validators import require_str, require_int, require_uuid_str

class Review(BaseModel):
    def __init__(self, text: str, rating, user_id: str, place_id: str):
        super().__init__()
        self.text = require_str(text, "text", max_len=1000)
        self.rating = require_int(rating, "rating", min_v=1, max_v=5)
        self.user_id = require_uuid_str(user_id, "user_id")
        self.place_id = require_uuid_str(place_id, "place_id")

    def update(self, data: dict):
        if "text" in data:
            self.text = require_str(data["text"], "text", max_len=1000)
        if "rating" in data:
            self.rating = require_int(data["rating"], "rating", min_v=1, max_v=5)
        # user_id/place_id عادة ثابتة
        self.touch()
        return self

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
