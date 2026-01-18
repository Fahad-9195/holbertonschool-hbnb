# HBnB Project - Part Organization

## Overview

HBnB Evolution is organized into 3 separate parts, each building on the previous:

## 📁 Part 1 - Design & Specifications
**Location**: `/part1/`

Contains technical specifications and architecture design:
- Package diagrams
- Class diagrams
- Sequence diagrams for API calls
- UML documentation

---

## 📁 Part 2 - Core Implementation
**Location**: `/part2/`

Implements the core business logic and REST API:
- ✅ Business logic layer
- ✅ REST API endpoints
- ✅ In-memory persistence (no database)
- ✅ 109 passing tests
- ✅ Flask-RESTx integration

**Features**:
- 4 main entities: User, Place, Review, Amenity
- 18 API endpoints
- Facade design pattern
- Request validation

---

## 📁 Part 3 - Enhanced Backend (New)
**Location**: `/part3/`

Enhances the backend with authentication, authorization, and database integration:
- ✅ JWT-based authentication
- ✅ Role-based access control (Admin/User)
- ✅ SQLAlchemy ORM
- ✅ SQLite database (development)
- ✅ MySQL support (production)
- ✅ Bcrypt password hashing
- ✅ Proper authorization checks
- ✅ Admin-only endpoints
- ✅ Owner-based resource access

### Part 3 Quick Start

```bash
# 1. Install dependencies
cd part3
pip install -r requirements.txt

# 2. Initialize database
python init_db.py

# 3. Run server
python run.py
```

**Access**: `http://localhost:5000`

---

## Key Differences

| Aspect | Part 2 | Part 3 |
|--------|--------|--------|
| Storage | In-memory (Python dict) | SQLite/MySQL (Database) |
| Authentication | None | JWT tokens |
| Authorization | None | Role-based (Admin/User) |
| Password Handling | Plain text | Bcrypt hashing |
| Database | None | SQLAlchemy ORM |
| Relationships | Managed manually | Database relationships |
| Admin Features | None | Admin-only endpoints |
| Persistence | Lost on restart | Persistent data |

---

## API Comparison

### Part 2 - Basic CRUD
```
GET    /api/v1/users      - List users
POST   /api/v1/users      - Create user (no auth)
GET    /api/v1/places     - List places
POST   /api/v1/places     - Create place (no auth)
```

### Part 3 - Secure API
```
POST   /api/v1/auth/register   - Register (new)
POST   /api/v1/auth/login      - Login (new)
GET    /api/v1/users           - List users
POST   /api/v1/users           - Create user
PUT    /api/v1/users/{id}      - Update user (auth required)
DELETE /api/v1/users/{id}      - Delete user (auth required)

POST   /api/v1/places          - Create place (auth required)
PUT    /api/v1/places/{id}     - Update place (owner/admin)
DELETE /api/v1/places/{id}     - Delete place (owner/admin)

POST   /api/v1/amenities       - Create amenity (admin only)
```

---

## Technology Stack Comparison

### Part 2
- Flask
- Flask-RESTx
- Pytest
- Requests

### Part 3 (Adds)
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Bcrypt
- Python-dotenv
- SQLite/MySQL

---

## Default Credentials (Part 3)

| Email | Password | Role |
|-------|----------|------|
| admin@hbnb.com | admin123 | Admin |
| john@example.com | password123 | User |
| jane@example.com | password123 | User |

---

## Team

👥 **Team Members:**
- Fahad Abdulaziz Alghamdi
- Alshammari Saud Fahad
- Nabel Nasser Aldwese

---

## Project Status

✅ Part 1: Design complete
✅ Part 2: Core implementation complete
✅ Part 3: Authentication & Database complete

**Ready for QA Review!** 🎉
