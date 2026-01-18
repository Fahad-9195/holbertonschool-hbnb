#!/usr/bin/env python
"""Database initialization script for HBnB application Part 3"""

import os
from dotenv import load_dotenv
from app import create_app
from app.models.base_model import db, User, Amenity, Place, Review

load_dotenv()

def init_db():
    """Initialize the database"""
    # Map FLASK_ENV to config class
    env = os.getenv('FLASK_ENV', 'development')
    config_map = {
        'development': 'config.DevelopmentConfig',
        'production': 'config.ProductionConfig',
        'testing': 'config.TestingConfig'
    }
    config_class = config_map.get(env, 'config.DevelopmentConfig')
    
    app = create_app(config_class)
    
    with app.app_context():
        # Drop all tables (development only!)
        print("Dropping existing tables...")
        db.drop_all()
        
        # Create all tables
        print("Creating tables...")
        db.create_all()
        print("Tables created successfully!")
        
        # Add sample data
        print("Adding sample data...")
        
        # Create sample users
        admin_user = User(
            first_name="Admin",
            last_name="User",
            email="admin@hbnb.com",
            is_admin=True
        )
        admin_user.hash_password("admin123")
        
        user1 = User(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            is_admin=False
        )
        user1.hash_password("password123")
        
        user2 = User(
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            is_admin=False
        )
        user2.hash_password("password123")
        
        db.session.add_all([admin_user, user1, user2])
        db.session.commit()
        print(f"Created 3 users")
        
        # Create sample amenities
        amenity1 = Amenity(name="WiFi")
        amenity2 = Amenity(name="Pool")
        amenity3 = Amenity(name="Gym")
        amenity4 = Amenity(name="Parking")
        
        db.session.add_all([amenity1, amenity2, amenity3, amenity4])
        db.session.commit()
        print(f"Created 4 amenities")
        
        # Create sample places
        place1 = Place(
            name="Cozy Apartment",
            description="A beautiful cozy apartment in the heart of the city",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=user1.id
        )
        place1.amenities.append(amenity1)
        place1.amenities.append(amenity4)
        
        place2 = Place(
            name="Luxury Villa",
            description="A stunning luxury villa with pool and gym",
            price=250.0,
            latitude=51.5074,
            longitude=-0.1278,
            owner_id=user2.id
        )
        place2.amenities.append(amenity2)
        place2.amenities.append(amenity3)
        
        db.session.add_all([place1, place2])
        db.session.commit()
        print(f"Created 2 places")
        
        # Create sample reviews
        review1 = Review(
            text="Great place! Very clean and comfortable.",
            rating=5,
            user_id=user2.id,
            place_id=place1.id
        )
        
        review2 = Review(
            text="Amazing villa! Would definitely stay again.",
            rating=5,
            user_id=user1.id,
            place_id=place2.id
        )
        
        db.session.add_all([review1, review2])
        db.session.commit()
        print(f"Created 2 reviews")
        
        print("\nDatabase initialized successfully!")
        print("\nSample credentials:")
        print("Admin - Email: admin@hbnb.com, Password: admin123")
        print("User1 - Email: john@example.com, Password: password123")
        print("User2 - Email: jane@example.com, Password: password123")

if __name__ == "__main__":
    init_db()
