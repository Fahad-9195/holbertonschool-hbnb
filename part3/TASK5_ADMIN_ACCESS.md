# Task 5: Administrator Access Endpoints - Implementation Complete ✅

## Overview

This task implements Role-Based Access Control (RBAC) to restrict certain API endpoints to administrators only, and allows administrators to bypass ownership restrictions on user resources.

---

## What Was Implemented

### 1. **Admin-Only User Management** ✅

#### POST /api/v1/users/ - Create User (Admin Only)
- ✓ Requires `@admin_required` decorator
- ✓ Only admins can create new users
- ✓ Admins can optionally set `is_admin` flag for new users
- ✓ Email uniqueness validation
- ✓ Password automatically hashed using `User.hash_password()`
- ✓ Returns 403 Forbidden if non-admin attempts access

#### PUT /api/v1/users/<user_id> - Update User
- ✓ **For Admins**: Can update any field
  - `first_name`, `last_name` - Always updatable
  - `email` - With uniqueness validation
  - `password` - Automatically hashed
  - `is_admin` - Can promote/demote users
- ✓ **For Non-Admins**: Can only update own profile
  - Limited to `first_name` and `last_name`
  - Cannot change `email`, `password`, or `is_admin` flag
- ✓ Ownership validation: `user_id == current_user_id or is_admin`

### 2. **Admin-Only Amenity Management** ✅

Amenities endpoints already implemented with `@admin_required`:
- ✓ POST /api/v1/amenities/ - Create (Admin only)
- ✓ PUT /api/v1/amenities/<id> - Update (Admin only)
- ✓ DELETE /api/v1/amenities/<id> - Delete (Admin only)

### 3. **Admin Bypass of Ownership Restrictions** ✅

#### Places Endpoint (`app/presentation/api/v1/places.py`)

**PUT /api/v1/places/<place_id>**
- Non-Admins: Can only update places they own
- Admins: Can update any place
- Implementation:
  ```python
  if place.owner_id != current_user_id and not is_admin:
      api.abort(403, "You can only update your own places")
  ```

**DELETE /api/v1/places/<place_id>**
- Non-Admins: Can only delete places they own
- Admins: Can delete any place
- Same ownership check pattern

#### Reviews Endpoint (`app/presentation/api/v1/reviews.py`)

**PUT /api/v1/reviews/<review_id>**
- Non-Admins: Can only update their own reviews
- Admins: Can update any review
- Implementation:
  ```python
  if review.user_id != current_user_id and not is_admin:
      api.abort(403, "You can only update your own reviews")
  ```

**DELETE /api/v1/reviews/<review_id>**
- Non-Admins: Can only delete their own reviews
- Admins: Can delete any review
- Same ownership check pattern

---

## Key Implementation Details

### JWT Claims Extraction

Instead of querying the database for every admin check, we use JWT claims:

```python
from flask_jwt_extended import get_jwt_identity, get_jwt

current_user_id = get_jwt_identity()
claims = get_jwt()
is_admin = claims.get('is_admin', False)
```

**Benefits:**
- ⚡ No database lookup needed
- 🔒 Stateless authentication
- 🚀 Better performance

### UserRepository.update() Enhancement

Added special handling for password updates:

```python
def update(self, obj_id: str, data: dict):
    """Update a user, with special handling for password"""
    user = self.get(obj_id)
    for key, value in data.items():
        if key != 'id' and hasattr(user, key):
            if key == 'password':
                # Hash the password if it's being updated
                user.hash_password(value)
            else:
                setattr(user, key, value)
    # ... commit changes
```

---

## Modified Files Summary

### 1. `app/presentation/api/v1/users.py`
- Added `get_jwt` import
- Added `@admin_required` decorator to POST endpoint
- Updated PUT endpoint:
  - Checks JWT claims for `is_admin` flag
  - Admins can update all fields (email, password, is_admin)
  - Non-admins limited to first_name, last_name
  - Email uniqueness validation for admin updates
  - Password automatic hashing

### 2. `app/presentation/api/v1/places.py`
- Added `get_jwt` import
- Updated PUT and DELETE endpoints:
  - Use `get_jwt()` instead of database lookup
  - Check `is_admin` claim from JWT
  - Admins bypass ownership restrictions

### 3. `app/presentation/api/v1/reviews.py`
- Added `get_jwt` import
- Updated PUT and DELETE endpoints:
  - Use `get_jwt()` instead of database lookup
  - Check `is_admin` claim from JWT
  - Admins bypass user_id restrictions

### 4. `app/persistence/repository.py`
- Added custom `update()` method to `UserRepository`
- Handles password hashing automatically when password is updated

---

## Authorization Matrix

| Endpoint | Method | Public | Auth | Admin | Notes |
|----------|--------|--------|------|-------|-------|
| Users | POST | ✗ | ✗ | ✓ | Create new user |
| Users | PUT/{id} | ✗ | ✓* | ✓ | Self or any (admin) |
| Users | DELETE/{id} | ✗ | ✓* | ✓ | Self or any (admin) |
| Places | POST | ✗ | ✓ | ✓ | Creates owned place |
| Places | PUT/{id} | ✗ | ✓ | ✓ | Own or any (admin) |
| Places | DELETE/{id} | ✗ | ✓ | ✓ | Own or any (admin) |
| Reviews | POST | ✗ | ✓ | ✓ | Creates own review |
| Reviews | PUT/{id} | ✗ | ✓ | ✓ | Own or any (admin) |
| Reviews | DELETE/{id} | ✗ | ✓ | ✓ | Own or any (admin) |
| Amenities | POST | ✗ | ✗ | ✓ | Admin only |
| Amenities | PUT/{id} | ✗ | ✗ | ✓ | Admin only |
| Amenities | DELETE/{id} | ✗ | ✗ | ✓ | Admin only |

