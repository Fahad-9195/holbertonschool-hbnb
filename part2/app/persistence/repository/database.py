from app.models import db, User, Place, Review, Amenity
from app.common.exceptions import NotFoundError, ConflictError, ValidationError
from sqlalchemy.exc import IntegrityError

class Repository:
    """Base repository for database operations"""
    
    def __init__(self, model):
        self.model = model
    
    def add(self, obj, commit=True):
        """Add an object to the database"""
        try:
            db.session.add(obj)
            if commit:
                db.session.commit()
            return obj
        except IntegrityError as e:
            db.session.rollback()
            if 'UNIQUE constraint failed' in str(e) or 'Duplicate entry' in str(e):
                raise ConflictError(f"A {self.model.__name__} with this data already exists")
            raise ValidationError(str(e))
    
    def get(self, obj_id: str):
        """Get an object by ID"""
        obj = self.model.query.get(obj_id)
        if not obj:
            raise NotFoundError(f"{self.model.__name__} not found")
        return obj
    
    def list_all(self):
        """List all objects"""
        return self.model.query.all()
    
    def update(self, obj_id: str, data: dict):
        """Update an object"""
        obj = self.get(obj_id)
        for key, value in data.items():
            if key != 'id' and hasattr(obj, key):
                setattr(obj, key, value)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise ConflictError(f"Update failed: {str(e)}")
        return obj
    
    def delete(self, obj_id: str):
        """Delete an object"""
        obj = self.get(obj_id)
        db.session.delete(obj)
        db.session.commit()
        return obj
    
    def delete_all(self):
        """Delete all objects (useful for testing)"""
        self.model.query.delete()
        db.session.commit()


class UserRepository(Repository):
    """Repository for User operations"""
    
    def __init__(self):
        super().__init__(User)
    
    def get_by_email(self, email: str):
        """Get a user by email"""
        user = User.query.filter_by(email=email).first()
        if not user:
            raise NotFoundError("User not found")
        return user
    
    def email_exists(self, email: str, exclude_id: str = None) -> bool:
        """Check if email already exists"""
        query = User.query.filter_by(email=email)
        if exclude_id:
            query = query.filter(User.id != exclude_id)
        return query.first() is not None


class PlaceRepository(Repository):
    """Repository for Place operations"""
    
    def __init__(self):
        super().__init__(Place)
    
    def get_by_owner(self, owner_id: str):
        """Get all places by owner ID"""
        return Place.query.filter_by(owner_id=owner_id).all()


class ReviewRepository(Repository):
    """Repository for Review operations"""
    
    def __init__(self):
        super().__init__(Review)
    
    def get_by_place(self, place_id: str):
        """Get all reviews for a place"""
        return Review.query.filter_by(place_id=place_id).all()
    
    def get_by_user(self, user_id: str):
        """Get all reviews by a user"""
        return Review.query.filter_by(user_id=user_id).all()


class AmenityRepository(Repository):
    """Repository for Amenity operations"""
    
    def __init__(self):
        super().__init__(Amenity)
    
    def get_by_name(self, name: str):
        """Get amenity by name"""
        amenity = Amenity.query.filter_by(name=name).first()
        if not amenity:
            raise NotFoundError("Amenity not found")
        return amenity
    
    def name_exists(self, name: str, exclude_id: str = None) -> bool:
        """Check if name already exists"""
        query = Amenity.query.filter_by(name=name)
        if exclude_id:
            query = query.filter(Amenity.id != exclude_id)
        return query.first() is not None
