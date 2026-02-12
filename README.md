# holbertonschool-hbnb

HBnB Evolution is a simplified AirBnB-like application built using a layered architecture (Presentation → Business Logic → Persistence) and a Facade pattern to unify access to core use-cases.

This repository contains a complete full-stack application developed in four progressive parts:

- **Part 1**: Technical documentation and UML design diagrams
- **Part 2**: Full implementation of core business logic and REST API endpoints with in-memory persistence
- **Part 3**: Authentication, Authorization, and Database Integration with SQLAlchemy
- **Part 4**: Modern web client (frontend) with HTML5, CSS3, and JavaScript

---

## Project Structure

```
holbertonschool-hbnb/
├── README.md                    # This file - Project overview
├── part1/                       # Technical Documentation (UML)
│   ├── README.md
│   ├── High-Level-Package-Diagram.md
│   ├── Detailed Class Diagram for Business Logic Layer.md
│   └── Sequence Diagrams for API Calls.md
├── part2/                       # Core Implementation (In-Memory)
│   ├── README.md
│   ├── app/
│   │   ├── business_logic/     # Domain models and business rules
│   │   ├── persistence/        # In-memory repository
│   │   ├── presentation/      # REST API endpoints
│   │   └── services/           # Facade pattern
│   ├── tests/                  # Comprehensive test suite
│   ├── requirements.txt
│   └── run.py
├── part3/                       # Secure Backend (JWT + SQLAlchemy)
│   ├── README.md               # Detailed task documentation (Tasks 0-10)
│   ├── app/
│   │   ├── auth/               # JWT authentication utilities
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── persistence/        # Database repositories
│   │   └── presentation/       # Protected API endpoints
│   ├── config.py               # Configuration classes
│   ├── run.py                  # Application entry point
│   ├── schema.sql              # Database schema (Task 9)
│   ├── data.sql                # Initial data (Task 9)
│   ├── test_queries.sql        # Test queries (Task 9)
│   ├── er_diagram.md           # ER diagram (Task 10)
│   └── requirements.txt
└── part4/                       # Web Client (Frontend)
    ├── README.md
    ├── index.html              # Places listing page
    ├── login.html              # Login page
    ├── register.html           # Registration page
    ├── place.html              # Place details page
    ├── add_review.html         # Add review page
    ├── css/                    # Modular CSS architecture
    ├── js/                     # JavaScript modules
    └── images/                 # Assets
```

---

## Part 1: Technical Documentation (UML)

**Objective**: Design the system architecture and create comprehensive UML diagrams before implementation.

### Deliverables

1. **High-Level Package Diagram**
   - Illustrates three-layer architecture (Presentation, Business Logic, Persistence)
   - Shows communication via Facade pattern
   - Defines layer responsibilities

2. **Detailed Class Diagram (Business Logic Layer)**
   - Models core entities: User, Place, Review, Amenity
   - Defines attributes, methods, and relationships
   - Shows inheritance from BaseModel (id, created_at, updated_at)

3. **Sequence Diagrams**
   - User Registration (POST /users)
   - Place Creation (POST /places)
   - Review Submission (POST /places/{id}/reviews)
   - Fetching Places List (GET /places)

### Key Relationships

- User owns many Places (one-to-many)
- User writes many Reviews (one-to-many)
- Place has many Reviews (one-to-many)
- Place includes many Amenities (many-to-many)

**Location**: `part1/` directory

---

## Part 2: Core Implementation and API Endpoints

**Objective**: Implement the complete business logic layer, REST API endpoints, and in-memory persistence.

### Tasks Completed (0-6)

**Task 0: Project Setup and Package Initialization**
- Three-layer architecture structure
- Facade Pattern implementation (HBnBFacade)
- In-Memory Repository
- Flask-RESTx configuration

**Task 1: Core Business Logic Classes**
- BaseModel with common attributes
- User, Place, Review, Amenity entities
- Validation logic and business rules
- Relationship management

**Task 2: User Endpoints**
- POST /api/v1/users/ - Create user
- GET /api/v1/users/ - List all users
- GET /api/v1/users/<id> - Get user by ID
- PUT /api/v1/users/<id> - Update user

**Task 3: Amenity Endpoints**
- POST /api/v1/amenities/ - Create amenity
- GET /api/v1/amenities/ - List all amenities
- GET /api/v1/amenities/<id> - Get amenity by ID
- PUT /api/v1/amenities/<id> - Update amenity