*Non-admins limited to own resources

---

## Security Features

✅ **JWT-based RBAC** - is_admin claim in token
✅ **Stateless admin checks** - No database queries needed
✅ **Email uniqueness** - Prevents duplicate emails
✅ **Password hashing** - Automatic on update
✅ **Ownership validation** - Prevents unauthorized access
✅ **Admin bypass** - Intentional and secure
✅ **Comprehensive error handling** - Clear 403 Forbidden messages

---

## Testing

Comprehensive test suite in `tests/test_task5.py` includes:

### Admin User Creation Tests
- ✅ Admin can create regular user
- ✅ Admin can create another admin
- ✅ Non-admin cannot create user (403)
- ✅ Unauthenticated cannot create user (401)
- ✅ Cannot create duplicate email (409)

### Admin User Update Tests
- ✅ Admin can update user email
- ✅ Admin can update user password
- ✅ Admin can update is_admin flag
- ✅ Non-admin cannot update other user (403)
- ✅ Non-admin can update own profile (limited fields)
- ✅ Non-admin cannot update own email (silently ignored)
- ✅ Cannot update to duplicate email (409)

### Admin Place Access Tests
- ✅ Admin can update others' places
- ✅ Admin can delete others' places
- ✅ Non-admin cannot update others' places (403)
- ✅ Non-admin cannot delete others' places (403)
- ✅ Owner can update own place

### Admin Review Access Tests
- ✅ Admin can update others' reviews
- ✅ Admin can delete others' reviews
- ✅ Non-admin cannot update others' reviews (403)
- ✅ Non-admin cannot delete others' reviews (403)
- ✅ Reviewer can update own review

### Admin Amenity Access Tests
- ✅ Admin can create amenity
- ✅ Non-admin cannot create amenity (403)
- ✅ Unauthenticated cannot create amenity (401)
- ✅ Admin can update amenity
- ✅ Non-admin cannot update amenity (403)
- ✅ Admin can delete amenity
- ✅ Non-admin cannot delete amenity (403)

---

## API Usage Examples

### Admin Creates User
```bash
curl -X POST "http://localhost:5000/api/v1/users/" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "securepass123",
    "is_admin": false
  }'
```

### Admin Updates User Email and Password
```bash
curl -X PUT "http://localhost:5000/api/v1/users/<user_id>" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newemail@example.com",
    "password": "newpassword123",
    "first_name": "Jane"
  }'
```

### Admin Updates Non-Owned Place
```bash
curl -X PUT "http://localhost:5000/api/v1/places/<place_id>" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"price": 150.00}'
```

### Admin Creates Amenity
```bash
curl -X POST "http://localhost:5000/api/v1/amenities/" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Hot Tub"}'
```

### Non-Admin Attempts to Create User (Fails)
```bash
curl -X POST "http://localhost:5000/api/v1/users/" \
  -H "Authorization: Bearer <user_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "password": "pass123"
  }'
# Response: 403 Forbidden - Admin access required
```

---

## Task Completion Checklist

- ✅ POST /api/v1/users/ restricted to admins only
- ✅ PUT /api/v1/users/<id> allows admins to modify any field
- ✅ PUT /api/v1/users/<id> restricts non-admins to name fields
- ✅ Amenity endpoints (POST/PUT/DELETE) are admin-only
- ✅ Admins can bypass ownership restrictions on places
- ✅ Admins can bypass ownership restrictions on reviews
- ✅ JWT claims used for admin checks (no DB lookup)
- ✅ Email uniqueness validation implemented
- ✅ Password hashing automatic for admin updates
- ✅ Comprehensive test suite with 25+ test cases
- ✅ All error handling with proper HTTP status codes

---

## Running Tests

```bash
# Run all tests
pytest tests/test_task5.py -v

# Run specific test class
pytest tests/test_task5.py::TestAdminUserCreation -v

# Run with coverage
pytest tests/test_task5.py --cov=app --cov-report=html
```

---

## Notes for Part 4-6 Integration

1. **Backward Compatibility**: All existing non-admin endpoints work as before
2. **No Database Migration**: Using existing User model with `is_admin` field
3. **Token Claims**: JWT tokens include `is_admin` claim automatically
4. **Password Security**: Passwords are hashed both on creation and update
5. **Default Credentials**: Initial admin user has email `admin@hbnb.com`

---

## Known Limitations & Future Enhancements

1. **Password Reset**: No password recovery mechanism yet
2. **Audit Logging**: No logging of admin actions
3. **Rate Limiting**: No API rate limiting
4. **Soft Deletes**: Deleted resources are hard-deleted (no soft deletes)
5. **Admin Audit Trail**: Consider adding in future version

