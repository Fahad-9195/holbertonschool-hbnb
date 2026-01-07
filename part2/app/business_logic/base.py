import uuid
from datetime import datetime, timezone

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def touch(self):
        self.updated_at = datetime.now(timezone.utc)
