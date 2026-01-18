# 🏠 HBnB Part 3: Secure Backend with JWT Authentication & Database Integration

> **A Production-Ready REST API with JWT Authentication, Role-Based Access Control, and SQLAlchemy ORM**

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.0-black?style=flat-square&logo=flask)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Architecture](#architecture)
- [Authentication](#authentication)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Testing](#testing)
- [Deployment](#deployment)

---

## 🎯 Overview

**HBnB Part 3** is a secure, scalable REST API for property rental management built with Flask. It implements industry-standard security practices including:

- ✅ **JWT-based authentication** with role-based access control
- ✅ **Bcrypt password hashing** for secure credential storage
- ✅ **SQLAlchemy ORM** for database abstraction
- ✅ **SQLite** for development & **MySQL** for production
- ✅ **RESTful API design** with automatic Swagger documentation
- ✅ **Comprehensive error handling** and validation

---

## ✨ Key Features

### 🔐 Security
- **JWT Authentication**: Stateless token-based authentication
- **Password Hashing**: Bcrypt with salt for secure password storage
- **Role-Based Authorization**: Admin and regular user roles
- **Protected Endpoints**: Decorator-based access control
- **CORS-Ready**: Prepared for cross-origin requests

### 📊 Database
- **Multi-Environment Support**: SQLite (dev) → MySQL (production)
- **ORM Abstraction**: SQLAlchemy for database independence
- **Data Relationships**: Proper foreign keys and cascading deletes
- **Automated Migrations**: Easy schema management
- **Transaction Safety**: ACID compliance

### 🏗️ Architecture
- **Application Factory Pattern**: Flexible app initialization
- **Three-Layer Architecture**:
  - 🎨 **Presentation**: REST API endpoints
  - 💼 **Business Logic**: Services and validations
  - 💾 **Persistence**: Database repositories
- **Modular Design**: Easy to extend and maintain
- **Clean Code**: Following Flask and Python best practices

### 📡 API Features
- **18+ Endpoints**: Full CRUD operations
- **Auto Documentation**: Swagger/OpenAPI with Flask-RESTX
- **Input Validation**: Automatic payload validation
- **Error Handling**: Consistent error responses
- **Status Codes**: RESTful HTTP status codes

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | Flask | 3.0.0 |
| **API Documentation** | Flask-RESTX | 1.3.0 |
| **Database ORM** | SQLAlchemy | 3.1.1 |
| **Authentication** | Flask-JWT-Extended | 4.5.3 |
| **Password Hashing** | Bcrypt | 4.1.1 |
| **Environment Config** | Python-dotenv | 1.0.0 |
| **Database (Dev)** | SQLite | Built-in |
| **Database (Prod)** | MySQL | 5.7+ |
| **Testing** | Pytest | 7.4.3 |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip or poetry
- MySQL 5.7+ (for production only)

### Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd part3

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# 5. Initialize database
python init_db.py

# 6. Run the application
python run.py
```

### API Endpoint
```
http://localhost:5000
API Documentation: http://localhost:5000 (Swagger UI)
```

---

## 📡 API Documentation

### Authentication Endpoints

#### **Register User**
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Response:** `201 Created`
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### **Login User**
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Users Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/users` | List all users | - |
| POST | `/api/v1/users` | Create user | - |
| GET | `/api/v1/users/{id}` | Get user details | - |
| PUT | `/api/v1/users/{id}` | Update user | ✅ |
| DELETE | `/api/v1/users/{id}` | Delete user | ✅ |

### Places Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/places` | List all places | - |
| POST | `/api/v1/places` | Create place | ✅ |
| GET | `/api/v1/places/{id}` | Get place details | - |
| PUT | `/api/v1/places/{id}` | Update place | ✅ |
| DELETE | `/api/v1/places/{id}` | Delete place | ✅ |

### Reviews Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/reviews` | List all reviews | - |
| POST | `/api/v1/reviews` | Create review | ✅ |
| GET | `/api/v1/reviews/{id}` | Get review details | - |
| PUT | `/api/v1/reviews/{id}` | Update review | ✅ |
| DELETE | `/api/v1/reviews/{id}` | Delete review | ✅ |

### Amenities Endpoints

| Method | Endpoint | Description | Auth | Admin |
|--------|----------|-------------|------|-------|
| GET | `/api/v1/amenities` | List amenities | - | - |
| POST | `/api/v1/amenities` | Create amenity | ✅ | ✅ |
| GET | `/api/v1/amenities/{id}` | Get amenity | - | - |
| PUT | `/api/v1/amenities/{id}` | Update amenity | ✅ | ✅ |
| DELETE | `/api/v1/amenities/{id}` | Delete amenity | ✅ | ✅ |

---

## 🔐 Authentication

### Using JWT Tokens

All protected endpoints require a JWT token in the Authorization header:

```bash
curl -X GET http://localhost:5000/api/v1/users \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Token Structure

JWT tokens include:
- **Identity**: User ID
- **Claims**: `is_admin` flag for role-based access
- **Expiration**: 1 hour (configurable)

### User Roles

- **Regular User**: Can manage own resources
- **Admin User**: Full access to all resources

---

## 🏗️ Architecture

### Three-Layer Architecture

```
┌─────────────────────────────────────┐
│   Presentation Layer (API)          │
│  - Flask-RESTX Endpoints            │
│  - Request Validation               │
│  - Response Marshalling             │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│   Business Logic Layer              │
│  - Services & Facades               │
│  - Domain Validations               │
│  - Business Rules                   │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│   Persistence Layer                 │
│  - SQLAlchemy ORM                   │
│  - Repository Pattern               │
│  - Database Operations              │
└─────────────────────────────────────┘
```

### Database Schema

```
┌─────────────┐
│    User     │
├─────────────┤
│ id (PK)     │
│ email (UQ)  │
│ password    │
│ first_name  │
│ last_name   │
│ is_admin    │
└────┬────────┘
     │ 1:N
     ├──→ Place (owner_id)
     └──→ Review (user_id)

┌─────────────────┐
│     Place       │
├─────────────────┤
│ id (PK)         │
│ owner_id (FK)   │
│ name            │
│ description     │
│ price           │
│ latitude        │
│ longitude       │
└────┬────────────┘
     │ 1:N
     ├──→ Review (place_id)
     └──→ M:N Amenity (place_amenity)

┌─────────────┐
│   Review    │
├─────────────┤
│ id (PK)     │
│ user_id (FK)│
│ place_id(FK)│
│ text        │
│ rating      │
└─────────────┘

┌─────────────┐
│   Amenity   │
├─────────────┤
│ id (PK)     │
│ name (UQ)   │
└─────────────┘
```

---

## 📁 Project Structure

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
│           ├── places.py        # Place endpoints
│           ├── reviews.py       # Review endpoints
│           └── amenities.py     # Amenity endpoints
├── config.py                    # Configuration classes
├── run.py                       # Application entry point
├── init_db.py                   # Database initialization
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
└── README.md                    # This file
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600

# Database (Development)
# SQLALCHEMY_DATABASE_URI=sqlite:///hbnb_dev.db

# Database (Production - MySQL)
SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:password@localhost:3306/hbnb_prod

# API Configuration
API_TITLE=HBnB API
API_VERSION=1.0
```

### Environment Configurations

**Development:**
```bash
FLASK_ENV=development
SQLALCHEMY_DATABASE_URI=sqlite:///hbnb_dev.db
```

**Production:**
```bash
FLASK_ENV=production
SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:pass@host/db
```

**Testing:**
```bash
FLASK_ENV=testing
SQLALCHEMY_DATABASE_URI=sqlite:///:memory:
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app
```

### Sample Data

The `init_db.py` script creates sample data:

| Email | Password | Role |
|-------|----------|------|
| admin@hbnb.com | admin123 | Admin |
| john@example.com | password123 | User |
| jane@example.com | password123 | User |

---

## 🚀 Deployment

### Production Checklist

- [ ] Change `JWT_SECRET_KEY` to a secure random string
- [ ] Set `FLASK_ENV=production`
- [ ] Configure MySQL database
- [ ] Set `DEBUG=False`
- [ ] Use a production WSGI server (Gunicorn, uWSGI)
- [ ] Set up SSL/TLS certificates
- [ ] Configure CORS for frontend domain
- [ ] Set up logging and monitoring

### Deployment Command

```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"

# Using uWSGI
uwsgi --http :5000 --wsgi-file run.py --callable app --processes 4 --threads 2
```

---

## 📝 Default Users for Testing

After running `init_db.py`, you can login with:

```bash
# Admin User
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@hbnb.com",
    "password": "admin123"
  }'

# Regular User
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

---

## 🔧 Configuration Details

### Application Factory Pattern

The app uses Flask's Application Factory pattern for flexible initialization:

```python
from app import create_app

# Development
app = create_app("config.DevelopmentConfig")

# Production
app = create_app("config.ProductionConfig")

# Testing
app = create_app("config.TestingConfig")
```

### JWT Configuration

- **Algorithm**: HS256 (HMAC with SHA-256)
- **Expiration**: 1 hour (3600 seconds)
- **Claims**: `identity` (user ID) + `is_admin` flag
- **Secret Key**: `JWT_SECRET_KEY` from config

---

## 🐛 Troubleshooting

### Common Issues

**1. Database Connection Error**
```
Solution: Check DATABASE_URI and ensure database server is running
```

**2. JWT Token Invalid**
```
Solution: Verify JWT_SECRET_KEY matches config
```

**3. Permission Denied (Admin Routes)**
```
Solution: Ensure user is admin or use admin user token
```

**4. Port Already in Use**
```bash
# Change port in run.py or use:
python run.py --port 5001
```

---

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [REST API Best Practices](https://restfulapi.net/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc7519)

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👨‍💻 Author

**Holberton School - HBnB Project**

Part 3: Secure Backend Implementation with JWT Authentication & Database Integration

---

<div align="center">

**Made with ❤️ for learning purpose**

[⬆ Back to Top](#-hbnb-part-3-secure-backend-with-jwt-authentication--database-integration)

</div>
