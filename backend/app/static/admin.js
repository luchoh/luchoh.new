// Project: luchoh.com refactoring
// File: frontend/src/js/admin.js

document.addEventListener('DOMContentLoaded', function () {
    // Existing Materialize initialization
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems);

    // Existing category selection functionality
    var categorySelect = document.getElementById('category-select');
    if (categorySelect) {
        categorySelect.addEventListener('change', function () {
            var selectedCategory = this.value;
            window.location.href = '/admin/galleries/' + selectedCategory;
        });
    }

    // New: Login form handler
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const success = await login(email, password);
            if (success) {
                window.location.href = '/admin/dashboard';
            } else {
                alert('Login failed. Please check your credentials.');
            }
        });
    }

    // New: Logout button handler
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', logout);
    }

    // New: Check login status on page load
    checkLoginStatus();
});

// New: Authentication functions
async function login(email, password) {
    const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
    });

    if (response.ok) {
        const data = await response.json();
        setToken(data.access_token);
        return true;
    } else {
        return false;
    }
}

function logout() {
    setToken('');
    window.location.href = '/admin/login';
}

function setToken(token) {
    localStorage.setItem('token', token);
}

function getToken() {
    return localStorage.getItem('token');
}

function isLoggedIn() {
    return !!getToken();
}

async function checkLoginStatus() {
    if (!isLoggedIn()) {
        window.location.href = '/admin/login';
    }
}

// Modified: Use authenticated requests
async function createGallery(title, description) {
    const response = await fetch('/api/v1/galleries/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getToken()}`
        },
        body: JSON.stringify({ title, description }),
    });

    if (response.ok) {
        const newGallery = await response.json();
        return newGallery;
    } else {
        throw new Error('Failed to create gallery');
    }
}

// Modified: Use authenticated requests
async function uploadImage(file, galleryId) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('gallery_id', galleryId);

    const response = await fetch('/api/v1/images/upload/', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${getToken()}`
        },
        body: formData,
    });

    if (response.ok) {
        const newImage = await response.json();
        return newImage;
    } else {
        throw new Error('Failed to upload image');
    }
}