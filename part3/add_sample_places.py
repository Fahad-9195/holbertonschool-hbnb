"""
Script to add sample places to the database for testing
Run this script to populate the database with sample places
"""

import sys
import os
from datetime import datetime
import uuid

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from config import DevelopmentConfig
from app.models.base_model import db, Place, User
from app.persistence.repository import UserRepository, PlaceRepository

# Sample places data
SAMPLE_PLACES = [
    {
        "name": "Cozy Apartment in Downtown",
        "description": "Beautiful modern apartment in the heart of the city. Perfect for couples or solo travelers. Fully furnished with all amenities.",
        "price": 85.00,
        "latitude": 40.7128,
        "longitude": -74.0060,  # New York City
    },
    {
        "name": "Beachfront Villa",
        "description": "Stunning beachfront property with ocean views. Private beach access, infinity pool, and modern amenities. Perfect for a relaxing getaway.",
        "price": 250.00,
        "latitude": 25.7617,
        "longitude": -80.1918,  # Miami
    },
    {
        "name": "Mountain Cabin Retreat",
        "description": "Peaceful mountain cabin surrounded by nature. Great for hiking enthusiasts. Cozy fireplace, fully equipped kitchen, and breathtaking mountain views.",
        "price": 120.00,
        "latitude": 39.7392,
        "longitude": -104.9903,  # Denver
    },
    {
        "name": "Luxury Penthouse Suite",
        "description": "Elegant penthouse with panoramic city views. High-end finishes, private terrace, and concierge service. The ultimate urban experience.",
        "price": 350.00,
        "latitude": 37.7749,
        "longitude": -122.4194,  # San Francisco
    },
    {
        "name": "Rustic Countryside House",
        "description": "Charming countryside house with large garden. Perfect for families. Close to nature, peaceful surroundings, and traditional architecture.",
        "price": 95.00,
        "latitude": 38.9072,
        "longitude": -77.0369,  # Washington DC
    },
    {
        "name": "Modern Studio in Arts District",
        "description": "Stylish studio apartment in the vibrant arts district. Walking distance to galleries, restaurants, and nightlife. Perfect for creative souls.",
        "price": 75.00,
        "latitude": 34.0522,
        "longitude": -118.2437,  # Los Angeles
    },
    {
        "name": "Historic Townhouse",
        "description": "Beautifully restored historic townhouse with original features. Elegant decor, spacious rooms, and rich history. A unique stay experience.",
        "price": 180.00,
        "latitude": 41.8781,
        "longitude": -87.6298,  # Chicago
    },
    {
        "name": "Tropical Paradise Bungalow",
        "description": "Private bungalow in tropical setting. Surrounded by palm trees, private pool, and outdoor shower. Your own slice of paradise.",
        "price": 200.00,
        "latitude": 21.3099,
        "longitude": -157.8581,  # Honolulu
    },
]

def add_sample_places():
    """Add sample places to the database"""
    app = create_app(DevelopmentConfig)
    
    with app.app_context():
        # Get or create a user to own the places
        user_repo = UserRepository()
        
        # Try to get the admin user first
        try:
            admin_user = user_repo.get_by_email('admin@hbnb.io')
            owner_id = admin_user.id
            print(f"Using admin user: {admin_user.email}")
        except Exception:
            # If admin doesn't exist, get the first user
            users = user_repo.list_all()
            if not users:
                print("ERROR: No users found in database. Please create a user first (register via the web interface).")
                return
            owner_id = users[0].id
            print(f"Using first available user: {users[0].email}")
        
        place_repo = PlaceRepository()
        
        # Check if places already exist
        existing_places = place_repo.list_all()
        if existing_places:
            print(f"\nFound {len(existing_places)} existing places in database.")
            print("Adding more sample places...")
        
        # Add sample places
        added_count = 0
        for place_data in SAMPLE_PLACES:
            try:
                # Check if place with same name already exists
                existing = Place.query.filter_by(name=place_data['name']).first()
                if existing:
                    print(f"  - Skipping '{place_data['name']}' (already exists)")
                    continue
                
                # Create new place
                place = Place(
                    id=str(uuid.uuid4()),
                    name=place_data['name'],
                    description=place_data['description'],
                    price=place_data['price'],
                    latitude=place_data['latitude'],
                    longitude=place_data['longitude'],
                    owner_id=owner_id,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                
                place_repo.add(place)
                added_count += 1
                print(f"  [+] Added: {place_data['name']} (${place_data['price']}/night)")
                
            except Exception as e:
                print(f"  [-] Error adding '{place_data['name']}': {str(e)}")
        
        print(f"\n[SUCCESS] Successfully added {added_count} sample places!")
        print(f"Total places in database: {len(place_repo.list_all())}")

if __name__ == '__main__':
    print("=" * 60)
    print("HBnB - Add Sample Places")
    print("=" * 60)
    print()
    add_sample_places()
    print()
    print("Done! You can now view the places in the web interface.")
