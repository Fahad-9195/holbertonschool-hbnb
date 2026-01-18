# Quick Start Guide - HBnB Part 3

## Installation & Running

### Step 1: Install Dependencies
```bash
cd part2
pip install -r requirements.txt
```

### Step 2: Set Up Environment
```bash
# The .env file is already created with development settings
# For production, update the values in .env
```

### Step 3: Initialize Database
```bash
python init_db.py
```

This will create:
- SQLite database (`hbnb_dev.db`)
- All tables
- Sample data:
  - Admin user: `admin@hbnb.com` / `admin123`
  - 2 regular users
  - 4 amenities
  - 2 sample places
  - 2 sample reviews

### Step 4: Start the Server
```bash
python run.py
```

Server will be available at: `http://localhost:5000`

## API Testing

### Using curl

#### 1. Register New User
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "mypassword123"
  }'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_id": "uuid-string"
}
```

#### 2. Login
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@hbnb.com",
    "password": "admin123"
  }'
```

#### 3. List All Users
```bash
curl http://localhost:5000/api/v1/users
```

#### 4. Get Current User (after login)
```bash
TOKEN="your-token-here"
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/v1/users
```

#### 5. Create a Place (Authenticated)
```bash
TOKEN="your-token-here"
curl -X POST http://localhost:5000/api/v1/places \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Luxury Penthouse",
    "description": "A stunning penthouse with city views",
    "price": 250.0,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "amenity_ids": []
  }'
```

#### 6. Create Amenity (Admin Only)
```bash
ADMIN_TOKEN="admin-token-here"
curl -X POST http://localhost:5000/api/v1/amenities \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Hot Tub"
  }'
```

#### 7. Create Review
```bash
TOKEN="your-token-here"
curl -X POST http://localhost:5000/api/v1/reviews \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Amazing place! Highly recommend!",
    "rating": 5,
    "place_id": "place-uuid-here"
  }'
```

### Using Swagger UI

1. Open: `http://localhost:5000/`
2. Try out any endpoint using the built-in Swagger interface
3. Click "Authorize" to add your JWT token
4. Test endpoints interactively

## Key Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token

### Users
- `GET /api/v1/users` - List all users
- `GET /api/v1/users/{id}` - Get specific user
- `PUT /api/v1/users/{id}` - Update user (auth required)
- `DELETE /api/v1/users/{id}` - Delete user (auth required)

### Places
- `GET /api/v1/places` - List all places
- `POST /api/v1/places` - Create place (auth required)
- `GET /api/v1/places/{id}` - Get specific place
- `PUT /api/v1/places/{id}` - Update place (auth + owner/admin)
- `DELETE /api/v1/places/{id}` - Delete place (auth + owner/admin)

### Reviews
- `GET /api/v1/reviews` - List all reviews
- `POST /api/v1/reviews` - Create review (auth required)
- `GET /api/v1/reviews/{id}` - Get specific review
- `PUT /api/v1/reviews/{id}` - Update review (auth + reviewer/admin)
- `DELETE /api/v1/reviews/{id}` - Delete review (auth + reviewer/admin)

### Amenities
- `GET /api/v1/amenities` - List all amenities
- `POST /api/v1/amenities` - Create amenity (admin only)
- `GET /api/v1/amenities/{id}` - Get specific amenity
- `PUT /api/v1/amenities/{id}` - Update amenity (admin only)
- `DELETE /api/v1/amenities/{id}` - Delete amenity (admin only)

## Testing

Run the test suite:
```bash
pytest tests/test_part3.py -v
```

Run tests with coverage:
```bash
pytest tests/test_part3.py --cov=app
```

## Default Users

After running `init_db.py`:

| Email | Password | Role |
|-------|----------|------|
| admin@hbnb.com | admin123 | Admin |
| john@example.com | password123 | User |
| jane@example.com | password123 | User |

## Important Notes

1. **Passwords**: All passwords are bcrypt hashed. Never stored in plain text.
2. **Tokens**: JWT tokens expire after 1 hour. Get a new one by logging in again.
3. **Ownership**: Users can only modify their own resources (except admins).
4. **Admin Functions**: Only admins can create/modify/delete amenities.
5. **Ratings**: Reviews must have a rating between 1-5.
6. **Locations**: Latitude must be between -90 and 90, longitude between -180 and 180.

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "Database already exists" warning
The database will be recreated when you run `init_db.py` (it first drops all tables).

### "Invalid token" error
- Get a new token by logging in
- Make sure the token is in the `Authorization: Bearer <token>` format

### Port 5000 already in use
Change the port in `run.py`:
```python
app.run(host="0.0.0.0", port=5001, debug=True)
```

## Production Deployment

Before deploying to production:

1. Update `JWT_SECRET_KEY` in `.env` to a strong random value
2. Set `FLASK_ENV=production`
3. Set `FLASK_DEBUG=False`
4. Configure MySQL instead of SQLite
5. Update database credentials
6. Enable HTTPS
7. Set up proper logging
8. Configure CORS if needed

See `PART3_README.md` for full production deployment checklist.

## Documentation

- Full API docs: See `PART3_README.md`
- Database schema: See `DATABASE_SCHEMA.md`
- Implementation details: See `IMPLEMENTATION_SUMMARY.md`
