# How to Run and Test Task 3

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python init_db.py
```

This creates sample data:
- Users (alice, bob, charlie)
- Places (sample properties)
- Reviews (sample reviews)
- Amenities (WiFi, Pool, etc.)

### 3. Start the Application
```bash
python run.py
```

The API will be available at: `http://localhost:5000/api/v1/`

---

## Testing All Features

### Test Script (Recommended)
```bash
python verify_task3.py
```

This script tests:
- ✅ Public GET endpoints (no auth)
- ✅ User registration and JWT
- ✅ User login
- ✅ Place creation
- ✅ Authentication requirement
- ✅ Review creation
- ✅ Self-review prevention
- ✅ Duplicate review prevention
- ✅ Ownership validation
- ✅ User profile updates
- ✅ Admin operations

**Expected Output:**
```
============================================================
Task 3: Authenticated User Access Endpoints - VERIFICATION
============================================================

[TEST 1] Public GET endpoints (no authentication required)
----------------------------------------------------------
✓ GET /api/v1/places/: 200
✓ GET /api/v1/reviews/: 200
✓ GET /api/v1/amenities/: 200
✓ GET /api/v1/users/: 200

[TEST 2] User registration and JWT token generation
----------------------------------------------------------
Registration status: 201
✓ Registration successful
✓ JWT token generated: eyJhbGciOiJIUzI1NiIsInR5cCI...
✓ User ID: <uuid>

... (more tests)

============================================================
VERIFICATION COMPLETE
============================================================

✓ All authentication and access control features verified!
```

---

## Manual Testing with cURL

### 1. Register a User
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 2. Create a Place (Requires Authentication)
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Beautiful Beach House",
    "description": "A wonderful place by the sea",
    "price": 150.00,
    "latitude": 40.7128,
    "longitude": -74.0060
  }'
```

### 3. Get All Places (Public, No Auth)
```bash
curl http://localhost:5000/api/v1/places/
```

### 4. Create a Review (Requires Auth)
```bash
PLACE_ID="<place-id-from-step-2>"

curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "text": "Amazing place! Highly recommended",
    "rating": 5,
    "place_id": "'$PLACE_ID'"
  }'
```

### 5. Test Self-Review Prevention
```bash
# Try to review your own place (should fail)
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "text": "Reviewing my own place",
    "rating": 5,
    "place_id": "'$PLACE_ID'"
  }'
```

**Expected Response (400):**
```json
{
  "message": "You cannot review your own place"
}
```

### 6. Test Duplicate Review Prevention
```bash
# Register a second user first
TOKEN2=$(curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Jane","last_name":"Smith","email":"jane@example.com","password":"Pass123!"}' \
  | jq -r '.access_token')

# First review (should succeed)
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN2" \
  -d '{
    "text": "Great place!",
    "rating": 5,
    "place_id": "'$PLACE_ID'"
  }'

# Second review (should fail)
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN2" \
  -d '{
    "text": "Another review",
    "rating": 4,
    "place_id": "'$PLACE_ID'"
  }'
```

**Expected Response (400):**
```json
{
  "message": "You have already reviewed this place"
}
```

### 7. Test Ownership Validation
```bash
# User 1 creates a place
PLACE_ID=$(curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{...}' | jq -r '.id')

# User 2 tries to update User 1's place (should fail)
curl -X PUT http://localhost:5000/api/v1/places/$PLACE_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN2" \
  -d '{
    "name": "New Name",
    "price": 200.00
  }'
```

**Expected Response (403):**
```json
{
  "message": "You can only update your own places"
}
```

---

## Pytest Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_api.py -v
pytest tests/test_business_logic.py -v
pytest tests/test_facade.py -v
```

### Run Tests with Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

---

## Error Scenarios to Test

### 1. Missing JWT Token
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{...}'
```

**Expected Response (401):**
```json
{
  "message": "Missing Authorization Header"
}
```

### 2. Invalid JWT Token
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Authorization: Bearer invalid_token_here" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

**Expected Response (422):**
```json
{
  "message": "Invalid token"
}
```

### 3. Non-Existent Place
```bash
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Review",
    "rating": 5,
    "place_id": "invalid-id"
  }'
```

**Expected Response (404):**
```json
{
  "message": "Place not found"
}
```

---

## Environment Variables

### .env File (Optional)
```env
FLASK_ENV=development
JWT_SECRET_KEY=your-super-secret-key-change-in-production
DATABASE_URL=sqlite:///hbnb_dev.db
```

### Configuration Selection
- `development` → SQLite database
- `production` → MySQL database
- `testing` → In-memory database

---

## Debugging

### Enable Debug Output
```python
# In config.py, set:
SQLALCHEMY_ECHO = True
DEBUG = True
```

### View Database
```bash
# For SQLite
sqlite3 hbnb_dev.db
sqlite> .tables
sqlite> SELECT * FROM users;
```

### Check Logs
The application logs all requests. Look for:
- Authentication errors
- Validation errors
- Database errors

---

## Common Issues & Solutions

### Issue: "No module named 'app'"
**Solution:** Make sure you're running from the part3 directory
```bash
cd part3
python run.py
```

### Issue: "Address already in use"
**Solution:** Kill the existing Flask process or use a different port
```bash
# Kill on port 5000
lsof -ti:5000 | xargs kill -9

# Or use a different port in run.py
app.run(host="0.0.0.0", port=5001)
```

### Issue: Database locked error
**Solution:** Delete the database file and reinitialize
```bash
rm hbnb_dev.db
python init_db.py
```

### Issue: JWT token expired
**Solution:** Get a new token by logging in again
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

---

## Performance Testing

### Load Testing with Apache Bench
```bash
# Test public endpoint (1000 requests)
ab -n 1000 -c 10 http://localhost:5000/api/v1/places/

# Test protected endpoint
ab -n 100 -c 5 \
  -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/v1/places/
```

---

## Next Steps

1. ✅ Run `python verify_task3.py` to test all features
2. ✅ Review the test output to verify implementation
3. ✅ Try manual cURL commands to understand API flow
4. ✅ Check logs for any errors or warnings
5. ✅ Deploy to production when satisfied

---

## Getting Help

1. **Check Documentation**: See TASK3_FINAL_SUMMARY.md
2. **Review Test File**: Look at verify_task3.py for examples
3. **Check Logs**: Enable debug mode for detailed output
4. **Read Error Messages**: They usually describe the problem

---

**Status: Ready for Testing** ✅

