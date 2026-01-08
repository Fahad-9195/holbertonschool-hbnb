# holbertonschool-hbnb

HBnB Evolution is a simplified AirBnB-like application built using a layered architecture (Presentation → Business Logic → Persistence) and a Facade pattern to unify access to core use-cases.

This repository contains:
- **Part 1**: Technical documentation and UML design diagrams
- **Part 2**: Full implementation of core business logic and REST API endpoints

---

## Project Structure

```text
holbertonschool-hbnb/
├── part1/
│   ├── README.md
│   └── diagrams/
│       ├── 0_package_diagram.png
│       ├── 1_class_diagram.png
│       ├── 2_1_user_registration.png
│       ├── 2_2_place_creation.png
│       ├── 2_3_review_submission.png
│       └── 2_4_fetch_places.png
└── part2/
    ├── app/
    │   ├── __init__.py
    │   ├── business_logic/
    │   │   ├── base.py
    │   │   ├── user.py
    │   │   ├── place.py
    │   │   ├── review.py
    │   │   ├── amenity.py
    │   │   └── validators.py
    │   ├── common/
    │   │   └── exceptions.py
    │   ├── persistence/
    │   │   └── repository/
    │   │       └── in_memory.py
    │   ├── presentation/
    │   │   └── api/
    │   │       └── v1/
    │   │           ├── users.py
    │   │           ├── amenities.py
    │   │           ├── places.py
    │   │           └── reviews.py
    │   └── services/
    │       └── facade.py
    ├── tests/
    │   ├── test_business_logic.py
    │   ├── test_facade.py
    │   └── test_api.py
    ├── requirements.txt
    ├── pytest.ini
    └── run.py
```

---

## Part 1: Technical Documentation (UML)

## Part 1: Technical Documentation (UML)

### Objectives

- Design the high-level architecture (3-layer system)
- Define the Business Logic classes (User, Place, Review, Amenity)
- Show sequence diagrams for key API calls
- Compile all into a clear documentation guide for implementation

### 0. High-Level Package Diagram

**Goal**: Illustrate the three-layer architecture and how layers communicate via the Facade pattern.

**Architecture**:

- **Presentation Layer**: API endpoints, DTO validation, request/response handling
- **Business Logic Layer**: Domain models + rules + HBnBFacade
- **Persistence Layer**: Repositories/DAO + database operations (implemented in Part 3)

The Facade provides a single interface to use-cases and reduces coupling between layers.

### 1. Detailed Class Diagram (Business Logic Layer)

**Goal**: Model the core entities, attributes, methods, and relationships.

**Key Concepts**:

Every entity has:
- `id` (UUID4)
- `created_at`
- `updated_at`

**Relationships**:
- User owns many Place
- User writes many Review
- Place has many Review
- Place includes many Amenity (many-to-many)

### 2. Sequence Diagrams (API Calls)

These diagrams show the flow across: Client → Presentation → HBnBFacade → Persistence → Database

**2.1 User Registration — POST /users**

Flow Summary:
- Validate request DTO
- Check email uniqueness
- Create user
- Save user and return 201 Created
- If email exists → 409 Conflict

**2.2 Place Creation — POST /places**

Flow Summary:
- Validate request DTO
- Verify owner exists
- Validate place fields (price, lat, long)
- Validate amenities (optional)
- Save place + link amenities → 201 Created
- Invalid owner → 404 Not Found

**2.3 Review Submission — POST /places/{id}/reviews**

Flow Summary:
- Validate request DTO
- Verify user exists
- Verify place exists
- Validate rating (1..5)
- Save review → 201 Created
- Invalid rating → 400 Bad Request
- Place not found → 404 Not Found

**2.4 Fetching a List of Places — GET /places**

Flow Summary:
- Parse and validate query filters
- Facade validates filters
- Repository performs search
- Return 200 OK with list
- Bad filters → 400 Bad Request

### Requirements

- Use UML notation for diagrams
- Ensure separation of concerns between layers
- Follow clean architecture style:
  - Controllers are thin
  - Business rules live in domain layer
  - Persistence is accessed via repositories

---

