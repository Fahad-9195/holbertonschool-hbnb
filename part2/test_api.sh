#!/bin/bash

# HBnB API Testing Script using cURL
# This script performs comprehensive black-box testing of all API endpoints
# Make sure the Flask server is running on http://localhost:5000

BASE_URL="http://localhost:5000/api/v1"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "HBnB API Testing Script"
echo "=========================================="
echo ""

# Variables to store IDs for later tests
USER_ID=""
USER_ID_2=""
AMENITY_ID=""
AMENITY_ID_2=""
PLACE_ID=""
PLACE_ID_2=""
REVIEW_ID=""

# Function to print test result
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: $2"
    else
        echo -e "${RED}✗ FAIL${NC}: $2"
    fi
}

# Function to extract ID from JSON response
extract_id() {
    echo $1 | grep -o '"id":"[^"]*' | grep -o '[^"]*$'
}

echo "=========================================="
echo "1. Testing Users Endpoints"
echo "=========================================="

# Test 1.1: Create User - Success
echo ""
echo "Test 1.1: POST /users - Create user successfully"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/users" \
    -H "Content-Type: application/json" \
    -d '{
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }')
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)
if [ "$HTTP_CODE" -eq 201 ]; then
    USER_ID=$(extract_id "$BODY")
    print_result 0 "Create user - Status: $HTTP_CODE"
    echo "  User ID: $USER_ID"
else
    print_result 1 "Create user - Expected 201, got $HTTP_CODE"
fi

# Test 1.2: Create User - Missing fields
echo ""
echo "Test 1.2: POST /users - Missing required fields"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/users" \
    -H "Content-Type: application/json" \
    -d '{
        "first_name": "John"
    }')
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" -eq 400 ]; then
    print_result 0 "Missing fields validation - Status: $HTTP_CODE"
else
    print_result 1 "Missing fields validation - Expected 400, got $HTTP_CODE"
fi

# Test 1.3: Create User - Duplicate email
echo ""
echo "Test 1.3: POST /users - Duplicate email"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/users" \
    -H "Content-Type: application/json" \
    -d '{
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "john.doe@example.com"
    }')
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" -eq 409 ]; then
    print_result 0 "Duplicate email validation - Status: $HTTP_CODE"
else
    print_result 1 "Duplicate email validation - Expected 409, got $HTTP_CODE"
fi

# Test 1.4: List Users
echo ""
echo "Test 1.4: GET /users - List all users"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/users")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)
if [ "$HTTP_CODE" -eq 200 ]; then
    print_result 0 "List users - Status: $HTTP_CODE"
    echo "  Response contains users array"
else
    print_result 1 "List users - Expected 200, got $HTTP_CODE"
fi

# Test 1.5: Get User by ID
echo ""
echo "Test 1.5: GET /users/<id> - Get user by ID"
if [ -n "$USER_ID" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/users/$USER_ID")
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    if [ "$HTTP_CODE" -eq 200 ]; then
        print_result 0 "Get user by ID - Status: $HTTP_CODE"
    else
        print_result 1 "Get user by ID - Expected 200, got $HTTP_CODE"
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC}: User ID not available"
fi

# Test 1.6: Get User - Not Found
echo ""
echo "Test 1.6: GET /users/<id> - User not found"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/users/non-existent-id")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" -eq 404 ]; then
    print_result 0 "User not found - Status: $HTTP_CODE"
else
    print_result 1 "User not found - Expected 404, got $HTTP_CODE"
fi

# Create second user for later tests
echo ""
echo "Creating second user for later tests..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/users" \
    -H "Content-Type: application/json" \
    -d '{
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com"
    }')
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)
if [ "$HTTP_CODE" -eq 201 ]; then
    USER_ID_2=$(extract_id "$BODY")
    echo "  Second User ID: $USER_ID_2"
fi

echo ""
echo "=========================================="
echo "2. Testing Amenities Endpoints"
echo "=========================================="

# Test 2.1: Create Amenity - Success
echo ""
echo "Test 2.1: POST /amenities - Create amenity successfully"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/amenities" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "WiFi"
    }')
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)
if [ "$HTTP_CODE" -eq 201 ]; then
    AMENITY_ID=$(extract_id "$BODY")
    print_result 0 "Create amenity - Status: $HTTP_CODE"
    echo "  Amenity ID: $AMENITY_ID"
else
    print_result 1 "Create amenity - Expected 201, got $HTTP_CODE"
fi

