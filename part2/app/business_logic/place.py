from app.business_logic.base import BaseModel
from app.business_logic.validators import require_str, require_float, require_uuid_str

class Place(BaseModel):
    def __init__(self, name: str, description: str, price, latitude, longitude, owner_id: str):
        super().__init__()
        self.name = require_str(name, "name", max_len=100)
        self.description = require_str(description, "description", max_len=1000)
        self.price = require_float(price, "price", min_v=0.0)
        self.latitude = require_float(latitude, "latitude", min_v=-90.0, max_v=90.0)
        self.longitude = require_float(longitude, "longitude", min_v=-180.0, max_v=180.0)
        self.owner_id = require_uuid_str(owner_id, "owner_id")

        # relationships by IDs
        self.amenity_ids = []  # list[str]
        self.review_ids = []   # list[str]

    def add_amenity(self, amenity_id: str):
        amenity_id = require_uuid_str(amenity_id, "amenity_id")
        if amenity_id not in self.amenity_ids:
            self.amenity_ids.append(amenity_id)
            self.touch()
        return self

    def add_review(self, review_id: str):
        review_id = require_uuid_str(review_id, "review_id")
        if review_id not in self.review_ids:
            self.review_ids.append(review_id)
            self.touch()
        return self

    def update(self, data: dict):
        if "name" in data:
            self.name = require_str(data["name"], "name", max_len=100)
        if "description" in data:
            self.description = require_str(data["description"], "description", max_len=1000)
        if "price" in data:
            self.price = require_float(data["price"], "price", min_v=0.0)
        if "latitude" in data:
            self.latitude = require_float(data["latitude"], "latitude", min_v=-90.0, max_v=90.0)
        if "longitude" in data:
            self.longitude = require_float(data["longitude"], "longitude", min_v=-180.0, max_v=180.0)
        # owner_id عادة ما يتغيرش، لكن لو تبغاه:
        if "owner_id" in data:
            self.owner_id = require_uuid_str(data["owner_id"], "owner_id")

        self.touch()
        return self

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenity_ids": list(self.amenity_ids),
            "review_ids": list(self.review_ids),
        }
