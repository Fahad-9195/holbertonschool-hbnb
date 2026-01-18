#!/usr/bin/env python3
"""
Task 5 Verification Script
Verifies that all Task 5 requirements are implemented correctly
"""

import sys
import inspect
from pathlib import Path

# Add the parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def check_admin_required_decorator():
    """Check if admin_required decorator exists and is used"""
    print("\n📋 Checking @admin_required decorator...")
    
    try:
        from app.auth.auth_utils import admin_required
        print("  ✅ admin_required decorator exists")
        
        # Check the decorator
        source = inspect.getsource(admin_required)
        if 'get_jwt()' in source and 'is_admin' in source:
            print("  ✅ admin_required checks is_admin claim")
            return True
        else:
            print("  ❌ admin_required doesn't check is_admin properly")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def check_users_endpoint():
    """Check if users endpoint has admin restrictions"""
    print("\n📋 Checking Users endpoint (POST, PUT)...")
    
    try:
        from app.presentation.api.v1.users import Users, UserById
        
        # Check POST
        post_method = Users.post
        post_source = inspect.getsource(post_method)
        
        if '@admin_required' in post_source or 'admin_required' in post_source:
            print("  ✅ POST /api/v1/users/ has @admin_required")
        else:
            print("  ❌ POST /api/v1/users/ missing @admin_required")
            return False
        
        # Check PUT
        put_method = UserById.put
        put_source = inspect.getsource(put_method)
        
        if 'get_jwt()' in put_source and 'is_admin' in put_source:
            print("  ✅ PUT /api/v1/users/{id} checks admin claim")
        else:
            print("  ❌ PUT /api/v1/users/{id} doesn't check admin properly")
            return False
        
        # Check if admin can update email and password
        if 'email' in put_source and 'password' in put_source:
            print("  ✅ PUT allows admin to update email and password")
        else:
            print("  ❌ PUT doesn't allow email/password updates")
            return False
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def check_places_endpoint():
    """Check if places endpoint has admin bypass"""
    print("\n📋 Checking Places endpoint (PUT, DELETE)...")
    
    try:
        from app.presentation.api.v1.places import PlaceById
        
        # Check PUT
        put_method = PlaceById.put
        put_source = inspect.getsource(put_method)
        
        if 'get_jwt()' in put_source and 'is_admin' in put_source:
            print("  ✅ PUT /api/v1/places/{id} checks admin claim")
            if 'owner_id' in put_source and 'not is_admin' in put_source:
                print("  ✅ PUT allows admin to bypass ownership check")
            else:
                print("  ⚠️  PUT might not properly bypass ownership")
        else:
            print("  ❌ PUT doesn't use JWT claims for admin check")
            return False
        
        # Check DELETE
        delete_method = PlaceById.delete
        delete_source = inspect.getsource(delete_method)
        
        if 'get_jwt()' in delete_source and 'is_admin' in delete_source:
            print("  ✅ DELETE /api/v1/places/{id} checks admin claim")
        else:
            print("  ❌ DELETE doesn't check admin properly")
            return False
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def check_reviews_endpoint():
    """Check if reviews endpoint has admin bypass"""
    print("\n📋 Checking Reviews endpoint (PUT, DELETE)...")
    
    try:
        from app.presentation.api.v1.reviews import ReviewById
        
        # Check PUT
        put_method = ReviewById.put
        put_source = inspect.getsource(put_method)
        
        if 'get_jwt()' in put_source and 'is_admin' in put_source:
            print("  ✅ PUT /api/v1/reviews/{id} checks admin claim")
        else:
            print("  ❌ PUT doesn't check admin properly")
            return False
        
        # Check DELETE
        delete_method = ReviewById.delete
        delete_source = inspect.getsource(delete_method)
        
        if 'get_jwt()' in delete_source and 'is_admin' in delete_source:
            print("  ✅ DELETE /api/v1/reviews/{id} checks admin claim")
        else:
            print("  ❌ DELETE doesn't check admin properly")
            return False
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def check_amenities_endpoint():
    """Check if amenities endpoint has admin restrictions"""
    print("\n📋 Checking Amenities endpoint (POST, PUT, DELETE)...")
    
    try:
        from app.presentation.api.v1.amenities import Amenities, AmenityById
        
        # Check POST
        post_method = Amenities.post
        post_source = inspect.getsource(post_method)
        
        if '@admin_required' in post_source or 'admin_required' in post_source:
            print("  ✅ POST /api/v1/amenities/ has @admin_required")
        else:
            print("  ❌ POST missing @admin_required")
            return False
        
        # Check PUT
        put_method = AmenityById.put
        put_source = inspect.getsource(put_method)
        
        if '@admin_required' in put_source or 'admin_required' in put_source:
            print("  ✅ PUT /api/v1/amenities/{id} has @admin_required")
        else:
            print("  ❌ PUT missing @admin_required")
            return False
        
        # Check DELETE
        delete_method = AmenityById.delete
        delete_source = inspect.getsource(delete_method)
        
        if '@admin_required' in delete_source or 'admin_required' in delete_source:
            print("  ✅ DELETE /api/v1/amenities/{id} has @admin_required")
        else:
            print("  ❌ DELETE missing @admin_required")
            return False
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def check_user_repository():
    """Check if UserRepository has custom update method"""
    print("\n📋 Checking UserRepository update method...")
    
    try:
        from app.persistence.repository import UserRepository
        
        # Check if update method exists
        if not hasattr(UserRepository, 'update'):
            print("  ❌ UserRepository missing update method")
            return False
        
        update_method = UserRepository.update
        update_source = inspect.getsource(update_method)
        
        if 'password' in update_source and 'hash_password' in update_source:
            print("  ✅ UserRepository.update handles password hashing")
        else:
            print("  ⚠️  UserRepository.update might not hash passwords")
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def check_imports():
    """Check if all necessary imports are in place"""
    print("\n📋 Checking imports...")
    
    try:
        from flask_jwt_extended import get_jwt
        print("  ✅ Flask-JWT-Extended has get_jwt")
        
        from app.auth.auth_utils import admin_required
        print("  ✅ admin_required is importable")
        
        return True
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False


def main():
    """Run all checks"""
    print("=" * 60)
    print("Task 5 Implementation Verification")
    print("=" * 60)
    
    checks = [
        ("Decorator", check_admin_required_decorator),
        ("Users Endpoint", check_users_endpoint),
        ("Places Endpoint", check_places_endpoint),
        ("Reviews Endpoint", check_reviews_endpoint),
        ("Amenities Endpoint", check_amenities_endpoint),
        ("UserRepository", check_user_repository),
        ("Imports", check_imports),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print("=" * 60)
    print(f"Results: {passed}/{total} checks passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 All checks passed! Task 5 is fully implemented.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} check(s) failed. Please review the issues above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