# Test 2.2: Create Amenity - Missing name
echo ""
echo "Test 2.2: POST /amenities - Missing name"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/amenities" \
    -H "Content-Type: application/json" \
    -d '{}')
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" -eq 400 ]; then
    print_result 0 "Missing name validation - Status: $HTTP_CODE"
else
    print_result 1 "Missing name validation - Expected 400, got $HTTP_CODE"
fi

# Test 2.3: Create Amenity - Duplicate name
echo ""
echo "Test 2.3: POST /amenities - Duplicate name"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/amenities" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "WiFi"
    }')
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" -eq 409 ]; then
    print_result 0 "Duplicate name validation - Status: $HTTP_CODE"
else
    print_result 1 "Duplicate name validation - Expected 409, got $HTTP_CODE"
fi

# Test 2.4: List Amenities
echo ""
echo "Test 2.4: GET /amenities - List all amenities"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/amenities")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" -eq 200 ]; then
    print_result 0 "List amenities - Status: $HTTP_CODE"
else
    print_result 1 "List amenities - Expected 200, got $HTTP_CODE"
fi

# Test 2.5: Get Amenity by ID
echo ""
echo "Test 2.5: GET /amenities/<id> - Get amenity by ID"
if [ -n "$AMENITY_ID" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/amenities/$AMENITY_ID")
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    if [ "$HTTP_CODE" -eq 200 ]; then
        print_result 0 "Get amenity by ID - Status: $HTTP_CODE"
    else
        print_result 1 "Get amenity by ID - Expected 200, got $HTTP_CODE"
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC}: Amenity ID not available"
fi

# Test 2.6: Update Amenity
echo ""
echo "Test 2.6: PUT /amenities/<id> - Update amenity"
if [ -n "$AMENITY_ID" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT "$BASE_URL/amenities/$AMENITY_ID" \
        -H "Content-Type: application/json" \
        -d '{
            "name": "Free WiFi"
        }')
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    if [ "$HTTP_CODE" -eq 200 ]; then
        print_result 0 "Update amenity - Status: $HTTP_CODE"
    else
        print_result 1 "Update amenity - Expected 200, got $HTTP_CODE"
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC}: Amenity ID not available"
fi

# Create second amenity for place tests
echo ""
echo "Creating second amenity for place tests..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/amenities" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Pool"
    }')
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)
if [ "$HTTP_CODE" -eq 201 ]; then
    AMENITY_ID_2=$(extract_id "$BODY")
    echo "  Second Amenity ID: $AMENITY_ID_2"
fi

echo ""
echo "=========================================="
echo "3. Testing Places Endpoints"
echo "=========================================="

# Test 3.1: Create Place - Success
echo ""
echo "Test 3.1: POST /places - Create place successfully"
if [ -n "$USER_ID" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/places" \
        -H "Content-Type: application/json" \
        -d "{
            \"name\": \"Beautiful Apartment\",
            \"description\": \"A nice place in the city\",
            \"price\": 100.0,
            \"latitude\": 40.7128,
            \"longitude\": -74.0060,
            \"owner_id\": \"$USER_ID\"
        }")
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | head -n-1)
    if [ "$HTTP_CODE" -eq 201 ]; then
        PLACE_ID=$(extract_id "$BODY")
        print_result 0 "Create place - Status: $HTTP_CODE"
        echo "  Place ID: $PLACE_ID"
    else
        print_result 1 "Create place - Expected 201, got $HTTP_CODE"
        echo "  Response: $BODY"
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC}: User ID not available"
fi

# Test 3.2: Create Place - Missing fields
echo ""
echo "Test 3.2: POST /places - Missing required fields"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/places" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Place"
    }')
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" -eq 400 ]; then
    print_result 0 "Missing fields validation - Status: $HTTP_CODE"
else
    print_result 1 "Missing fields validation - Expected 400, got $HTTP_CODE"
fi

# Test 3.3: Create Place - Invalid owner_id
echo ""
echo "Test 3.3: POST /places - Invalid owner_id"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/places" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Place",
        "description": "Desc",
        "price": 100.0,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "owner_id": "non-existent-id"
    }')
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" -eq 404 ]; then
    print_result 0 "Invalid owner_id validation - Status: $HTTP_CODE"
else
    print_result 1 "Invalid owner_id validation - Expected 404, got $HTTP_CODE"
fi

