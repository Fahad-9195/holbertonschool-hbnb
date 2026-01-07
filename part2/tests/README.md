# HBnB API Tests

This directory contains comprehensive tests for the HBnB API implementation.

## Test Structure

- `test_business_logic.py` - Unit tests for business logic models (User, Place, Review, Amenity) and validators
- `test_facade.py` - Unit tests for the service layer (HBnBFacade)
- `test_api.py` - Integration tests for API endpoints using Flask test client

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you're in the `part2` directory:
```bash
cd part2
```

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Files
```bash
# Business logic tests
pytest tests/test_business_logic.py -v

# Facade service tests
pytest tests/test_facade.py -v

# API integration tests
pytest tests/test_api.py -v
```

### Run Specific Test Classes
```bash
pytest tests/test_business_logic.py::TestUser -v
pytest tests/test_facade.py::TestUserFacade -v
```

### Run with Coverage (if pytest-cov is installed)
```bash
pytest tests/ --cov=app --cov-report=html
```

## Test Coverage

### Business Logic Tests
- Validator functions (require_str, require_float, require_int, require_uuid_str)
- User model validation and operations
- Amenity model validation and operations
- Place model validation and operations
- Review model validation and operations

### Facade Tests
- User CRUD operations
- Amenity CRUD operations
- Place CRUD operations (with relationships)
- Review CRUD operations (with relationships)
- Error handling (ValidationError, NotFoundError, ConflictError)

### API Integration Tests
- All HTTP endpoints (GET, POST, PUT, DELETE)
- Status code validation
- Response format validation
- Error response validation
- Extended attributes (owner, amenities, user, place)

## Expected Results

All tests should pass. If any test fails:
1. Check that the Flask app is properly configured
2. Verify all dependencies are installed
3. Check that the business logic models are correctly implemented
4. Review error messages for specific issues

## Notes

- Tests use isolated test fixtures to avoid side effects
- Each test creates fresh instances of the repository
- Tests validate both success cases and error cases
- Integration tests use Flask's test client (no actual HTTP server needed)
