# Part 4 - HBnB Web Client

A modern, responsive front-end web application for the HBnB platform built with HTML5, CSS3, and JavaScript ES6. This client provides a beautiful user interface that seamlessly connects with the RESTful API backend developed in Part 3.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Pages](#pages)
- [Architecture](#architecture)
- [API Integration](#api-integration)
- [Frontend-Backend Connection](#frontend-backend-connection)
- [Setup Instructions](#setup-instructions)
- [Configuration](#configuration)
- [Design System](#design-system)
- [Tasks Compliance](#tasks-compliance)
- [Browser Compatibility](#browser-compatibility)

## 🎯 Overview

Part 4 implements a complete front-end web client that allows users to:
- Browse and filter available places
- View detailed information about places
- Register and login with JWT authentication
- Add reviews for places
- Experience a modern, responsive UI with smooth animations

The application follows modern web development practices with modular JavaScript, organized CSS, and semantic HTML5.

## ✨ Features

### Authentication
- **User Registration**: Create new accounts with first name, last name, email, and password
- **User Login**: Secure authentication using JWT tokens
- **Token Management**: JWT tokens stored in HTTP-only cookies
- **Session Management**: Automatic authentication state checking
- **Admin Support**: Special admin badge and privileges for admin users

### Places Management
- **Places Listing**: Grid view of all available places with images
- **Price Filtering**: Filter places by maximum price ($10, $50, $100, or All)
- **Place Details**: Comprehensive information including:
  - Name, description, and price
  - Host/owner information
  - Location (latitude/longitude)
  - Amenities list
  - Reviews and ratings
- **Responsive Cards**: Beautiful place cards with hover effects

### Reviews System
- **View Reviews**: Display all reviews for a place with ratings
- **Add Reviews**: Authenticated users can add reviews (1-5 stars)
- **Owner Protection**: Place owners cannot review their own places
- **User Information**: Reviews show reviewer names and ratings

### User Experience
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Modern UI**: Clean, professional design with smooth animations
- **Error Handling**: User-friendly error messages for all operations
- **Loading States**: Visual feedback during API requests
- **Empty States**: Helpful messages when no data is available

## 📁 Project Structure

```
part4/
├── css/
│   ├── variables.css      # CSS variables and color palette
│   ├── base.css           # Reset, typography, and base styles
│   ├── layout.css         # Header, footer, and page structure
│   ├── components.css     # Cards, forms, buttons, and UI components
│   └── style.css          # Main stylesheet (imports all modules)
├── js/
│   ├── utils.js           # Configuration, cookies, API requests, helpers
│   ├── auth.js            # Authentication functions (login, logout, check auth)
│   ├── places.js          # Places loading, display, and filtering
│   ├── reviews.js         # Reviews loading and submission
│   ├── animations.js      # Scroll reveal and animation effects
│   └── scripts.js         # Main entry point (legacy support)
├── images/
│   ├── logo.svg           # Application logo (SVG)
│   └── icon.svg           # Favicon (SVG)
├── index.html             # Main page - List of Places
├── login.html             # Login page
├── register.html          # Registration page
├── place.html             # Place details page
├── add_review.html        # Add review form page
└── README.md              # This file
```

## 📄 Pages

### 1. Index Page (`index.html`)

**Purpose**: Display all available places in a grid layout

**Features**:
- Grid of place cards showing name, price, and image
- Price filter dropdown (10, 50, 100, All)
- "View Details" button on each card
- Login link (shown only if user is not authenticated)
- Logout button (shown only if user is authenticated)
- Admin badge (shown only for admin users)

**Required IDs** (Task 2):
- `id="places-list"` - Container for places grid
- `id="price-filter"` - Price filter dropdown
- `id="login-link"` - Login link in navigation

**Functionality**:
- Fetches all places from `/api/v1/places/`
- Client-side filtering by price
- Dynamic loading with visual feedback
- Responsive grid layout

### 2. Login Page (`login.html`)

**Purpose**: User authentication

**Features**:
- Email and password input fields
- Form validation
- Error message display
- Success message on login
- Automatic redirect to index after login

**Required Functionality** (Task 1):
- Stores JWT token in cookie upon successful login
- Redirects to index page after login
- Displays error messages on login failure
- Event listener on form submission with `preventDefault()`

**API Endpoint**: `POST /api/v1/auth/login`

### 3. Register Page (`register.html`)

**Purpose**: New user registration

**Features**:
- Registration form with:
  - First name
  - Last name
  - Email
  - Password
- Form validation
- Automatic login after successful registration
- Redirect to index page

**API Endpoint**: `POST /api/v1/auth/register`

### 4. Place Details Page (`place.html`)

**Purpose**: Display detailed information about a specific place

**Features**:
- Place name and price
- Full description
- Host/owner information (fetched from API)
- Location coordinates (latitude/longitude)
- Amenities list (fetched from API)
- Reviews section with ratings
- Add review form (shown only if user is authenticated and not the owner)
- Admin actions (delete button for admin users)

**Required IDs** (Task 3):
- `id="place-details"` - Place details section
- `id="add-review"` - Add review form section

**Functionality**:
- Extracts place ID from URL query parameters (`?id=<place_id>`)
- Fetches place details from `/api/v1/places/<id>`
- Fetches owner information from `/api/v1/users/<owner_id>`
- Fetches amenities from `/api/v1/amenities/<id>` for each amenity
- Loads reviews for the place
- Hides add review form if user is the place owner

**API Endpoints**:
- `GET /api/v1/places/<id>`
- `GET /api/v1/users/<id>`
- `GET /api/v1/amenities/<id>`
- `GET /api/v1/reviews/` (filtered by place_id)

### 5. Add Review Page (`add_review.html`)

**Purpose**: Allow authenticated users to add reviews for places

**Features**:
- Review form with:
  - Place ID (extracted from URL or input)
  - Review text (textarea)
  - Rating (1-5 stars, dropdown)
- Form validation
- Authentication check (redirects to index if not logged in)
- Redirect to place details page after submission

**Required IDs** (Task 4):
- `id="review-form"` - Review form element

**Functionality**:
- Extracts place ID from URL query parameters (`?place_id=<id>`)
- Requires authentication (redirects if not logged in)
- Validates form inputs
- Submits review to API
- Redirects to place details page after successful submission

**API Endpoint**: `POST /api/v1/reviews/`

## 🏗️ Architecture

### JavaScript Modules

#### `utils.js` - Core Utilities
- **Configuration**: API base URL, cookie name
- **Cookie Functions**: Get, set, delete cookies
- **Authentication Helpers**: 
  - `getAuthToken()` - Get JWT token from cookie
  - `isAuthenticated()` - Check if user is logged in
  - `isAdmin()` - Check if user is admin (from JWT claims)
  - `getCurrentUserInfo()` - Extract user info from token
- **API Request Function**: `apiRequest(endpoint, options)` - Centralized API communication
- **UI Helpers**: Error/success message display
- **Formatting**: Price formatting, HTML escaping, star rating generation

#### `auth.js` - Authentication
- `handleLogin()` - Process login form submission
- `handleLogout()` - Clear token and redirect
- `checkAuthentication()` - Update UI based on auth state

#### `places.js` - Places Management
- `loadPlaces()` - Fetch and display all places
- `displayPlaces(places)` - Render places in grid
- `filterPlacesByPrice()` - Filter places by maximum price
- `loadPlaceDetails()` - Load and display place details
- `deletePlace(placeId)` - Delete place (admin only)

#### `reviews.js` - Reviews Management
- `loadReviews(placeId)` - Load and display reviews for a place
- `handleReviewSubmit()` - Submit new review form
- `displayReviews(reviews)` - Render reviews list

#### `animations.js` - UI Animations
- Scroll reveal animations
- Smooth transitions
- Loading animations

### CSS Architecture

#### `variables.css`
- CSS custom properties for colors, spacing, typography
- Color palette definitions
- Responsive breakpoints

#### `base.css`
- CSS reset
- Typography styles
- Base element styles

#### `layout.css`
- Header and navigation
- Footer
- Page structure
- Grid and flexbox layouts

#### `components.css`
- Place cards
- Review cards
- Forms and inputs
- Buttons
- Loading states
- Empty states

#### `style.css`
- Main stylesheet that imports all modules
- Global styles

## 🔌 API Integration

### Base Configuration

The API base URL is configured in `js/utils.js`:

```javascript
const API_BASE_URL = 'http://localhost:5000/api/v1';
```

### Authentication Endpoints

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | User login | No |

### Places Endpoints

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| GET | `/api/v1/places/` | List all places | No |
| GET | `/api/v1/places/<id>` | Get place details | No |
| DELETE | `/api/v1/places/<id>` | Delete place | Yes (Admin) |

### Reviews Endpoints

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| GET | `/api/v1/reviews/` | List all reviews | No |
| POST | `/api/v1/reviews/` | Create review | Yes |

### Users Endpoints

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| GET | `/api/v1/users/<id>` | Get user information | No |

### Amenities Endpoints

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| GET | `/api/v1/amenities/<id>` | Get amenity information | No |

### Request Format

All API requests use the `apiRequest()` function which:
- Automatically adds `Authorization: Bearer <token>` header if user is authenticated
- Sets `Content-Type: application/json` header
- Handles errors with user-friendly messages
- Returns parsed JSON responses

**Example**:
```javascript
// GET request
const places = await apiRequest('/places/');

// POST request
const response = await apiRequest('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password })
});
```

### Authentication

JWT tokens are:
- Stored in cookies with name `hbnb_token`
- Automatically included in API request headers
- Decoded client-side to check admin status (for UI only)
- Server always verifies tokens on protected endpoints

## 🔗 Frontend-Backend Connection

### Connection Flow

```
Frontend (Part 4)          Backend (Part 3)
     │                           │
     │  HTTP Request             │
     ├──────────────────────────>│
     │  (fetch API)              │
     │                           │
     │  JSON Response            │
     │<──────────────────────────┤
     │                           │
```

### Technical Details

1. **Frontend Server**: 
   - Serves static files (HTML, CSS, JS)
   - Typically runs on `http://localhost:8000` or `http://localhost:3000`
   - Can use Python's HTTP server: `python -m http.server 8000`

2. **Backend Server**:
   - Flask API server
   - Runs on `http://localhost:5000`
   - Started with: `python run.py` (in part3 directory)

3. **CORS Configuration**:
   - Backend (Part 3) has CORS enabled in `app/__init__.py`
   - Allows requests from frontend origins
   - Configured to accept `Authorization` header

4. **Communication Protocol**:
   - RESTful API over HTTP/HTTPS
   - JSON request/response format
   - JWT authentication via Bearer tokens

### Database Connection

The backend connects to a SQLite database:
- **Location**: `part3/instance/hbnb_dev.db`
- **Schema**: Defined in `part3/schema.sql`
- **Initial Data**: Loaded from `part3/data.sql`

The frontend does NOT directly access the database. All data operations go through the API.

## 🚀 Setup Instructions

### Prerequisites

- Python 3.7+ (for backend)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Backend API running (Part 3)

### Step 1: Start the Backend API

```bash
# Navigate to part3 directory
cd part3

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run the Flask server
python run.py
```

The API should now be running on `http://localhost:5000`

### Step 2: Start the Frontend Server

Open a new terminal:

```bash
# Navigate to part4 directory
cd part4

# Start a simple HTTP server
# Option 1: Python 3
python -m http.server 8000

# Option 2: Python 2
python -m SimpleHTTPServer 8000

# Option 3: Node.js (if you have http-server installed)
npx http-server -p 8000

# Option 4: PHP
php -S localhost:8000
```

### Step 3: Open in Browser

Open your web browser and navigate to:
```
http://localhost:8000
```

### Step 4: Test the Application

1. **Register a new account**:
   - Click "Login" → "Register"
   - Fill in the registration form
   - You'll be automatically logged in

2. **Browse places**:
   - View all places on the index page
   - Use the price filter to filter places
   - Click "View Details" on any place

3. **Add a review**:
   - Go to a place details page
   - Scroll to the reviews section
   - Fill in the review form and submit

4. **Test admin features** (if you have admin account):
   - Login with admin credentials
   - You'll see an "Admin" badge
   - You can delete places (admin only)

### Default Admin Account

The backend includes a default admin account:
- **Email**: `admin@hbnb.io`
- **Password**: `admin1234`

This account is created automatically when the database is initialized.

## ⚙️ Configuration

### API Base URL

To change the API server URL, edit `js/utils.js`:

```javascript
const API_BASE_URL = 'http://localhost:5000/api/v1';
```

Change `localhost:5000` to your API server address.

### Cookie Settings

Cookie name and expiration can be modified in `js/utils.js`:

```javascript
const COOKIE_NAME = 'hbnb_token';

function setCookie(name, value, days = 7) {
    // days = 7 means cookie expires in 7 days
}
```

### CORS Configuration

CORS is configured in the backend (Part 3). If you need to add new origins, edit `part3/app/__init__.py`:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:8000", "http://your-new-origin:port"],
        ...
    }
})
```

## 🎨 Design System

### Color Palette

- **Primary**: `#FF5A5F` (Coral Red) - Main brand color
- **Secondary**: `#00A699` (Teal) - Accent color
- **Accent**: `#FC642D` (Orange) - Highlight color
- **Text Primary**: `#2C3E50` (Dark Blue-Gray)
- **Text Secondary**: `#7F8C8D` (Gray)
- **Background**: `#F7F9FC` (Light Gray)
- **Background Secondary**: `#FFFFFF` (White)
- **Border**: `#E1E8ED` (Light Gray)

### Typography

- **Primary Font**: Inter (sans-serif) - Body text
- **Heading Font**: Poppins (sans-serif) - Headings
- **Font Sizes**: Responsive scale from 0.875rem to 2.5rem
- **Line Height**: 1.5 for body, 1.2 for headings

### Components

#### Place Cards
- Margin: `20px`
- Padding: `10px`
- Border: `1px solid #ddd`
- Border radius: `10px`
- Hover effect: Elevation change
- Image: Hotel photos from Unsplash with fallback

#### Review Cards
- Margin: `20px`
- Padding: `10px`
- Border: `1px solid #ddd`
- Border radius: `10px`
- Star rating display

#### Buttons
- Primary: Coral red background
- Hover: Darker shade
- Transition: Smooth 0.3s
- Border radius: `8px`

#### Forms
- Input fields with focus states
- Error messages in red
- Success messages in green
- Validation feedback

### Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## ✅ Tasks Compliance

### Task 0: Design ✅

- ✅ Complete HTML structure for all pages using semantic HTML5
- ✅ Modern CSS styling with beautiful design
- ✅ Responsive layout for all screen sizes
- ✅ Valid HTML5 (W3C compliant)
- ✅ All required classes and IDs:
  - `logo` class for logo
  - `login-button` class for login button
  - `details-button` class for view details button
  - `place-card` class for place cards
  - `review-card` class for review cards
  - `place-details` class for place details
  - `place-info` class for place information
  - `add-review` class for add review form
- ✅ Fixed parameters:
  - Margin: 20px for place and review cards
  - Padding: 10px within place and review cards
  - Border: 1px solid #ddd for place and review cards
  - Border radius: 10px for place and review cards

### Task 1: Login ✅

- ✅ Login form with email and password
- ✅ JWT token storage in cookies
- ✅ Authentication state management
- ✅ Redirect after successful login
- ✅ Error message display on login failure
- ✅ Event listener on form submission with `preventDefault()`

### Task 2: Index ✅

- ✅ Display all places in a grid layout
- ✅ Place cards with name, price, and details button
- ✅ Client-side filtering by price (10, 50, 100, All)
- ✅ Uses `id="places-list"` for places container
- ✅ Uses `id="price-filter"` for price filter dropdown
- ✅ Uses `id="login-link"` for login link
- ✅ Shows login link only if user is not authenticated
- ✅ Fetches places data from API
- ✅ Populates places list dynamically

### Task 3: Place Details ✅

- ✅ Detailed place information display
- ✅ Uses `id="place-details"` for place details section
- ✅ Uses `id="add-review"` for add review form
- ✅ Extracts place ID from URL query parameters
- ✅ Host information
- ✅ Amenities list
- ✅ Reviews display with ratings
- ✅ Shows add review form only if user is authenticated
- ✅ Fetches place details from API using place ID
- ✅ Hides add review form if user is the place owner

### Task 4: Add Review ✅

- ✅ Review form with text and rating
- ✅ Uses `id="review-form"` for review form
- ✅ Authentication required - redirects to index if not logged in
- ✅ Extracts place ID from URL query parameters
- ✅ Redirects to place details page after submission
- ✅ Error handling and validation
- ✅ Event listener on form submission with `preventDefault()`

## 🌐 Browser Compatibility

### Supported Browsers

- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

### Features Used

- ES6 JavaScript (arrow functions, async/await, const/let)
- Fetch API
- CSS Grid and Flexbox
- CSS Custom Properties (Variables)
- CSS Animations and Transitions

### Polyfills

No polyfills required for modern browsers. For older browser support, consider:
- Babel for ES6 transpilation
- Fetch polyfill for IE11
- CSS Grid polyfill for older browsers

## 📝 Notes

### Images

- Place images are loaded from Unsplash with hotel-themed photos
- If images fail to load, a fallback with a hotel icon is displayed
- Images use lazy loading for better performance

### Error Handling

- All API calls include comprehensive error handling
- User-friendly error messages displayed to users
- Console logging for debugging (can be removed in production)
- Network error detection and helpful messages

### Security

- JWT tokens stored in cookies (consider HttpOnly in production)
- XSS protection via HTML escaping
- CORS properly configured
- Input validation on forms
- Server-side validation always enforced (client-side is for UX only)

### Performance

- Lazy loading for images
- Efficient DOM manipulation
- Minimal API calls (caching where appropriate)
- Optimized CSS (modular structure)
- No external dependencies (vanilla JavaScript)

## 🔧 Troubleshooting

### Common Issues

1. **CORS Errors**:
   - Make sure backend CORS is configured correctly
   - Check that frontend origin is in allowed origins list
   - Verify backend is running on correct port

2. **API Connection Failed**:
   - Verify backend is running: `http://localhost:5000`
   - Check API base URL in `js/utils.js`
   - Check browser console for detailed error messages

3. **Authentication Not Working**:
   - Check that cookies are enabled in browser
   - Verify JWT token is being stored in cookies
   - Check browser console for token errors

4. **Images Not Loading**:
   - Check internet connection (Unsplash images require internet)
   - Verify CORS settings for image sources
   - Fallback images should display if main images fail

5. **Styles Not Applied**:
   - Verify CSS files are in correct location
   - Check browser console for 404 errors
   - Clear browser cache

## 📚 Additional Resources

- [Part 3 README](../part3/README.md) - Backend API documentation
- [Main README](../README.md) - Overall project documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MDN Web Docs](https://developer.mozilla.org/) - JavaScript, HTML, CSS reference

## 📄 License

This project is part of the Holberton School curriculum.

---

**Last Updated**: 2024
**Version**: 1.0.0