# Test 3.4: Create Place - With amenities
echo ""
echo "Test 3.4: POST /places - Create place with amenities"
if [ -n "$USER_ID" ] && [ -n "$AMENITY_ID" ] && [ -n "$AMENITY_ID_2" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/places" \
        -H "Content-Type: application/json" \
        -d "{
            \"name\": \"Luxury Apartment\",
            \"description\": \"A luxury place with amenities\",
            \"price\": 200.0,
            \"latitude\": 40.7580,
            \"longitude\": -73.9855,
            \"owner_id\": \"$USER_ID\",
            \"amenity_ids\": [\"$AMENITY_ID\", \"$AMENITY_ID_2\"]
        }")
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | head -n-1)
    if [ "$HTTP_CODE" -eq 201 ]; then
        PLACE_ID_2=$(extract_id "$BODY")
        print_result 0 "Create place with amenities - Status: $HTTP_CODE"
        echo "  Place ID: $PLACE_ID_2"
    else
        print_result 1 "Create place with amenities - Expected 201, got $HTTP_CODE"
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC}: Required IDs not available"
fi

# Test 3.5: List Places
echo ""
echo "Test 3.5: GET /places - List all places"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/places")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" -eq 200 ]; then
    print_result 0 "List places - Status: $HTTP_CODE"
else
    print_result 1 "List places - Expected 200, got $HTTP_CODE"
fi

# Test 3.6: Get Place by ID
echo ""
echo "Test 3.6: GET /places/<id> - Get place by ID"
if [ -n "$PLACE_ID" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/places/$PLACE_ID")
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | head -n-1)
    if [ "$HTTP_CODE" -eq 200 ]; then
        print_result 0 "Get place by ID - Status: $HTTP_CODE"
        # Check if response includes owner and amenities
        if echo "$BODY" | grep -q '"owner"'; then
            echo "  ✓ Response includes owner information"
        fi
        if echo "$BODY" | grep -q '"amenities"'; then
            echo "  ✓ Response includes amenities array"
        fi
    else
        print_result 1 "Get place by ID - Expected 200, got $HTTP_CODE"
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC}: Place ID not available"
fi

# Test 3.7: Update Place
echo ""
echo "Test 3.7: PUT /places/<id> - Update place"
if [ -n "$PLACE_ID" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT "$BASE_URL/places/$PLACE_ID" \
        -H "Content-Type: application/json" \
        -d '{
            "name": "Updated Place Name",
            "price": 150.0
        }')
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    if [ "$HTTP_CODE" -eq 200 ]; then
        print_result 0 "Update place - Status: $HTTP_CODE"
    else
        print_result 1 "Update place - Expected 200, got $HTTP_CODE"
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC}: Place ID not available"
fi

# Test 3.8: List Reviews for Place
echo ""
echo "Test 3.8: GET /places/<id>/reviews - List reviews for place"
if [ -n "$PLACE_ID" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/places/$PLACE_ID/reviews")
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    if [ "$HTTP_CODE" -eq 200 ]; then
        print_result 0 "List place reviews - Status: $HTTP_CODE"
    else
        print_result 1 "List place reviews - Expected 200, got $HTTP_CODE"
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC}: Place ID not available"
fi

echo ""
echo "=========================================="
echo "4. Testing Reviews Endpoints"
echo "=========================================="

# Test 4.1: Create Review - Success
echo ""
echo "Test 4.1: POST /reviews - Create review successfully"
if [ -n "$PLACE_ID" ] && [ -n "$USER_ID_2" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/reviews" \
        -H "Content-Type: application/json" \
        -d "{
            \"text\": \"Great place! Highly recommended.\",
            \"rating\": 5,
            \"user_id\": \"$USER_ID_2\",
            \"place_id\": \"$PLACE_ID\"
        }")
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | head -n-1)
    if [ "$HTTP_CODE" -eq 201 ]; then
        REVIEW_ID=$(extract_id "$BODY")
        print_result 0 "Create review - Status: $HTTP_CODE"
        echo "  Review ID: $REVIEW_ID"
    else
        print_result 1 "Create review - Expected 201, got $HTTP_CODE"
        echo "  Response: $BODY"
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC}: Required IDs not available"
fi

# Test 4.2: Create Review - Missing fields
echo ""
echo "Test 4.2: POST /reviews - Missing required fields"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/reviews" \
    -H "Content-Type: application/json" \
    -d '{
        "text": "Great!"
    }')
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" -eq 400 ]; then
    print_result 0 "Missing fields validation - Status: $HTTP_CODE"
else
    print_result 1 "Missing fields validation - Expected 400, got $HTTP_CODE"
fi

