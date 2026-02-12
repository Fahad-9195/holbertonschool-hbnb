/**
 * HBnB Web Client - Utility Functions
 * Configuration, cookies, API requests, and helper functions
 */

// ========== Configuration ==========
const API_BASE_URL = 'http://localhost:5000/api/v1';
const COOKIE_NAME = 'hbnb_token';

// ========== Cookie Functions ==========

/**
 * Get cookie value by name
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

/**
 * Set cookie
 */
function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/;SameSite=Lax`;
}

/**
 * Delete cookie
 */
function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
}

/**
 * Get authentication token
 */
function getAuthToken() {
    return getCookie(COOKIE_NAME);
}

/**
 * Check if user is authenticated
 */
function isAuthenticated() {
    return getAuthToken() !== null;
}

/**
 * Decode JWT token to get claims (without verification)
 * Note: This is for client-side UI only. Server always verifies tokens.
 */
function decodeJWT(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch (error) {
        console.error('Error decoding JWT:', error);
        return null;
    }
}

/**
 * Check if current user is admin
 */
function isAdmin() {
    const token = getAuthToken();
    if (!token) {
        return false;
    }
    
    try {
        const decoded = decodeJWT(token);
        if (!decoded || typeof decoded !== 'object') {
            return false;
        }
        
        // Check if is_admin exists and is explicitly true (boolean)
        // Must be boolean true, not truthy value
        const isAdminValue = decoded.is_admin;
        
        // Only return true if is_admin is explicitly boolean true
        // Reject: undefined, null, false, 0, '', 'true', etc.
        // This ensures only real admins get admin privileges
        return isAdminValue === true;
    } catch (error) {
        console.error('Error checking admin status:', error);
        return false;
    }
}

/**
 * Get current user info from token
 */
function getCurrentUserInfo() {
    const token = getAuthToken();
    if (!token) return null;
    
    const decoded = decodeJWT(token);
    if (!decoded) return null;
    
    return {
        user_id: decoded.sub || decoded.identity,
        is_admin: decoded.is_admin === true
    };
}

/**
 * Get authorization headers for API requests
 */
function getAuthHeaders() {
    const token = getAuthToken();
    const headers = {
        'Content-Type': 'application/json',
    };
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
}

// ========== API Request Function ==========

/**
 * Make API request
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
        ...options,
        headers: {
            ...getAuthHeaders(),
            ...(options.headers || {}),
        },
    };

    try {
        const response = await fetch(url, config);
        
        // Check if response has JSON content
        let data = {};
        const contentType = response.headers.get('content-type') || '';
        
        // Clone response to read it multiple times if needed
        const responseClone = response.clone();
        
        try {
            if (contentType.includes('application/json')) {
                data = await response.json();
            } else {
                // If not JSON, try to get text
                const text = await response.text();
                if (text && text.trim()) {
                    try {
                        data = JSON.parse(text);
                    } catch (parseError) {
                        // If parsing fails, check if it's HTML error page
                        if (text.includes('401') || text.includes('Unauthorized')) {
                            data = { message: 'Invalid email or password. Please check your credentials.' };
                        } else {
                            data = { message: text.substring(0, 200) || `HTTP error! status: ${response.status}` };
                        }
                    }
                }
            }
        } catch (parseError) {
            // If we can't parse the response, create a basic error object
            console.error('Error parsing response:', parseError);
            data = { message: `Server error: ${response.status} ${response.statusText}` };
        }

        if (!response.ok) {
            // Handle specific error codes
            if (response.status === 401) {
                const errorMsg = data.message || data.error || 'Invalid email or password. Please check your credentials.';
                throw new Error(errorMsg);
            }
            if (response.status === 400) {
                const errorMsg = data.message || data.error || 'Invalid request. Please check your input.';
                throw new Error(errorMsg);
            }
            if (response.status === 404) {
                const errorMsg = data.message || data.error || 'Resource not found.';
                throw new Error(errorMsg);
            }
            if (response.status === 500) {
                const errorMsg = data.message || data.error || 'Server error. Please try again later.';
                throw new Error(errorMsg);
            }
            // Generic error
            throw new Error(data.message || data.error || `HTTP error! status: ${response.status}`);
        }

        return data;
    } catch (error) {
        console.error('API Request Error:', error);
        
        // Handle network errors (CORS, connection refused, etc.)
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            throw new Error('Cannot connect to the server. Please make sure the API is running on http://localhost:5000 and CORS is configured.');
        }
        
        // Handle CORS errors specifically
        if (error.message.includes('CORS') || error.message.includes('cross-origin')) {
            throw new Error('CORS error: The API server needs to allow requests from this origin. Please configure CORS in the Flask API.');
        }
        
        // Re-throw with a more user-friendly message if it's a generic network error
        if (!error.message || error.message === 'Failed to fetch') {
            throw new Error('Network error: Unable to connect to the API server. Please check if the server is running and CORS is configured.');
        }
        
        throw error;
    }
}

// ========== UI Helper Functions ==========

/**
 * Show error message
 */
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        element.classList.remove('hidden');
    }
}

/**
 * Hide error message
 */
function hideError(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.add('hidden');
        element.textContent = '';
    }
}

/**
 * Show success message
 */
function showSuccess(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        element.classList.remove('hidden');
    }
}

/**
 * Hide success message
 */
function hideSuccess(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.add('hidden');
        element.textContent = '';
    }
}

// ========== Helper Functions ==========

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Format price
 */
function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
    }).format(price);
}

/**
 * Generate star rating HTML
 */
function generateStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    let stars = '';

    for (let i = 0; i < 5; i++) {
        if (i < fullStars) {
            stars += '<span class="rating-star">★</span>';
        } else if (i === fullStars && hasHalfStar) {
            stars += '<span class="rating-star">★</span>';
        } else {
            stars += '<span class="rating-star empty">★</span>';
        }
    }

    return stars;
}
