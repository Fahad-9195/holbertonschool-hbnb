from app.business_logic.base import BaseModel

class Amenity(BaseModel):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
