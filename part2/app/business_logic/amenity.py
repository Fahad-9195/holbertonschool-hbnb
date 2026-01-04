from app.business_logic.base import BaseModel
from app.business_logic.validators import require_str

class Amenity(BaseModel):
    def __init__(self, name: str):
        super().__init__()
        self.name = require_str(name, "name", max_len=50)

    def update(self, data: dict):
        if "name" in data:
            self.name = require_str(data["name"], "name", max_len=50)
        self.touch()
        return self

    def to_dict(self):
        return {"id": self.id, "name": self.name}
