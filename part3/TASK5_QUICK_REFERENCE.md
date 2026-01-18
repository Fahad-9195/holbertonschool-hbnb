# Task 5 Quick Reference Guide

## Overview
This task implements **Role-Based Access Control (RBAC)** to restrict API endpoints to administrators and allow admins to bypass ownership restrictions.

## Key Changes

### 1. Admin-Only User Creation & Management

#### Before Task 5:
```
POST /api/v1/users/ → Anyone could create users (via JSON payload)
PUT /api/v1/users/{id} → Only self, limited fields
```

#### After Task 5:
```
POST /api/v1/users/ → ✅ Admins only, can set is_admin flag
PUT /api/v1/users/{id} → Admins: full control | Non-admins: self only (name fields)
```

### 2. Admin Bypass of Ownership Restrictions

#### Before:
```
PUT /api/v1/places/{id} → Only owner can update
PUT /api/v1/reviews/{id} → Only reviewer can update
```

#### After:
```
PUT /api/v1/places/{id} → Owner OR admin can update
PUT /api/v1/reviews/{id} → Reviewer OR admin can update
DELETE /api/v1/places/{id} → Owner OR admin can delete
DELETE /api/v1/reviews/{id} → Reviewer OR admin can delete
```

## Request Examples

### Create User (Admin Only)
```bash
POST /api/v1/users/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "securepass123",
  "is_admin": false
}
```

### Update User as Admin
```bash
PUT /api/v1/users/<user_id>
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "email": "newemail@example.com",
  "password": "newpass123",
  "is_admin": true
}
```

### Update User as Non-Admin
```bash
PUT /api/v1/users/<user_id>
Authorization: Bearer <user_token>
Content-Type: application/json

{
  "first_name": "Jane",
  "last_name": "Doe"
  // email and password are ignored
}
```

## Error Codes

| Code | Meaning | When |
|------|---------|------|
| 201 | Created | User/amenity created successfully |
| 200 | OK | Update/delete successful |
| 400 | Bad Request | Invalid input (missing fields, invalid data) |
| 401 | Unauthorized | Missing/invalid JWT token |
| 403 | Forbidden | Non-admin trying admin action, or non-owner trying to modify resource |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Email already exists |

## Response Examples

### Success: Admin Creates User
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "is_admin": false,
  "created_at": "2024-01-18T10:30:00",
  "updated_at": "2024-01-18T10:30:00"
}
```

### Error: Non-Admin Tries to Create User
```json
{
  "message": "Admin access required"
}
```
Status: 403

### Error: Duplicate Email
```json
{
  "message": "Email already exists"
}
```
Status: 409

## JWT Token Structure

The JWT token includes:
- `identity` (user ID)
- `is_admin` (boolean claim)

Example decoded payload:
```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "is_admin": true,
  "iat": 1705574000,
  "exp": 1705577600
}
```

## Files Modified

1. `app/presentation/api/v1/users.py` - Added admin-only POST, updated PUT
2. `app/presentation/api/v1/places.py` - Added admin bypass
3. `app/presentation/api/v1/reviews.py` - Added admin bypass
4. `app/persistence/repository.py` - Added password hashing in UserRepository.update()
5. `app/auth/auth_utils.py` - No changes (already had admin_required decorator)

## Testing the Implementation

### Quick Test with curl

1. Login as admin:
```bash
curl -X POST "http://localhost:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hbnb.com", "password": "admin123"}'
```

2. Use returned token to create user:
```bash
curl -X POST "http://localhost:5000/api/v1/users/" \
  -H "Authorization: Bearer <token_from_step_1>" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "password": "test123"
  }'
```

3. Test with non-admin token (should fail):
```bash
# Login as regular user first
curl -X POST "http://localhost:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "password123"}'

# Try to create user (should return 403)
curl -X POST "http://localhost:5000/api/v1/users/" \
  -H "Authorization: Bearer <non_admin_token>" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

## Key Design Decisions

1. **JWT Claims for Admin Check**: Uses `get_jwt()` instead of database lookup for better performance
2. **Automatic Password Hashing**: When admin updates password, it's automatically hashed
3. **Email Validation**: Ensures no duplicate emails even for admin-created users
4. **Non-Admin Restrictions**: Non-admins cannot change email/password even for their own account
5. **Clear Error Messages**: 403 errors clearly indicate what privilege is needed

## Security Considerations

✅ Passwords always hashed (using bcrypt)
✅ Admin status checked via JWT claim (no DB lookup needed)
✅ Email uniqueness enforced at database level
✅ Password field never returned in responses
✅ Admin bypass is intentional and secure
✅ All endpoints except GET require authentication for modifications

## Troubleshooting

### "Admin access required" error
→ Non-admin user trying to create user or modify amenity
→ Solution: Use admin token from admin@hbnb.com login

### "Email already exists"
→ Email is already registered to another user
→ Solution: Try different email or use admin to update existing user's email

### "You can only update your own profile"
→ Non-admin trying to update other user
→ Solution: Only admins can update other users

### Password not updating
→ Password must be in JSON payload as string
→ Must be non-empty
→ Solution: Check JSON format and ensure password field is present

