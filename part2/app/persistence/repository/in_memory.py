from app.common.exceptions import NotFoundError, ConflictError, ValidationError

class InMemoryRepository:
    """
    Generic in-memory repository.
    Stores objects by: { entity_name: { id: obj } }
    """

    def __init__(self):
        self._data = {}

    def _bucket(self, entity_name: str) -> dict:
        if entity_name not in self._data:
            self._data[entity_name] = {}
        return self._data[entity_name]

    def add(self, entity_name: str, obj, unique_fields=None):
        bucket = self._bucket(entity_name)

        if not getattr(obj, "id", None):
            raise ValidationError("Object must have an id")

        if unique_fields:
            for existing in bucket.values():
                for field in unique_fields:
                    if getattr(existing, field, None) == getattr(obj, field, None):
                        raise ConflictError(f"{entity_name}.{field} must be unique")

        if obj.id in bucket:
            raise ConflictError(f"{entity_name} with id already exists")

        bucket[obj.id] = obj
        return obj

    def get(self, entity_name: str, obj_id: str):
        bucket = self._bucket(entity_name)
        obj = bucket.get(obj_id)
        if not obj:
            raise NotFoundError(f"{entity_name} not found")
        return obj

    def list(self, entity_name: str):
        bucket = self._bucket(entity_name)
        return list(bucket.values())

    def update(self, entity_name: str, obj_id: str, data: dict):
        obj = self.get(entity_name, obj_id)
        for k, v in data.items():
            if k == "id":
                continue
            if hasattr(obj, k):
                setattr(obj, k, v)
        if hasattr(obj, "touch") and callable(getattr(obj, "touch")):
            obj.touch()
        return obj

    def delete(self, entity_name: str, obj_id: str):
        bucket = self._bucket(entity_name)
        if obj_id not in bucket:
            raise NotFoundError(f"{entity_name} not found")
        return bucket.pop(obj_id)
