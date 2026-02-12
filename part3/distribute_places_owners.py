"""
Script to create multiple users and distribute places ownership
Creates: Fahad Alshammari, Fahad Al-Ghamdi, Nabil Al-Duwaisi
Distributes existing places among them
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from config import DevelopmentConfig
from app.models.base_model import db, Place, User
from app.persistence.repository import UserRepository, PlaceRepository

# Users to create
USERS = [
    {
        "first_name": "Fahad",
        "last_name": "Alshammari",
        "email": "fahad.alshammari@hbnb.io",
        "password": "password123"
    },
    {
        "first_name": "Fahad",
        "last_name": "Al-Ghamdi",
        "email": "fahad.alghamdi@hbnb.io",
        "password": "password123"
    },
    {
        "first_name": "Nabil",
        "last_name": "Al-Duwaisi",
        "email": "nabil.alduwaisi@hbnb.io",
        "password": "password123"
    }
]

def distribute_places():
    """Create users and distribute places among them"""
    app = create_app(DevelopmentConfig)
    
    with app.app_context():
        user_repo = UserRepository()
        place_repo = PlaceRepository()
        
        print("=" * 60)
        print("HBnB - Distribute Places Ownership")
        print("=" * 60)
        print()
        
        # Step 1: Create or get users
        user_ids = []
        for user_data in USERS:
            try:
                # Check if user exists
                user = user_repo.get_by_email(user_data['email'])
                print(f"User already exists: {user.first_name} {user.last_name} ({user.email})")
                user_ids.append(user.id)
            except Exception:
                # Create new user
                user = User(
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email=user_data['email'],
                    is_admin=False
                )
                user.hash_password(user_data['password'])
                created_user = user_repo.add(user)
                user_ids.append(created_user.id)
                print(f"Created user: {created_user.first_name} {created_user.last_name} ({created_user.email})")
        
        print(f"\nTotal users: {len(user_ids)}")
        print()
        
        # Step 2: Get all places
        all_places = place_repo.list_all()
        print(f"Found {len(all_places)} places in database")
        
        if not all_places:
            print("No places found. Please add places first using add_sample_places.py")
            return
        
        # Step 3: Distribute places among users
        print("\nDistributing places...")
        updated_count = 0
        
        for index, place in enumerate(all_places):
            # Distribute evenly: place 0 -> user 0, place 1 -> user 1, place 2 -> user 2, place 3 -> user 0, etc.
            owner_index = index % len(user_ids)
            new_owner_id = user_ids[owner_index]
            
            # Get owner name for display
            owner = user_repo.get(new_owner_id)
            owner_name = f"{owner.first_name} {owner.last_name}"
            
            # Update place owner
            place.owner_id = new_owner_id
            db.session.commit()
            
            updated_count += 1
            print(f"  [{updated_count}] '{place.name}' -> {owner_name}")
        
        print(f"\n[SUCCESS] Distributed {updated_count} places among {len(user_ids)} users!")
        print()
        
        # Step 4: Show summary
        print("Ownership Summary:")
        print("-" * 60)
        for i, user_id in enumerate(user_ids):
            owner = user_repo.get(user_id)
            owner_places = Place.query.filter_by(owner_id=user_id).all()
            print(f"{owner.first_name} {owner.last_name}: {len(owner_places)} places")
            for place in owner_places:
                print(f"  - {place.name}")

if __name__ == '__main__':
    try:
        distribute_places()
        print("\nDone!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
