"""
Script to fix admin password in the database
This script will:
1. Check if admin user exists
2. Verify/update the admin password hash
3. Ensure the password 'admin1234' works correctly
"""

import sys
import os

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, bcrypt
from app.models.base_model import db, User
from config import DevelopmentConfig

def fix_admin_password():
    """Fix admin password in the database"""
    app = create_app(DevelopmentConfig)
    
    with app.app_context():
        admin_email = 'admin@hbnb.io'
        admin_password = 'admin1234'
        admin_id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
        
        print(f"Checking admin user with email: {admin_email}")
        
        # Try to get admin user by email
        admin_user = User.query.filter_by(email=admin_email).first()
        
        if not admin_user:
            print(f"Admin user not found by email. Trying by ID: {admin_id}")
            admin_user = User.query.filter_by(id=admin_id).first()
        
        if not admin_user:
            print("Admin user not found. Creating new admin user...")
            admin_user = User(
                id=admin_id,
                first_name='Admin',
                last_name='HBnB',
                email=admin_email,
                is_admin=True
            )
            admin_user.hash_password(admin_password)
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print(f"Admin user found: {admin_user.first_name} {admin_user.last_name}")
            print(f"Current email: {admin_user.email}")
            print(f"Is admin: {admin_user.is_admin}")
            
            # Verify current password
            if admin_user.verify_password(admin_password):
                print("Password verification: SUCCESS")
            else:
                print("Password verification: FAILED - Updating password...")
                admin_user.hash_password(admin_password)
                db.session.commit()
                print("Password updated successfully!")
                
                # Verify again
                if admin_user.verify_password(admin_password):
                    print("Password verification after update: SUCCESS")
                else:
                    print("ERROR: Password verification still fails after update!")
                    return False
        
        # Final verification
        print("\n=== Final Verification ===")
        test_user = User.query.filter_by(email=admin_email).first()
        if test_user and test_user.verify_password(admin_password):
            print("SUCCESS: Admin password is working correctly!")
            print(f"Admin ID: {test_user.id}")
            print(f"Admin Email: {test_user.email}")
            print(f"Is Admin: {test_user.is_admin}")
            return True
        else:
            print("ERROR: Final verification failed!")
            return False

if __name__ == '__main__':
    try:
        success = fix_admin_password()
        if success:
            print("\nAdmin password fixed successfully!")
            sys.exit(0)
        else:
            print("\nFailed to fix admin password!")
            sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