**Task 4: Place Endpoints**
- POST /api/v1/places/ - Create place
- GET /api/v1/places/ - List all places
- GET /api/v1/places/<id> - Get place by ID
- PUT /api/v1/places/<id> - Update place
- GET /api/v1/places/<id>/reviews - Get place reviews

**Task 5: Review Endpoints**
- POST /api/v1/reviews/ - Create review
- GET /api/v1/reviews/ - List all reviews
- GET /api/v1/reviews/<id> - Get review by ID
- PUT /api/v1/reviews/<id> - Update review
- DELETE /api/v1/reviews/<id> - Delete review

**Task 6: Testing and Validation**
- Comprehensive unit tests (109 tests)
- Facade layer tests
- API integration tests
- 100% endpoint coverage

### Features

- Complete CRUD operations for all entities
- Full relationship management
- Comprehensive input validation
- Extended response objects with nested relationships
- In-memory persistence with unique constraints

**Location**: `part2/` directory

---

## Part 3: Authentication, Authorization, and Database Integration

**Objective**: Transform the backend into a production-ready application with JWT authentication, role-based access control, and SQLAlchemy ORM.

### Tasks Completed (0-10)

**Task 0: Application Factory with Configuration**
- Application Factory pattern implementation
- Configuration classes (Development, Production, Testing)
- Environment-based configuration

**Task 1: Password Hashing**
- Bcrypt password hashing in User model
- Secure password storage
- Passwords excluded from GET responses

**Task 2: JWT Authentication**
- Flask-JWT-Extended integration
- Login endpoint with token generation
- JWT tokens with user claims (is_admin)

**Task 3: Authenticated User Access**
- Protected endpoints requiring JWT
- Ownership validation for places and reviews
- Public endpoints remain accessible
- Prevents users from reviewing own places

**Task 4: Administrator Access**
- Admin-only endpoints for user and amenity management
- Administrators bypass ownership restrictions
- Role-based access control

**Task 5: SQLAlchemy Repository**
- Repository pattern with SQLAlchemy
- Replaces in-memory storage
- Database abstraction layer

**Task 6: Map User Entity to SQLAlchemy**
- BaseModelDB with common attributes
- User model mapped to database
- UserRepository implementation

**Task 7: Map Remaining Entities**
- Place, Review, and Amenity models
- All models inherit from BaseModelDB
- Complete attribute mapping

**Task 8: Map Relationships**
- One-to-many: User -> Place, User -> Review, Place -> Review
- Many-to-many: Place <-> Amenity (via place_amenity table)
- Foreign keys and relationship() definitions
- Backrefs for bidirectional access

**Task 9: SQL Scripts**
- schema.sql: Complete database schema
- data.sql: Initial administrator user and amenities
- test_queries.sql: CRUD verification queries

**Task 10: Database Diagrams**
- ER diagram using Mermaid.js
- Visual representation of all entities and relationships
- Documented in er_diagram.md

### Database Schema

**Entities**:
- User: id, first_name, last_name, email, password, is_admin, created_at, updated_at
- Place: id, name, description, price, latitude, longitude, owner_id, created_at, updated_at
- Review: id, text, rating, user_id, place_id, created_at, updated_at
- Amenity: id, name, created_at, updated_at
- Place_Amenity: place_id, amenity_id (association table)

**Relationships**:
- User -> Place (One-to-Many via owner_id)
- User -> Review (One-to-Many via user_id)
- Place -> Review (One-to-Many via place_id)
- Place <-> Amenity (Many-to-Many via place_amenity)

### API Endpoints

**Authentication**:
- POST /api/v1/auth/register - Register new user
- POST /api/v1/auth/login - Login and get JWT token

**Users**:
- GET /api/v1/users/ - List all users (public)
- GET /api/v1/users/<id> - Get user by ID (public)
- PUT /api/v1/users/<id> - Update user (authenticated, self or admin)

**Places**:
- POST /api/v1/places/ - Create place (authenticated)
- GET /api/v1/places/ - List all places (public)
- GET /api/v1/places/<id> - Get place by ID (public)
- PUT /api/v1/places/<id> - Update place (authenticated, owner or admin)
- DELETE /api/v1/places/<id> - Delete place (authenticated, owner or admin)

**Reviews**:
- POST /api/v1/reviews/ - Create review (authenticated)
- GET /api/v1/reviews/ - List all reviews (public)
- GET /api/v1/reviews/<id> - Get review by ID (public)
- PUT /api/v1/reviews/<id> - Update review (authenticated, author or admin)
- DELETE /api/v1/reviews/<id> - Delete review (authenticated, author or admin)

