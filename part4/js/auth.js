/**
 * HBnB Web Client - Authentication Functions
 * Handles login, logout, and authentication state
 */

/**
 * Handle login
 */
async function handleLogin() {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    // Hide previous errors
    hideError('emailError');
    hideError('passwordError');
    hideError('formError');
    hideSuccess('formSuccess');

    // Validate inputs
    if (!email) {
        showError('emailError', 'Email is required');
        return;
    }

    if (!password) {
        showError('passwordError', 'Password is required');
        return;
    }

    // Disable submit button
    const submitButton = document.getElementById('submitButton');
    submitButton.disabled = true;
    submitButton.textContent = 'Signing in...';

    try {
        // Log the request for debugging (remove in production)
        console.log('Attempting login with email:', email);
        
        const response = await apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password }),
        });

        // Store token in cookie
        if (response && response.access_token) {
            setCookie(COOKIE_NAME, response.access_token);
        } else {
            throw new Error('No access token received from server');
        }

        // Show success message
        showSuccess('formSuccess', 'Login successful! Redirecting...');

        // Redirect to index page after short delay
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 1000);
    } catch (error) {
        console.error('Login error:', error);
        // Show user-friendly error message
        let errorMessage = error.message || 'Login failed. Please check your credentials.';
        
        // Provide helpful hints based on error
        if (errorMessage.includes('connect') || errorMessage.includes('Network')) {
            errorMessage = 'Cannot connect to the server. Please make sure the API is running on http://localhost:5000';
        } else if (errorMessage.includes('401') || errorMessage.includes('Invalid email or password')) {
            errorMessage = 'Invalid email or password. Please check your credentials and try again.';
        } else if (errorMessage.includes('CORS')) {
            errorMessage = 'CORS error. Please check that CORS is configured in the backend API.';
        }
        
        showError('formError', errorMessage);
        submitButton.disabled = false;
        submitButton.textContent = 'Sign In';
    }
}

/**
 * Handle logout
 */
function handleLogout() {
    deleteCookie(COOKIE_NAME);
    window.location.href = 'index.html';
}

/**
 * Check authentication and update UI
 */
function checkAuthentication() {
    const isAuth = isAuthenticated();
    const loginLink = document.getElementById('login-link');
    const loginNavButton = document.getElementById('loginNavButton'); // For backward compatibility
    const logoutButton = document.getElementById('logoutButton');
    const adminBadge = document.getElementById('admin-badge');

    // Handle login-link (Task 2 requirement)
    // Show Login ONLY if user is NOT authenticated
    if (loginLink) {
        if (isAuth) {
            // User is logged in - HIDE login button
            loginLink.classList.add('hidden');
            loginLink.style.display = 'none';
            loginLink.style.visibility = 'hidden';
        } else {
            // User is NOT logged in - SHOW login button
            loginLink.classList.remove('hidden');
            loginLink.style.display = 'inline-block';
            loginLink.style.visibility = 'visible';
        }
    }

    // Handle loginNavButton (for other pages)
    if (loginNavButton) {
        if (isAuth) {
            loginNavButton.classList.add('hidden');
            loginNavButton.style.display = 'none';
        } else {
            loginNavButton.classList.remove('hidden');
            loginNavButton.style.display = 'inline-block';
        }
    }

    // Handle logout button
    // Show Logout ONLY if user IS authenticated
    if (logoutButton) {
        if (isAuth) {
            // User is logged in - SHOW logout button
            logoutButton.classList.remove('hidden');
            logoutButton.style.display = 'inline-block';
            logoutButton.style.visibility = 'visible';
            // Remove old listener and add new one
            logoutButton.onclick = handleLogout;
        } else {
            // User is NOT logged in - HIDE logout button
            logoutButton.classList.add('hidden');
            logoutButton.style.display = 'none';
            logoutButton.style.visibility = 'hidden';
            logoutButton.onclick = null;
        }
    }

    // Show admin badge ONLY if user is admin
    if (adminBadge) {
        const userIsAdmin = isAdmin();
        
        if (isAuth && userIsAdmin) {
            adminBadge.classList.remove('hidden');
            adminBadge.style.display = 'inline-flex';
        } else {
            adminBadge.classList.add('hidden');
            adminBadge.style.display = 'none';
        }
    }
}