# Test 4.3: Create Review - Invalid user_id
echo ""
echo "Test 4.3: POST /reviews - Invalid user_id"
if [ -n "$PLACE_ID" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/reviews" \
        -H "Content-Type: application/json" \
        -d "{
            \"text\": \"Great!\",
            \"rating\": 5,
            \"user_id\": \"non-existent-id\",
            \"place_id\": \"$PLACE_ID\"
        }")
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    if [ "$HTTP_CODE" -eq 404 ]; then
        print_result 0 "Invalid user_id validation - Status: $HTTP_CODE"
    else
        print_result 1 "Invalid user_id validation - Expected 404, got $HTTP_CODE"
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC}: Place ID not available"
fi

# Test 4.4: Create Review - Invalid place_id
echo ""
echo "Test 4.4: POST /reviews - Invalid place_id"
if [ -n "$USER_ID_2" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/reviews" \
        -H "Content-Type: application/json" \
        -d "{
            \"text\": \"Great!\",
            \"rating\": 5,
            \"user_id\": \"$USER_ID_2\",
            \"place_id\": \"non-existent-id\"
        }")
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    if [ "$HTTP_CODE" -eq 404 ]; then
        print_result 0 "Invalid place_id validation - Status: $HTTP_CODE"
    else
        print_result 1 "Invalid place_id validation - Expected 404, got $HTTP_CODE"
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC}: User ID not available"
fi

# Test 4.5: List Reviews
echo ""
echo "Test 4.5: GET /reviews - List all reviews"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/reviews")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" -eq 200 ]; then
    print_result 0 "List reviews - Status: $HTTP_CODE"
else
    print_result 1 "List reviews - Expected 200, got $HTTP_CODE"
fi

# Test 4.6: Get Review by ID
echo ""
echo "Test 4.6: GET /reviews/<id> - Get review by ID"
if [ -n "$REVIEW_ID" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/reviews/$REVIEW_ID")
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | head -n-1)
    if [ "$HTTP_CODE" -eq 200 ]; then
        print_result 0 "Get review by ID - Status: $HTTP_CODE"
        # Check if response includes user and place info
        if echo "$BODY" | grep -q '"user"'; then
            echo "  ✓ Response includes user information"
        fi
        if echo "$BODY" | grep -q '"place"'; then
            echo "  ✓ Response includes place information"
        fi
    else
        print_result 1 "Get review by ID - Expected 200, got $HTTP_CODE"
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC}: Review ID not available"
fi

# Test 4.7: Update Review
echo ""
echo "Test 4.7: PUT /reviews/<id> - Update review"
if [ -n "$REVIEW_ID" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT "$BASE_URL/reviews/$REVIEW_ID" \
        -H "Content-Type: application/json" \
        -d '{
            "text": "Updated review text",
            "rating": 4
        }')
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    if [ "$HTTP_CODE" -eq 200 ]; then
        print_result 0 "Update review - Status: $HTTP_CODE"
    else
        print_result 1 "Update review - Expected 200, got $HTTP_CODE"
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC}: Review ID not available"
fi

# Test 4.8: Delete Review
echo ""
echo "Test 4.8: DELETE /reviews/<id> - Delete review"
if [ -n "$REVIEW_ID" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE "$BASE_URL/reviews/$REVIEW_ID")
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    if [ "$HTTP_CODE" -eq 200 ]; then
        print_result 0 "Delete review - Status: $HTTP_CODE"
        # Verify deletion
        RESPONSE2=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/reviews/$REVIEW_ID")
        HTTP_CODE2=$(echo "$RESPONSE2" | tail -n1)
        if [ "$HTTP_CODE2" -eq 404 ]; then
            echo "  ✓ Review successfully deleted (404 on GET)"
        fi
    else
        print_result 1 "Delete review - Expected 200, got $HTTP_CODE"
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC}: Review ID not available"
fi

# Test 4.9: Get Review - Not Found
echo ""
echo "Test 4.9: GET /reviews/<id> - Review not found"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/reviews/non-existent-id")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" -eq 404 ]; then
    print_result 0 "Review not found - Status: $HTTP_CODE"
else
    print_result 1 "Review not found - Expected 404, got $HTTP_CODE"
fi

echo ""
echo "=========================================="
echo "Testing Complete!"
echo "=========================================="
echo ""
echo "Summary:"
echo "  - Users: 6 tests"
echo "  - Amenities: 6 tests"
echo "  - Places: 8 tests"
echo "  - Reviews: 9 tests"
echo ""
echo "Total: 29 test cases"
echo ""
echo "Note: Check the output above for detailed results."
echo "      Green ✓ indicates passed tests, Red ✗ indicates failed tests."
