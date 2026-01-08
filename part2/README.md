# HBnB Part 2: Core Implementation and API Endpoints

HBnB Evolution Part 2 implements the complete business logic layer, REST API endpoints, and a working in-memory persistence layer. This part focuses on building a fully functional API for managing Users, Places, Reviews, and Amenities following a clean architecture with three layers (Presentation, Business Logic, Persistence) and the Facade design pattern.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Tasks Overview](#tasks-overview)
  - [Task 0: Project Setup and Package Initialization](#task-0-project-setup-and-package-initialization)
  - [Task 1: Core Business Logic Classes](#task-1-core-business-logic-classes)
  - [Task 2: User Endpoints](#task-2-user-endpoints)
  - [Task 3: Amenity Endpoints](#task-3-amenity-endpoints)
  - [Task 4: Place Endpoints](#task-4-place-endpoints)
  - [Task 5: Review Endpoints](#task-5-review-endpoints)
  - [Task 6: Testing and Validation](#task-6-testing-and-validation)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Architecture](#architecture)

## Overview

Part 2 implements a complete RESTful API for the HBnB application. The implementation follows best practices for clean architecture, with clear separation between the Presentation layer (API endpoints), Business Logic layer (domain models and rules), and Persistence layer (data storage).

**Key Features**:
- Complete CRUD operations for Users, Places, Reviews, and Amenities
- Full relationship management between entities
- Comprehensive input validation and error handling
- In-memory persistence (ready to be replaced with database in Part 3)
- Automatic API documentation via Flask-RESTx (Swagger)
- Comprehensive test suite with 109 passing tests

## Project Structure

```
part2/
├── app/
│   ├── __init__.py                 # Flask app factory
│   ├── business_logic/             # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── base.py                 # BaseModel class
│   │   ├── user.py                 # User entity
│   │   ├── place.py                # Place entity
│   │   ├── review.py               # Review entity
│   │   ├── amenity.py              # Amenity entity
│   │   └── validators.py           # Validation functions
│   ├── common/                     # Shared components
│   │   ├── __init__.py
│   │   └── exceptions.py           # Custom exceptions
│   ├── persistence/                # Persistence Layer
│   │   ├── __init__.py
│   │   └── repository/
│   │       ├── __init__.py
│   │       └── in_memory.py        # In-memory repository
│   ├── presentation/               # Presentation Layer
│   │   ├── __init__.py
│   │   └── api/
│   │       ├── __init__.py
│   │       └── v1/
│   │           ├── __init__.py
│   │           ├── users.py        # User endpoints
│   │           ├── amenities.py    # Amenity endpoints
│   │           ├── places.py       # Place endpoints
│   │           └── reviews.py      # Review endpoints
│   └── services/                   # Service Layer
│       ├── __init__.py
│       └── facade.py               # HBnBFacade class
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── test_business_logic.py      # Business logic tests
│   ├── test_facade.py              # Facade layer tests
│   └── test_api.py                 # API integration tests
├── requirements.txt                # Python dependencies
├── pytest.ini                      # Pytest configuration
├── run.py                          # Application entry point
└── README.md                       # This file
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. Navigate to the part2 directory:
```bash
cd part2
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

Start the Flask development server:
```bash
python run.py
```

The API will be available at `http://localhost:5000`

### Accessing API Documentation

Flask-RESTx automatically generates Swagger/OpenAPI documentation. Access it at:
- Swagger UI: `http://localhost:5000/api/v1/`
- JSON Schema: `http://localhost:5000/api/v1/swagger.json`

## Tasks Overview

### Task 0: Project Setup and Package Initialization

**Objective**: Set up the initial project structure for the HBnB application, ensuring the codebase is organized according to best practices for a modular Python application.

**Implementation Details**:

- **Three-Layer Architecture**:
  - **Presentation Layer** (`app/presentation/api/v1/`): Flask-RESTx API endpoints handling HTTP requests and responses
  - **Business Logic Layer** (`app/business_logic/`): Domain models with business rules and validation
  - **Persistence Layer** (`app/persistence/repository/`): In-memory repository implementation for data storage

- **Facade Pattern** (`app/services/facade.py`):
  - `HBnBFacade` class provides a unified interface for all business operations
  - Simplifies communication between Presentation and Persistence layers
  - Centralizes business logic and validation rules

- **In-Memory Repository** (`app/persistence/repository/in_memory.py`):
  - Generic repository implementation storing entities in memory
  - Supports CRUD operations: add, get, list, update, delete
  - Enforces unique field constraints (e.g., email uniqueness for users)
  - Designed to be easily replaced with database-backed repository in Part 3

- **Custom Exceptions** (`app/common/exceptions.py`):
  - `ValidationError`: For validation failures
  - `NotFoundError`: For missing resources
  - `ConflictError`: For unique constraint violations

**Key Files Created**:
- `app/__init__.py`: Flask app factory with namespace registration
- `app/services/facade.py`: HBnBFacade class managing all business operations
- `app/persistence/repository/in_memory.py`: InMemoryRepository class
- `requirements.txt`: Project dependencies (Flask, flask-restx, pytest)

### Task 1: Core Business Logic Classes

**Objective**: Implement the core business logic classes that define the entities of the HBnB application, including attributes, methods, and relationships.

**Implementation Details**:

- **BaseModel** (`app/business_logic/base.py`):
  - Base class for all entities
  - Provides common attributes: `id` (UUID4), `created_at`, `updated_at`
  - Implements `touch()` method to update `updated_at` timestamp automatically

- **User** (`app/business_logic/user.py`):
  - Attributes: `first_name`, `last_name`, `email`
  - Validation: 
    - String fields with length constraints (first_name, last_name: max 50, email: max 255)
    - Email uniqueness enforced at repository level
  - Methods: `update()`, `to_dict()`
  - Note: No password field (as per requirements)

- **Place** (`app/business_logic/place.py`):
  - Attributes: `name`, `description`, `price`, `latitude`, `longitude`, `owner_id`
  - Relationships: `amenity_ids` (list), `review_ids` (list)
  - Validation: 
    - Price must be >= 0
    - Latitude must be between -90 and 90
    - Longitude must be between -180 and 180
    - Name max 100 characters, description max 1000 characters
  - Methods: `add_amenity()`, `add_review()`, `update()`, `to_dict()`
  - Relationship management: Maintains lists of related amenity and review IDs

- **Review** (`app/business_logic/review.py`):
  - Attributes: `text`, `rating`, `user_id`, `place_id`
  - Validation: 
    - Rating must be between 1 and 5 (inclusive)
    - Text max 1000 characters
  - Methods: `update()`, `to_dict()`
  - Linked to both User and Place entities

- **Amenity** (`app/business_logic/amenity.py`):
  - Attributes: `name`
  - Validation: Name max 50 characters
  - Methods: `update()`, `to_dict()`
  - Name uniqueness enforced at repository level

- **Validators** (`app/business_logic/validators.py`):
  - `require_str()`: Validates string fields with min/max length constraints
  - `require_float()`: Validates numeric fields with min/max value constraints
  - `require_int()`: Validates integer fields with min/max value constraints
  - `require_uuid_str()`: Validates UUID string format
  - All validators raise `ValueError` with descriptive messages on validation failure

**Relationships Implemented**:
- User owns many Places (via `place.owner_id`)
- User writes many Reviews (via `review.user_id`)
- Place has many Reviews (via `place.review_ids` and `review.place_id`)
- Place includes many Amenities (many-to-many via `place.amenity_ids`)

### Task 2: User Endpoints

**Objective**: Implement API endpoints for managing users with CRUD operations (Create, Read, Update). DELETE is not implemented for users as per requirements.

**Endpoints Implemented**:

1. **POST /api/v1/users/**: Create a new user
   - Request Body: `{ "first_name": string, "last_name": string, "email": string }`
   - Validates required fields
   - Ensures email uniqueness (returns 409 Conflict if duplicate)
   - Returns 201 Created with user data including generated `id`

2. **GET /api/v1/users/**: List all users
   - Returns 200 OK with array of all users
   - Each user includes: `id`, `first_name`, `last_name`, `email`, `created_at`, `updated_at`
   - Password is not included in responses (no password field exists)

3. **GET /api/v1/users/<user_id>**: Get user by ID
   - Returns 200 OK with user data
   - Returns 404 Not Found if user doesn't exist

4. **PUT /api/v1/users/<user_id>**: Update user information
   - Request Body: `{ "first_name": string (optional), "last_name": string (optional), "email": string (optional) }`
   - Validates updated fields
   - Ensures email uniqueness if email is being updated
   - Returns 200 OK with updated user data
   - Returns 404 Not Found if user doesn't exist
   - Returns 409 Conflict if email already exists

**Error Handling**:
- 400 Bad Request: Validation errors (missing fields, invalid format)
- 404 Not Found: User not found
- 409 Conflict: Duplicate email

### Task 3: Amenity Endpoints

**Objective**: Implement API endpoints for managing amenities with CRUD operations (Create, Read, Update). DELETE is not implemented for amenities as per requirements.

**Endpoints Implemented**:

1. **POST /api/v1/amenities/**: Create a new amenity
   - Request Body: `{ "name": string }`
   - Validates required field: `name`
   - Ensures name uniqueness (returns 409 Conflict if duplicate)
   - Returns 201 Created with amenity data including generated `id`

2. **GET /api/v1/amenities/**: List all amenities
   - Returns 200 OK with array of all amenities
   - Each amenity includes: `id`, `name`, `created_at`, `updated_at`

3. **GET /api/v1/amenities/<amenity_id>**: Get amenity by ID
   - Returns 200 OK with amenity data
   - Returns 404 Not Found if amenity doesn't exist

4. **PUT /api/v1/amenities/<amenity_id>**: Update amenity information
   - Request Body: `{ "name": string (optional) }`
   - Validates updated name field
   - Ensures name uniqueness if name is being updated
   - Returns 200 OK with updated amenity data
   - Returns 404 Not Found if amenity doesn't exist
   - Returns 409 Conflict if name already exists

**Error Handling**:
- 400 Bad Request: Validation errors (missing name, invalid format)
- 404 Not Found: Amenity not found
- 409 Conflict: Duplicate name

### Task 4: Place Endpoints

**Objective**: Implement API endpoints for managing places with CRUD operations (Create, Read, Update). DELETE is not implemented for places as per requirements. Handle relationships with User (owner) and Amenity entities.

**Endpoints Implemented**:

1. **POST /api/v1/places/**: Create a new place
   - Request Body: 
     ```json
     {
       "name": string,
       "description": string,
       "price": float,
       "latitude": float,
       "longitude": float,
       "owner_id": string,
       "amenity_ids": [string] (optional)
     }
     ```
   - Validates required fields
   - Validates `owner_id` exists (returns 404 if not found)
   - Validates price >= 0, latitude [-90, 90], longitude [-180, 180]
   - Optionally accepts `amenity_ids` array and validates all amenities exist
   - Returns 201 Created with place data including expanded `owner` object and `amenities` array

2. **GET /api/v1/places/**: List all places
   - Returns 200 OK with array of all places
   - Each place includes:
     - Place fields: `id`, `name`, `description`, `price`, `latitude`, `longitude`, `owner_id`, `amenity_ids`, `review_ids`
     - Expanded `owner` object: `{ "id", "first_name", "last_name" }`
     - Expanded `amenities` array: `[{ "id", "name" }, ...]`

3. **GET /api/v1/places/<place_id>**: Get place by ID
   - Returns 200 OK with place data including expanded relationships
   - Returns 404 Not Found if place doesn't exist

4. **PUT /api/v1/places/<place_id>**: Update place information
   - Request Body: Any combination of place fields (all optional)
   - Validates updated fields including price, latitude, longitude constraints
   - Validates `owner_id` if being updated
   - Can update `amenity_ids` list (validates all amenities exist)
   - Returns 200 OK with updated place data including expanded relationships
   - Returns 404 Not Found if place or related entities don't exist

5. **GET /api/v1/places/<place_id>/reviews**: Get all reviews for a place
   - Returns 200 OK with array of reviews for the specified place
   - Each review includes expanded `user` and `place` objects
   - Returns 404 Not Found if place doesn't exist

**Error Handling**:
- 400 Bad Request: Validation errors (invalid price, latitude, longitude, missing fields)
- 404 Not Found: Place, owner, or amenity not found
- 409 Conflict: Data conflicts

**Special Features**:
- Response includes expanded relationships (owner, amenities) for better API usability
- Coordinates are validated to ensure valid geographic locations
- Price validation ensures non-negative values
- Relationship integrity maintained when updating place-amenity associations

### Task 5: Review Endpoints

**Objective**: Implement API endpoints for managing reviews with full CRUD operations (Create, Read, Update, Delete). Reviews are the only entity with DELETE support in Part 2.

**Endpoints Implemented**:

1. **POST /api/v1/reviews/**: Create a new review
   - Request Body: 
     ```json
     {
       "text": string,
       "rating": integer,
       "user_id": string,
       "place_id": string
     }
     ```
   - Validates required fields
   - Validates `user_id` and `place_id` exist (returns 404 if not found)
   - Validates rating is between 1 and 5 (inclusive)
   - Automatically adds review to place's `review_ids` list
   - Returns 201 Created with review data including expanded `user` and `place` objects

2. **GET /api/v1/reviews/**: List all reviews
   - Returns 200 OK with array of all reviews
   - Each review includes:
     - Review fields: `id`, `text`, `rating`, `user_id`, `place_id`, `created_at`, `updated_at`
     - Expanded `user` object: `{ "id", "first_name", "last_name" }`
     - Expanded `place` object: `{ "id", "name" }`

3. **GET /api/v1/reviews/<review_id>**: Get review by ID
   - Returns 200 OK with review data including expanded relationships
   - Returns 404 Not Found if review doesn't exist

4. **PUT /api/v1/reviews/<review_id>**: Update review information
   - Request Body: Any combination of review fields (all optional)
   - Validates updated fields including rating constraints
   - Validates `user_id` and `place_id` if being updated
   - If `place_id` is changed, removes review from old place and adds to new place
   - Returns 200 OK with updated review data including expanded relationships
   - Returns 404 Not Found if review or related entities don't exist

5. **DELETE /api/v1/reviews/<review_id>**: Delete a review
   - Removes review from place's `review_ids` list
   - Deletes the review from repository
   - Returns 200 OK with success message: `{ "message": "Review deleted successfully" }`
   - Returns 404 Not Found if review doesn't exist

**Error Handling**:
- 400 Bad Request: Validation errors (invalid rating, missing fields, rating out of range)
- 404 Not Found: Review, user, or place not found
- 409 Conflict: Data conflicts

**Special Features**:
- Rating validation ensures values between 1 and 5
- Automatic relationship management when reviews are created, updated, or deleted
- Place's `review_ids` list is automatically maintained
- When review's `place_id` is changed, relationships are updated on both old and new places

### Task 6: Testing and Validation

**Objective**: Create comprehensive tests, implement validation logic, and document testing results.

**Test Suite Overview**:

The test suite consists of 109 tests covering all aspects of the application:

- **Unit Tests** (`tests/test_business_logic.py` - 52 tests):
  - Validator function tests (require_str, require_float, require_int, require_uuid_str)
  - User model tests (creation, validation, updates, edge cases)
  - Amenity model tests (creation, validation, updates, edge cases)
  - Place model tests (creation, validation, relationships, coordinate validation)
  - Review model tests (creation, validation, rating constraints)

- **Facade Layer Tests** (`tests/test_facade.py` - 28 tests):
  - User CRUD operations through facade
  - Amenity CRUD operations through facade
  - Place CRUD operations with relationship handling
  - Review CRUD operations with relationship handling
  - Error handling tests (ValidationError, NotFoundError, ConflictError)
  - Relationship integrity tests (place-amenity, place-review, review-user-place)

- **API Integration Tests** (`tests/test_api.py` - 29 tests):
  - All HTTP endpoints tested (GET, POST, PUT, DELETE)
  - Status code validation (200, 201, 400, 404, 409)
  - Response format validation
  - Error response validation
  - Extended attributes validation (owner, amenities, user, place objects in responses)
  - Edge cases and error scenarios

**Running Tests**:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_business_logic.py -v
pytest tests/test_facade.py -v
pytest tests/test_api.py -v

# Run specific test class
pytest tests/test_business_logic.py::TestUser -v
pytest tests/test_api.py::TestUsersAPI -v

# Run with coverage (requires pytest-cov)
pytest tests/ --cov=app --cov-report=html
```

**Test Results**:
- All 109 tests pass successfully
- 100% endpoint coverage
- Comprehensive error scenario coverage
- Relationship integrity verified

**Testing Features**:
- Isolated test fixtures to prevent side effects
- Each test creates fresh instances of the repository
- Tests validate both success cases and error cases
- Integration tests use Flask's test client (no actual HTTP server needed)
- Comprehensive edge case testing (boundary values, invalid inputs, missing fields)

**Documentation**:
- `tests/README.md`: Complete testing documentation with usage examples
- Swagger/OpenAPI documentation auto-generated by Flask-RESTx at `/api/v1/`
- All endpoints documented with request/response models

## API Documentation

The API is fully documented using Flask-RESTx, which automatically generates Swagger/OpenAPI documentation.

### Accessing Documentation

When the application is running:
- Swagger UI: `http://localhost:5000/api/v1/`
- JSON Schema: `http://localhost:5000/api/v1/swagger.json`

### API Base URL

All endpoints are prefixed with `/api/v1/`

### Response Format

All responses are in JSON format. Successful responses include the requested data, while error responses include an error message.

**Success Response Example** (201 Created):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com"
}
```

**Error Response Example** (404 Not Found):
```json
{
  "message": "users not found"
}
```

### HTTP Status Codes

- `200 OK`: Successful GET or PUT request
- `201 Created`: Successful POST request (resource created)
- `400 Bad Request`: Validation error or invalid input
- `404 Not Found`: Resource not found
- `409 Conflict`: Unique constraint violation (e.g., duplicate email)

## Testing

See the [tests/README.md](tests/README.md) file for detailed testing documentation.

### Quick Test Commands

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=term-missing

# Run specific test category
pytest tests/test_api.py -v -k "user"
```

## Architecture

### Three-Layer Architecture

The application follows a clean three-layer architecture:

1. **Presentation Layer** (`app/presentation/`):
   - Handles HTTP requests and responses
   - Validates request data using Flask-RESTx models
   - Converts business logic results to HTTP responses
   - Manages HTTP status codes and error responses

2. **Business Logic Layer** (`app/business_logic/`):
   - Contains domain models (User, Place, Review, Amenity)
   - Implements business rules and validation
   - Manages entity relationships
   - Provides `to_dict()` methods for serialization

3. **Persistence Layer** (`app/persistence/`):
   - In-memory repository implementation
   - Generic CRUD operations
   - Enforces unique constraints
   - Designed to be replaced with database persistence in Part 3

### Facade Pattern

The `HBnBFacade` class (`app/services/facade.py`) provides a unified interface for all business operations:

- **Benefits**:
  - Simplifies API endpoint code
  - Centralizes business logic
  - Reduces coupling between layers
  - Makes testing easier

- **Responsibilities**:
  - Coordinates between Presentation and Persistence layers
  - Validates business rules
  - Manages entity relationships
  - Expands relationships in responses (e.g., adding owner object to place response)

### Data Flow

```
Client Request
    ↓
Presentation Layer (API Endpoint)
    ↓
Facade Layer (HBnBFacade)
    ↓
Business Logic Layer (Domain Models)
    ↓
Persistence Layer (Repository)
    ↓
Response (with expanded relationships)
    ↓
Client Response
```

### Key Design Decisions

1. **No Password Field**: Users do not have passwords in Part 2 (authentication will be added in future parts)

2. **In-Memory Storage**: Data is stored in memory using dictionaries. This allows for easy testing and will be replaced with database persistence in Part 3

3. **Expanded Relationships**: API responses include expanded relationship objects (e.g., place responses include owner object) for better API usability

4. **Unique Constraints**: Email (users) and name (amenities) must be unique, enforced at repository level

5. **No DELETE for Most Entities**: Only Reviews support DELETE operation. Users, Places, and Amenities cannot be deleted (as per requirements)

## Summary

Part 2 successfully implements a complete RESTful API for the HBnB application with:

- 18 API endpoints across 4 entity types
- Comprehensive validation and error handling
- Full relationship management
- 109 passing tests with 100% endpoint coverage
- Clean architecture with clear separation of concerns
- Automatic API documentation via Swagger

The implementation is ready for Part 3, where the in-memory repository will be replaced with SQLAlchemy database persistence.
