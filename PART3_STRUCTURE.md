# HBnB Project - Part 3: Authentication & Database Integration

## 📁 Project Structure

```
holbertonschool-hbnb/
├── part1/                    # Technical specifications & UML diagrams
├── part2/                    # Core implementation (Business Logic & API)
└── part3/                    # Enhanced backend (Auth & Database) ← NEW
    ├── config.py             # Database & app configuration
    ├── requirements.txt      # Python dependencies
    ├── .env                  # Environment variables
    ├── .env.example          # Configuration template
    ├── run.py                # Application entry point
    ├── init_db.py            # Database initialization
    ├── README.md             # Part 3 documentation
    ├── app/
    │   ├── __init__.py       # Flask app factory
    │   ├── models/
    │   │   └── base_model.py # SQLAlchemy ORM models
    │   ├── auth/
    │   │   └── auth_utils.py # JWT & Password utilities
    │   ├── persistence/
    │   │   └── repository.py # Database repositories
    │   └── presentation/
    │       └── api/v1/
    │           ├── auth.py       # Register/Login endpoints
    │           ├── users.py      # User CRUD endpoints
    │           ├── places.py     # Place CRUD endpoints
    │           ├── reviews.py    # Review CRUD endpoints
    │           └── amenities.py  # Amenity CRUD endpoints
    └── tests/
        └── test_part3.py    # Test suite
```

## ✨ Part 3 Features

### Authentication
- User registration with email/password
- Secure login with JWT tokens
- Password hashing using bcrypt
- 1-hour token expiration

### Authorization
- Role-based access control (Admin/User)
- Admin-only endpoints (amenities management)
- Owner authorization for resources
- User can modify own profile/resources

### Database
- SQLAlchemy ORM for data models
- SQLite for development
- MySQL ready for production
- Proper relationships and constraints
- Cascade delete operations

### API Endpoints (18 total)
✅ Authentication: 2 endpoints
✅ Users: 5 endpoints
✅ Places: 5 endpoints
✅ Reviews: 5 endpoints
✅ Amenities: 4 endpoints

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd part3
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python init_db.py
```

### 3. Run Application
```bash
python run.py
```

Access at: `http://localhost:5000`

## 📝 Default Users

| Email | Password | Role |
|-------|----------|------|
| admin@hbnb.com | admin123 | Admin |
| john@example.com | password123 | User |
| jane@example.com | password123 | User |

## 🔐 Key Endpoints

### Authentication
```
POST /api/v1/auth/register - Register new user
POST /api/v1/auth/login    - Login and get JWT
```

### Resources (CRUD)
```
GET    /api/v1/users         - List users
GET    /api/v1/places        - List places
GET    /api/v1/reviews       - List reviews
GET    /api/v1/amenities     - List amenities

POST   /api/v1/users         - Create user
POST   /api/v1/places        - Create place (auth required)
POST   /api/v1/reviews       - Create review (auth required)
POST   /api/v1/amenities     - Create amenity (admin only)
```

## 🗄️ Database Models

### User
- first_name, last_name, email, password (hashed)
- is_admin flag
- One-to-many: Places, Reviews

### Place
- name, description, price, latitude, longitude
- owner_id (foreign key to User)
- Many-to-many: Amenities
- One-to-many: Reviews

### Review
- text, rating (1-5)
- user_id, place_id (foreign keys)

### Amenity
- name (unique)
- Many-to-many: Places

## 🧪 Testing

Run all tests:
```bash
pytest tests/test_part3.py -v
```

## 📚 Documentation

- Full API docs: See `part3/README.md`
- Database schema: Check database relationships in models
- Configuration: Edit `.env` file for settings

## ✅ Project Status

- ✅ Part 1: Design & Documentation
- ✅ Part 2: Core Implementation
- ✅ Part 3: Authentication & Database (COMPLETE)

---

**Ready for Manual QA Review!** 🎉
