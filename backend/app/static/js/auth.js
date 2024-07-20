// Project: luchoh.com refactoring
// File: backend/app/static/js/auth.js

export async function login(username, password) {
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

export function setToken(token) {
    localStorage.setItem('token', token);
    console.log('Token set:', token);
}

export function getToken() {
    return localStorage.getItem('token');
}

export function removeToken() {
    localStorage.removeItem('token');
    console.log('Token removed');
}

export function isLoggedIn() {
    return !!getToken();
}

export function logout() {
    removeToken();
    const loginForm = document.getElementById('loginForm');
    const adminContent = document.getElementById('adminContent');
    if (loginForm) loginForm.style.display = 'block';
    if (adminContent) adminContent.style.display = 'none';
    console.log('Logged out');
}

export async function checkLoginStatus() {
    if (isLoggedIn()) {
        updateUIAfterLogin();
        return true;
    } else {
        const loginForm = document.getElementById('loginForm');
        const adminContent = document.getElementById('adminContent');
        if (loginForm) loginForm.style.display = 'block';
        if (adminContent) adminContent.style.display = 'none';
        return false;
    }
}

export function updateUIAfterLogin() {
    const loginForm = document.getElementById('loginForm');
    const adminContent = document.getElementById('adminContent');
    console.log('Updating UI after login');
    console.log('loginForm:', loginForm);
    console.log('adminContent:', adminContent);
    if (loginForm) {
        loginForm.style.display = 'none';
        console.log('Login form hidden');
    }
    if (adminContent) {
        adminContent.style.display = 'block';
        console.log('Admin content shown');
    } else {
        console.warn('Admin content element not found');
    }
}
