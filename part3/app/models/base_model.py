from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

# Association table for many-to-many relationship between Place and Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('place.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenity.id'), primary_key=True),
)

class BaseModelDB:
    """Base model for all database entities"""
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class User(BaseModelDB, db.Model):
    """User model"""
    __tablename__ = 'user'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relationships (Task 8)
    # - One-to-many: User -> Places
    # - One-to-many: User -> Reviews
    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    
    def hash_password(self, password):
        """Hashes the password before storing it."""
        from app import bcrypt
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        from app import bcrypt
        return bcrypt.check_password_hash(self.password, password)
    
    def to_dict(self):
        """Convert user to dictionary - excludes password"""
        data = super().to_dict()
        data.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
        })
        return data


class Amenity(BaseModelDB, db.Model):
    """Amenity model"""
    __tablename__ = 'amenity'
    
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)

    # Relationships (Task 8)
    # - Many-to-many: Amenity <-> Places (via association table)
    # Backref 'places' is defined on Place.amenities
    
    def to_dict(self):
        """Convert amenity to dictionary"""
        data = super().to_dict()
        data['name'] = self.name
        return data


class Place(BaseModelDB, db.Model):
    """Place model"""
    __tablename__ = 'place'
    
    # NOTE: API layer expects `name` and `owner_id`
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # Foreign key (Task 8: User -> Place one-to-many)
    owner_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False, index=True)

    # Relationships (Task 8)
    # - One-to-many: Place -> Reviews
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    # - Many-to-many: Place <-> Amenities
    amenities = db.relationship(
        'Amenity',
        secondary=place_amenity,
        lazy='subquery',
        backref=db.backref('places', lazy=True),
    )
    
    def to_dict(self):
        """Convert place to dictionary"""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'amenity_ids': [amenity.id for amenity in (self.amenities or [])],
            'review_ids': [review.id for review in (self.reviews or [])],
        })
        return data


class Review(BaseModelDB, db.Model):
    """Review model"""
    __tablename__ = 'review'
    
    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Foreign keys (Task 8: relationships)
    # - Review belongs to one User
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False, index=True)
    # - Review belongs to one Place
    place_id = db.Column(db.String(36), db.ForeignKey('place.id'), nullable=False, index=True)
    
    def to_dict(self):
        """Convert review to dictionary"""
        data = super().to_dict()
        data.update({
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id,
        })
        return data