## Part 2: Core Implementation and API Endpoints

Part 2 implements the complete business logic layer, REST API endpoints, and a working in-memory persistence layer. All tasks from 0 to 6 have been completed and tested.

### Task 0: Project Setup and Package Initialization

**Objective**: Set up the initial project structure for the HBnB application, ensuring the codebase is organized according to best practices for a modular Python application.

**Implementation**:

- Created a three-layer architecture structure:
  - **Presentation Layer** (`app/presentation/api/v1/`): Flask-RESTx API endpoints
  - **Business Logic Layer** (`app/business_logic/`): Domain models and business rules
  - **Persistence Layer** (`app/persistence/repository/`): In-memory repository implementation
- Implemented **Facade Pattern** (`app/services/facade.py`): `HBnBFacade` class provides a unified interface for all use cases
- Implemented **In-Memory Repository** (`app/persistence/repository/in_memory.py`): Generic repository for storing entities in memory
- Configured Flask application with Flask-RESTx for automatic API documentation
- Set up project dependencies in `requirements.txt` (Flask, flask-restx, pytest)
- Created test structure with pytest configuration

**Key Files**:
- `app/__init__.py`: Flask app factory with namespace registration
- `app/services/facade.py`: HBnBFacade class managing all business operations
- `app/persistence/repository/in_memory.py`: InMemoryRepository class
- `app/common/exceptions.py`: Custom exceptions (ValidationError, NotFoundError, ConflictError)

### Task 1: Core Business Logic Classes

**Objective**: Implement the core business logic classes that define the entities of the HBnB application, including attributes, methods, and relationships.

**Implementation**:

- **BaseModel** (`app/business_logic/base.py`):
  - Provides common attributes: `id` (UUID4), `created_at`, `updated_at`
  - Implements `touch()` method to update `updated_at` timestamp

- **User** (`app/business_logic/user.py`):
  - Attributes: `first_name`, `last_name`, `email`
  - Validation: String fields with length constraints (first_name, last_name: max 50, email: max 255)
  - Methods: `update()`, `to_dict()`
  - No password field (as per requirements)

- **Place** (`app/business_logic/place.py`):
  - Attributes: `name`, `description`, `price`, `latitude`, `longitude`, `owner_id`
  - Relationships: `amenity_ids` (list), `review_ids` (list)
  - Validation: 
    - Price must be >= 0
    - Latitude must be between -90 and 90
    - Longitude must be between -180 and 180
  - Methods: `add_amenity()`, `add_review()`, `update()`, `to_dict()`

- **Review** (`app/business_logic/review.py`):
  - Attributes: `text`, `rating`, `user_id`, `place_id`
  - Validation: Rating must be between 1 and 5, text max 1000 characters
  - Methods: `update()`, `to_dict()`

- **Amenity** (`app/business_logic/amenity.py`):
  - Attributes: `name`
  - Validation: Name max 50 characters
  - Methods: `update()`, `to_dict()`

- **Validators** (`app/business_logic/validators.py`):
  - `require_str()`: Validates string fields with min/max length
  - `require_float()`: Validates numeric fields with min/max constraints
  - `require_int()`: Validates integer fields with min/max constraints
  - `require_uuid_str()`: Validates UUID string format

**Relationships Implemented**:
- User owns many Places (via `place.owner_id`)
- User writes many Reviews (via `review.user_id`)
- Place has many Reviews (via `place.review_ids` and `review.place_id`)
- Place includes many Amenities (many-to-many via `place.amenity_ids`)

### Task 2: User Endpoints

**Objective**: Implement API endpoints for managing users with CRUD operations (Create, Read, Update). DELETE is not implemented for users.

**Implementation**:

- **POST /api/v1/users/**: Create a new user
  - Validates required fields: `first_name`, `last_name`, `email`
  - Ensures email uniqueness (409 Conflict if duplicate)
  - Returns 201 Created with user data

- **GET /api/v1/users/**: List all users
  - Returns 200 OK with array of all users
  - Password is not included in responses (no password field exists)

- **GET /api/v1/users/<user_id>**: Get user by ID
  - Returns 200 OK with user data
  - Returns 404 Not Found if user doesn't exist

- **PUT /api/v1/users/<user_id>**: Update user information
  - Validates updated fields
  - Ensures email uniqueness if email is being updated
  - Returns 200 OK with updated user data
  - Returns 404 Not Found if user doesn't exist
  - Returns 409 Conflict if email already exists

**Error Handling**:
- 400 Bad Request: Validation errors
- 404 Not Found: User not found
- 409 Conflict: Duplicate email

### Task 3: Amenity Endpoints

**Objective**: Implement API endpoints for managing amenities with CRUD operations (Create, Read, Update). DELETE is not implemented for amenities.

**Implementation**:

- **POST /api/v1/amenities/**: Create a new amenity
  - Validates required field: `name`
  - Ensures name uniqueness (409 Conflict if duplicate)
  - Returns 201 Created with amenity data

- **GET /api/v1/amenities/**: List all amenities
  - Returns 200 OK with array of all amenities

- **GET /api/v1/amenities/<amenity_id>**: Get amenity by ID
  - Returns 200 OK with amenity data
  - Returns 404 Not Found if amenity doesn't exist

- **PUT /api/v1/amenities/<amenity_id>**: Update amenity information
  - Validates updated name field
  - Ensures name uniqueness if name is being updated
  - Returns 200 OK with updated amenity data
  - Returns 404 Not Found if amenity doesn't exist
  - Returns 409 Conflict if name already exists

**Error Handling**:
- 400 Bad Request: Validation errors
- 404 Not Found: Amenity not found
- 409 Conflict: Duplicate name

### Task 4: Place Endpoints

**Objective**: Implement API endpoints for managing places with CRUD operations (Create, Read, Update). DELETE is not implemented for places. Handle relationships with User (owner) and Amenity entities.

**Implementation**:

- **POST /api/v1/places/**: Create a new place
  - Validates required fields: `name`, `description`, `price`, `latitude`, `longitude`, `owner_id`
  - Validates `owner_id` exists (404 if not found)
  - Validates price >= 0, latitude [-90, 90], longitude [-180, 180]
  - Optionally accepts `amenity_ids` array and validates all amenities exist
  - Returns 201 Created with place data including expanded `owner` and `amenities` objects

- **GET /api/v1/places/**: List all places
  - Returns 200 OK with array of all places
  - Each place includes expanded `owner` object and `amenities` array

- **GET /api/v1/places/<place_id>**: Get place by ID
  - Returns 200 OK with place data including expanded relationships
  - Returns 404 Not Found if place doesn't exist

- **PUT /api/v1/places/<place_id>**: Update place information
  - Validates updated fields including price, latitude, longitude constraints
  - Validates `owner_id` if being updated
  - Can update `amenity_ids` list (validates all amenities exist)
  - Returns 200 OK with updated place data including expanded relationships
  - Returns 404 Not Found if place or related entities don't exist

- **GET /api/v1/places/<place_id>/reviews**: Get all reviews for a place
  - Returns 200 OK with array of reviews for the specified place
  - Each review includes expanded `user` and `place` objects
  - Returns 404 Not Found if place doesn't exist

**Error Handling**:
- 400 Bad Request: Validation errors (invalid price, latitude, longitude, etc.)
- 404 Not Found: Place, owner, or amenity not found
- 409 Conflict: Data conflicts

### Task 5: Review Endpoints

**Objective**: Implement API endpoints for managing reviews with full CRUD operations (Create, Read, Update, Delete). Reviews are the only entity with DELETE support in Part 2.

**Implementation**:

- **POST /api/v1/reviews/**: Create a new review
  - Validates required fields: `text`, `rating`, `user_id`, `place_id`
  - Validates `user_id` and `place_id` exist (404 if not found)
  - Validates rating is between 1 and 5
  - Automatically adds review to place's `review_ids` list
  - Returns 201 Created with review data including expanded `user` and `place` objects

- **GET /api/v1/reviews/**: List all reviews
  - Returns 200 OK with array of all reviews
  - Each review includes expanded `user` and `place` objects

- **GET /api/v1/reviews/<review_id>**: Get review by ID
  - Returns 200 OK with review data including expanded relationships
  - Returns 404 Not Found if review doesn't exist

- **PUT /api/v1/reviews/<review_id>**: Update review information
  - Validates updated fields including rating constraints
  - Validates `user_id` and `place_id` if being updated
  - If `place_id` is changed, removes review from old place and adds to new place
  - Returns 200 OK with updated review data including expanded relationships
  - Returns 404 Not Found if review or related entities don't exist

- **DELETE /api/v1/reviews/<review_id>**: Delete a review
  - Removes review from place's `review_ids` list
  - Deletes the review from repository
  - Returns 200 OK with success message
  - Returns 404 Not Found if review doesn't exist

**Error Handling**:
- 400 Bad Request: Validation errors (invalid rating, missing fields)
- 404 Not Found: Review, user, or place not found
- 409 Conflict: Data conflicts

### Task 6: Testing and Validation

**Objective**: Create comprehensive tests, implement validation logic, and document testing results.

**Implementation**:

- **Unit Tests** (`tests/test_business_logic.py`):
  - Validator function tests (require_str, require_float, require_int, require_uuid_str)
  - User model tests (creation, validation, updates)
  - Amenity model tests (creation, validation, updates)
  - Place model tests (creation, validation, relationships, coordinate validation)
  - Review model tests (creation, validation, rating constraints)

- **Facade Layer Tests** (`tests/test_facade.py`):
  - User CRUD operations through facade
  - Amenity CRUD operations through facade
  - Place CRUD operations with relationship handling
  - Review CRUD operations with relationship handling
  - Error handling tests (ValidationError, NotFoundError, ConflictError)
  - Relationship integrity tests (place-amenity, place-review, review-user-place)

- **API Integration Tests** (`tests/test_api.py`):
  - All HTTP endpoints tested (GET, POST, PUT, DELETE)
  - Status code validation (200, 201, 400, 404, 409)
  - Response format validation
  - Error response validation
  - Extended attributes validation (owner, amenities, user, place objects in responses)
  - Edge cases and error scenarios

**Test Results**:
- All 109 tests pass successfully
- 100% endpoint coverage
- Comprehensive error scenario coverage
- Relationship integrity verified

**Testing Tools**:
- pytest for test execution
- Flask test client for API integration tests
- Isolated test fixtures to prevent side effects

**Documentation**:
- `tests/README.md`: Complete testing documentation
- Swagger/OpenAPI documentation auto-generated by Flask-RESTx at `/api/v1/`
- All endpoints documented with request/response models

### Part 2 Summary

**Architecture**:
- Clean separation of concerns across three layers
- Facade pattern provides unified business logic interface
- Repository pattern abstracts data access (ready for Part 3 database integration)

**Features Implemented**:
- Complete CRUD operations for Users, Amenities, Places, and Reviews
- Full relationship management (User-Places, Place-Amenities, Place-Reviews, Review-User-Place)
- Comprehensive input validation and error handling
- Extended response objects with nested relationships
- In-memory persistence with unique field constraints

**API Endpoints Summary**:
- Users: 4 endpoints (POST, GET list, GET by id, PUT)
- Amenities: 4 endpoints (POST, GET list, GET by id, PUT)
- Places: 5 endpoints (POST, GET list, GET by id, PUT, GET reviews)
- Reviews: 5 endpoints (POST, GET list, GET by id, PUT, DELETE)

**Next Steps (Part 3)**:
- Replace in-memory repository with SQLAlchemy database persistence
- Implement database migrations
- Add query filtering and pagination
- Implement authentication and authorization

---

## Requirements

### Part 1 Requirements

- Use UML notation for diagrams
- Ensure separation of concerns between layers
- Follow clean architecture style:
  - Controllers are thin
  - Business rules live in domain layer
  - Persistence is accessed via repositories

### Part 2 Requirements

- Follow Python best practices and PEP 8
- Implement comprehensive error handling
- Write tests for all business logic and API endpoints
- Use Flask-RESTx for API documentation
- Maintain clean code architecture
- Ensure all endpoints return appropriate HTTP status codes
