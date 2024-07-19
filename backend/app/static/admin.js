// Project: luchoh.com refactoring
// File: backend/app/static/admin.js

document.addEventListener('DOMContentLoaded', function () {
    // Login form handler
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const success = await login(username, password);
            if (success) {
                document.getElementById('loginForm').style.display = 'none';
                document.getElementById('adminContent').style.display = 'block';
            } else {
                alert('Login failed. Please check your credentials.');
            }
        });
    }

    // Upload form handler
    const uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const file = document.getElementById('image-file').files[0];
            const name = document.getElementById('image-name').value;
            const title = document.getElementById('image-title').value;
            const description = document.getElementById('image-description').value;
            try {
                await uploadImage(file, name, title, description);
                alert('Image uploaded successfully');
            } catch (error) {
                alert('Failed to upload image: ' + error.message);
            }
        });
    }

    // Check login status on page load
    checkLoginStatus();
});

async function login(username, password) {
    const response = await fetch('/api/v1/auth/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
    });

    if (response.ok) {
        const data = await response.json();
        setToken(data.access_token);
        return true;
    } else {
        return false;
    }
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
    if (isLoggedIn()) {
        document.getElementById('loginForm').style.display = 'none';
        document.getElementById('adminContent').style.display = 'block';
    }
}

async function uploadImage(file, name, title, description) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('name', name);
    formData.append('title', title);
    formData.append('description', description);

    const response = await fetch('/api/v1/images/upload/', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${getToken()}`
        },
        body: formData,
    });

    if (!response.ok) {
        throw new Error('Failed to upload image');
    }

    return await response.json();
}