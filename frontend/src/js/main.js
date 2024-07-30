/*Project: luchoh.com refactoring
File: frontend/src/js/main.js*/

let apiBaseUrl = '';

async function fetchConfig() {
    const response = await fetch('/config');
    const config = await response.json();
    apiBaseUrl = config.apiBaseUrl;
}

async function fetchImagesByTag(tagName) {
    try {
        const response = await fetch(`/tag/${tagName}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const html = await response.text();
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;
        const newImageList = tempDiv.querySelector('#image-list');
        if (newImageList) {
            document.getElementById('image-list').innerHTML = newImageList.innerHTML;
        }
        setupLightbox();
    } catch (error) {
        console.error('Error fetching images by tag:', error);
    }
}

function setupTagNavigation() {
    const tagLinks = document.querySelectorAll('.tag-link');
    tagLinks.forEach(link => {
        link.addEventListener('click', async (e) => {
            e.preventDefault();
            const tagName = e.target.dataset.tag;
            await fetchImagesByTag(tagName);
            history.pushState(null, '', `/tag/${tagName}`);
        });
    });
}

function setupLightbox() {
    if (typeof lightbox !== 'undefined') {
        lightbox.option({
            'resizeDuration': 200,
            'wrapAround': true,
            'albumLabel': "Image %1 of %2",
            'fadeDuration': 300
        });
        lightbox.init();
    }
}

function setupMobileMenu() {
    const mobileMenuToggle = document.querySelector('.button-collapse');
    const mobileMenu = document.querySelector('#mobile-menu');

    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('active');
        });
    }
}

function isLoggedIn() {
    return !!localStorage.getItem('token');
}

async function checkLoginStatus() {
    const token = localStorage.getItem('token');
    if (!token) return false;

    try {
        const response = await fetch(`${apiBaseUrl}/auth/login/test-token`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        return response.ok;
    } catch (error) {
        console.error('Error checking login status:', error);
        return false;
    }
}

async function checkSuperuserStatus() {
    const token = localStorage.getItem('token');
    if (!token) return false;

    try {
        const response = await fetch(`${apiBaseUrl}/auth/login/test-token`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (response.ok) {
            const userData = await response.json();
            return userData.is_superuser;
        }
        return false;
    } catch (error) {
        console.error('Error checking superuser status:', error);
        return false;
    }
}

async function login(username, password) {
    try {
        const response = await fetch(`${apiBaseUrl}/auth/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            return true;
        }
        return false;
    } catch (error) {
        console.error('Login error:', error);
        return false;
    }
}

function logout() {
    localStorage.removeItem('token');
    updateAuthUI();
}

function updateAuthUI() {
    const loggedIn = isLoggedIn();
    const authMenuItem = document.getElementById('auth-menu-item');
    const authMenuItemMobile = document.getElementById('auth-menu-item-mobile');
    const signOutMenuItem = document.getElementById('sign-out-menu-item');
    const signOutMenuItemMobile = document.getElementById('sign-out-menu-item-mobile');
    const manageMenuItem = document.getElementById('manage-menu-item');
    const manageMenuItemMobile = document.getElementById('manage-menu-item-mobile');

    if (loggedIn) {
        authMenuItem.style.display = 'none';
        authMenuItemMobile.style.display = 'none';
        signOutMenuItem.style.display = 'inline-block';
        signOutMenuItemMobile.style.display = 'block';

        checkSuperuserStatus().then(isSuperuser => {
            manageMenuItem.style.display = isSuperuser ? 'inline-block' : 'none';
            manageMenuItemMobile.style.display = isSuperuser ? 'block' : 'none';
        });
    } else {
        authMenuItem.style.display = 'inline-block';
        authMenuItemMobile.style.display = 'block';
        signOutMenuItem.style.display = 'none';
        signOutMenuItemMobile.style.display = 'none';
        manageMenuItem.style.display = 'none';
        manageMenuItemMobile.style.display = 'none';
    }
}

function setupAuthUI() {
    const loginModal = M.Modal.init(document.getElementById('login-modal'), {
        dismissible: true,
        opacity: 0.9,
        inDuration: 300,
        outDuration: 200,
        startingTop: '4%',
        endingTop: '10%'
    });

    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const success = await login(username, password);
        if (success) {
            loginModal.close();
            updateAuthUI();
            loginForm.reset();
        } else {
            alert('Login failed. Please check your credentials.');
        }
    });

    const signOutAction = document.getElementById('sign-out-action');
    const signOutActionMobile = document.getElementById('sign-out-action-mobile');

    signOutAction.addEventListener('click', (e) => {
        e.preventDefault();
        logout();
    });

    signOutActionMobile.addEventListener('click', (e) => {
        e.preventDefault();
        logout();
    });

    updateAuthUI();
}

document.addEventListener('DOMContentLoaded', async () => {
    await fetchConfig();
    setupTagNavigation();
    setupLightbox();
    setupMobileMenu();
    setupAuthUI();
});