// Project: luchoh.com refactoring
// File: backend/app/static/js/admin.js

import * as auth from './auth.js';
import * as gallery from './gallery.js';
import * as image from './image.js';
import { handleError } from './utils.js';

async function initializeAdmin() {
    console.log('Initializing admin page');
    setupLoginForm();
    setupUploadForm();
    setupGalleryForm();
    setupEditImageForm();
    setupLogoutButton();

    const isLoggedIn = await auth.checkLoginStatus();
    if (isLoggedIn) {
        console.log('User is logged in, loading data');
        await loadAdminData();
    } else {
        console.log('User is not logged in');
    }
}

async function loadAdminData() {
    try {
        await gallery.loadGalleries();
        await image.loadImages();
    } catch (error) {
        console.error('Error loading admin data:', error);
        handleError(error);
    }
}

function setupLoginForm() {
    const loginForm = document.getElementById('login-form');
    console.log('Login form:', loginForm);
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    } else {
        console.warn('Login form not found');
    }
}

async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    try {
        const success = await auth.login(username, password);
        if (success) {
            console.log('Login successful');
            auth.updateUIAfterLogin();
            await loadAdminData();
        } else {
            console.log('Login failed');
            alert('Login failed. Please check your credentials.');
        }
    } catch (error) {
        console.error('Error during login:', error);
        handleError(error);
    }
}

function setupUploadForm() {
    const uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', handleImageUpload);
    }
}

async function handleImageUpload(e) {
    e.preventDefault();
    const file = document.getElementById('image-file').files[0];
    const title = document.getElementById('image-title').value;
    const description = document.getElementById('image-description').value;
    try {
        await image.uploadImage(file, title, description);
        alert('Image uploaded successfully');
        e.target.reset();
        await image.loadImages();
    } catch (error) {
        handleError(error);
    }
}

function setupGalleryForm() {
    const galleryForm = document.getElementById('gallery-form');
    if (galleryForm) {
        galleryForm.addEventListener('submit', handleGalleryCreation);
    }
}

async function handleGalleryCreation(e) {
    e.preventDefault();
    const title = document.getElementById('gallery-title').value;
    const description = document.getElementById('gallery-description').value;
    try {
        await gallery.createGallery(title, description);
        alert('Gallery created successfully');
        e.target.reset();
        await gallery.loadGalleries();
    } catch (error) {
        handleError(error);
    }
}

function setupEditImageForm() {
    const editImageForm = document.getElementById('edit-image-form');
    if (editImageForm) {
        editImageForm.addEventListener('submit', handleImageEdit);
    }
}

async function handleImageEdit(e) {
    e.preventDefault();
    const id = document.getElementById('edit-image-id').value;
    const title = document.getElementById('edit-image-title').value;
    const description = document.getElementById('edit-image-description').value;
    try {
        await image.updateImage(id, title, description);
        alert('Image updated successfully');
        e.target.style.display = 'none';
        await image.loadImages();
    } catch (error) {
        handleError(error);
    }
}

function setupLogoutButton() {
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', auth.logout);
    }
}

// These functions need to be global to be called from inline event handlers
window.editGallery = gallery.editGallery;
window.deleteGallery = async (id) => {
    if (confirm('Are you sure you want to delete this gallery?')) {
        try {
            await gallery.deleteGallery(id);
            await gallery.loadGalleries();
        } catch (error) {
            handleError(error);
        }
    }
};

window.editImage = (id, title, description) => {
    const form = document.getElementById('edit-image-form');
    document.getElementById('edit-image-id').value = id;
    document.getElementById('edit-image-title').value = title;
    document.getElementById('edit-image-description').value = description;
    form.style.display = 'block';
};

window.deleteImage = async (id) => {
    if (confirm('Are you sure you want to delete this image?')) {
        try {
            await image.deleteImage(id);
            await image.loadImages();
        } catch (error) {
            handleError(error);
        }
    }
};

document.addEventListener('DOMContentLoaded', initializeAdmin);