**Amenities**:
- GET /api/v1/amenities/ - List all amenities (public)
- POST /api/v1/amenities/ - Create amenity (admin only)
- PUT /api/v1/amenities/<id> - Update amenity (admin only)
- DELETE /api/v1/amenities/<id> - Delete amenity (admin only)

**Location**: `part3/` directory

---

## Part 4: Web Client (Frontend)

**Objective**: Build a modern, responsive web client that connects to the Part 3 backend API.

### Features

**Authentication**:
- User registration with form validation
- Login with JWT token storage in cookies
- Session management and authentication state checking
- Admin badge and privileges display

**Places Management**:
- Grid view of all available places
- Price filtering (10, 50, 100, All)
- Place details page with comprehensive information
- Responsive place cards with hover effects

**Reviews System**:
- View all reviews for a place with ratings
- Add reviews (authenticated users only)
- Owner protection (owners cannot review own places)
- Star rating display

**User Experience**:
- Responsive design (mobile, tablet, desktop)
- Modern UI with smooth animations
- Error handling with user-friendly messages
- Loading states and empty states

### Pages

1. **index.html** - Places listing with filtering
2. **login.html** - User authentication
3. **register.html** - New user registration
4. **place.html** - Place details with reviews
5. **add_review.html** - Add review form

### Architecture

**JavaScript Modules**:
- utils.js - Core utilities, API requests, cookie management
- auth.js - Authentication functions
- places.js - Places loading and display
- reviews.js - Reviews management
- animations.js - UI animations

**CSS Architecture**:
- variables.css - CSS custom properties
- base.css - Reset and typography
- layout.css - Page structure
- components.css - UI components
- style.css - Main stylesheet

**Location**: `part4/` directory

---

## Quick Start

### Part 2 (In-Memory Backend)

```bash
cd part2
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

API available at: `http://localhost:5000`

### Part 3 (Secure Backend with Database)

```bash
cd part3
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file:
```
FLASK_ENV=development
JWT_SECRET_KEY=your-secret-key-change-in-production
SQLALCHEMY_DATABASE_URI=sqlite:///hbnb_dev.db
```

Run the application:
```bash
python run.py
```

API available at: `http://localhost:5000`

### Part 4 (Web Client)

**Prerequisites**: Part 3 backend must be running

```bash
cd part4
python -m http.server 8000
```

Open browser: `http://localhost:8000`

---

## Technologies

**Backend**:
- Python 3.9+
- Flask 3.0.0
- Flask-RESTX 1.3.0
- Flask-JWT-Extended 4.5.3
- Flask-Bcrypt 4.1.1
- Flask-SQLAlchemy 3.1.1
- SQLite (development) / MySQL (production)

**Frontend**:
- HTML5
- CSS3 (with CSS Custom Properties)
- JavaScript ES6 (vanilla, no frameworks)
- Fetch API

**Testing**:
- pytest
- Flask test client

---

## Architecture Principles

1. **Layered Architecture**: Clear separation between Presentation, Business Logic, and Persistence layers
2. **Facade Pattern**: Unified interface for all business operations
3. **Repository Pattern**: Abstraction of data access
4. **RESTful API**: Standard HTTP methods and status codes
5. **Security**: JWT authentication, password hashing, role-based access control
6. **Database Design**: Proper relationships, foreign keys, and constraints

---

## Requirements

### Part 1 Requirements
- Use UML notation for diagrams
- Ensure separation of concerns between layers
- Follow clean architecture style

### Part 2 Requirements
- Follow Python best practices and PEP 8
- Implement comprehensive error handling
- Write tests for all business logic and API endpoints
- Use Flask-RESTx for API documentation
- Maintain clean code architecture

### Part 3 Requirements
- Implement JWT authentication
- Secure endpoints with proper authorization
- Use SQLAlchemy for database operations
- Create SQL scripts for schema and initial data
- Generate ER diagrams

### Part 4 Requirements
- Use semantic HTML5
- Modern CSS with responsive design
- Vanilla JavaScript (no frameworks)
- Connect to Part 3 backend API
- Implement all required functionality

---

## Documentation

- **Part 1**: `part1/README.md` - UML diagrams and architecture
- **Part 2**: `part2/README.md` - Implementation details and API documentation
- **Part 3**: `part3/README.md` - Tasks 0-10 documentation
- **Part 4**: `part4/README.md` - Frontend documentation and setup

---

## License

This project is part of the Holberton School curriculum.
