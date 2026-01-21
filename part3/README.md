# HBnB Part 3: Secure Backend with JWT Authentication & Database Integration

## Overview

This part implements a secure REST API with JWT authentication, role-based access control, and SQLAlchemy ORM for database persistence.

## Tasks

### Task 0: Modify the Application Factory to Include the Configuration
- Updated `app/__init__.py` to implement Application Factory pattern
- Configuration classes in `config.py` (Development, Production, Testing)
- Application factory accepts configuration object

### Task 1: Modify the User Model to Include Password Hashing
- User model in `app/models/base_model.py` includes password hashing using bcrypt
- Password hashing implemented in User model methods
- Passwords are hashed before storage and not returned in GET requests

### Task 2: Implement JWT Authentication with flask-jwt-extended
- JWT authentication setup in `app/auth/auth_utils.py`
- Login endpoint in `app/presentation/api/v1/auth.py`
- JWT tokens generated upon successful login
- Tokens include user claims (is_admin)

### Task 3: Implement Authenticated User Access Endpoints
- Protected endpoints require JWT authentication
- Users can create, update, and delete their own places
- Users can create and update their own reviews
- Ownership validation implemented
- Public endpoints remain accessible without authentication

### Task 4: Implement Administrator Access Endpoints
- Admin-only endpoints for user and amenity management
- Administrators can bypass ownership restrictions
- Role-based access control using is_admin claim in JWT

### Task 5: Implement SQLAlchemy Repository
- Repository pattern implemented in `app/persistence/repository.py`
- SQLAlchemy-based repository replaces in-memory storage
- Repository handles CRUD operations for all entities

### Task 6: Map the User Entity to SQLAlchemy Model
- BaseModelDB class in `app/models/base_model.py` with common attributes
- User model mapped to SQLAlchemy with all attributes
- UserRepository implemented for database operations

### Task 7: Map Remaining Entities to SQLAlchemy Models
- Place, Review, and Amenity models mapped to SQLAlchemy
- All models inherit from BaseModelDB
- Models include all required attributes and relationships

### Task 8: Map Relationships Between Entities Using SQLAlchemy
- One-to-many relationships: User -> Place, User -> Review, Place -> Review
- Many-to-many relationship: Place <-> Amenity (via place_amenity table)
- Foreign keys and relationship() defined in models
- Backrefs implemented for bidirectional access

### Task 9: SQL Scripts for Table Generation and Initial Data
- `schema.sql`: Creates all database tables with relationships and constraints
- `data.sql`: Inserts initial administrator user and amenities
- `test_queries.sql`: Contains CRUD operations to verify schema and data

### Task 10: Generate Database Diagrams
- ER diagram created using Mermaid.js in `er_diagram.md`
- Diagram includes all entities: User, Place, Review, Amenity, Place_Amenity
- Relationships visualized: one-to-many and many-to-many

## Project Structure

```
part3/
├── app/
│   ├── __init__.py              # Application Factory
│   ├── auth/
│   │   └── auth_utils.py        # JWT & Bcrypt utilities
│   ├── models/
│   │   └── base_model.py        # SQLAlchemy models
│   ├── persistence/
│   │   └── repository.py        # Database repositories
│   └── presentation/
│       └── api/v1/
│           ├── auth.py          # Auth endpoints
│           ├── users.py         # User endpoints
│           ├── places.py         # Place endpoints
│           ├── reviews.py        # Review endpoints
│           └── amenities.py      # Amenity endpoints
├── config.py                    # Configuration classes
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── schema.sql                   # Database schema (Task 9)
├── data.sql                     # Initial data (Task 9)
├── test_queries.sql             # Test queries (Task 9)
└── er_diagram.md                # ER diagram (Task 10)
```

## Database Schema

### Entities

- **User**: id, first_name, last_name, email, password, is_admin, created_at, updated_at
- **Place**: id, name, description, price, latitude, longitude, owner_id, created_at, updated_at
- **Review**: id, text, rating, user_id, place_id, created_at, updated_at
- **Amenity**: id, name, created_at, updated_at
- **Place_Amenity**: place_id, amenity_id (association table)

### Relationships

- User -> Place (One-to-Many): A user can own many places
- User -> Review (One-to-Many): A user can write many reviews
- Place -> Review (One-to-Many): A place can have many reviews
- Place <-> Amenity (Many-to-Many): A place can have many amenities, an amenity can be in many places

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables (create .env file):
```
FLASK_ENV=development
JWT_SECRET_KEY=your-secret-key
SQLALCHEMY_DATABASE_URI=sqlite:///hbnb_dev.db
```

3. Run the application:
```bash
python run.py
```

## API Endpoints

- POST /api/v1/auth/register - Register new user
- POST /api/v1/auth/login - Login and get JWT token
- GET /api/v1/users/ - List all users (public)
- GET /api/v1/users/<id> - Get user by ID (public)
- PUT /api/v1/users/<id> - Update user (authenticated, self or admin)
- POST /api/v1/places/ - Create place (authenticated)
- GET /api/v1/places/ - List all places (public)
- GET /api/v1/places/<id> - Get place by ID (public)
- PUT /api/v1/places/<id> - Update place (authenticated, owner or admin)
- DELETE /api/v1/places/<id> - Delete place (authenticated, owner or admin)
- POST /api/v1/reviews/ - Create review (authenticated)
- GET /api/v1/reviews/ - List all reviews (public)
- GET /api/v1/reviews/<id> - Get review by ID (public)
- PUT /api/v1/reviews/<id> - Update review (authenticated, author or admin)
- DELETE /api/v1/reviews/<id> - Delete review (authenticated, author or admin)
- GET /api/v1/amenities/ - List all amenities (public)
- POST /api/v1/amenities/ - Create amenity (admin only)
- PUT /api/v1/amenities/<id> - Update amenity (admin only)
- DELETE /api/v1/amenities/<id> - Delete amenity (admin only)

## Technologies

- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-JWT-Extended 4.5.3
- Flask-Bcrypt 4.1.1
- Flask-RESTX 1.3.0
- SQLite (development) / MySQL (production)
