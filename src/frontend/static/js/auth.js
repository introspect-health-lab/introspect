// Authentication management

const AUTH_TOKEN_KEY = 'auth_token';
const USER_DATA_KEY = 'user_data';

/**
 * Get the stored authentication token
 * @returns {string|null} The auth token or null
 */
function getAuthToken() {
    return localStorage.getItem(AUTH_TOKEN_KEY);
}

/**
 * Set the authentication token
 * @param {string} token - The token to store
 */
function setAuthToken(token) {
    localStorage.setItem(AUTH_TOKEN_KEY, token);
}

/**
 * Remove the authentication token
 */
function removeAuthToken() {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    localStorage.removeItem(USER_DATA_KEY);
}

/**
 * Check if user is authenticated
 * @returns {boolean} True if authenticated
 */
function isAuthenticated() {
    return !!getAuthToken();
}

/**
 * Get stored user data
 * @returns {object|null} User data or null
 */
function getUserData() {
    const data = localStorage.getItem(USER_DATA_KEY);
    return data ? JSON.parse(data) : null;
}

/**
 * Set user data
 * @param {object} userData - User data to store
 */
function setUserData(userData) {
    localStorage.setItem(USER_DATA_KEY, JSON.stringify(userData));
}

/**
 * Sign in user
 * @param {string} email - User email
 * @param {string} password - User password
 * @returns {Promise<object>} Response data
 */
async function signIn(email, password) {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    formData.append('grant_type', 'password');
    
    const response = await fetch('/auth/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Sign in failed');
    }
    
    const data = await response.json();
    setAuthToken(data.access_token);
    
    // Fetch user data
    await fetchUserData();
    
    return data;
}

/**
 * Sign up new user
 * @param {object} userData - User registration data
 * @returns {Promise<object>} Response data
 */
async function signUp(userData) {
    const response = await fetch('/auth/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Sign up failed');
    }
    
    return response;
}

/**
 * Sign out user
 */
function signOut() {
    removeAuthToken();
    window.location.href = '/signin';
}

/**
 * Fetch current user data
 * @returns {Promise<object>} User data
 */
async function fetchUserData() {
    const token = getAuthToken();
    if (!token) {
        throw new Error('Not authenticated');
    }
    
    const response = await fetch('/users/me', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    if (!response.ok) {
        if (response.status === 401) {
            removeAuthToken();
            window.location.href = '/signin';
        }
        throw new Error('Failed to fetch user data');
    }
    
    const userData = await response.json();
    setUserData(userData);
    return userData;
}

/**
 * Make an authenticated API request
 * @param {string} url - The API endpoint
 * @param {object} options - Fetch options
 * @returns {Promise<Response>} Fetch response
 */
async function authenticatedFetch(url, options = {}) {
    const token = getAuthToken();
    if (!token) {
        window.location.href = '/signin';
        throw new Error('Not authenticated');
    }
    
    const headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
    
    const response = await fetch(url, {
        ...options,
        headers
    });
    
    if (response.status === 401) {
        removeAuthToken();
        window.location.href = '/signin';
        throw new Error('Session expired');
    }
    
    return response;
}

/**
 * Protect a page - redirect to signin if not authenticated
 */
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = '/signin';
    }
}

/**
 * Redirect to todos if already authenticated
 */
function redirectIfAuthenticated() {
    if (isAuthenticated()) {
        window.location.href = '/dashboard';
    }
}

