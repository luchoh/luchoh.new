// Project: luchoh.com refactoring
// File: backend/app/static/js/admin.js

import * as auth from './auth.js';
import * as tag from './tag.js';
import * as image from './image.js';
import { handleError } from './utils.js';

let cropper;

async function initializeAdmin() {
    console.log('Initializing admin page');
    setupLoginForm();
    setupNavigation();
    setupUploadForm();
    setupTagForm();
    setupEditImageForm();
    setupEditTagForm();
    setupLogoutButton();
    setupImageListListeners();
    setupTagCreation();

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
        await tag.loadTags();
        await image.loadImages();
    } catch (error) {
        console.error('Error loading admin data:', error);
        handleError(error);
    }
}

function setupLoginForm() {
    const loginForm = document.getElementById('login-form');
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

function setupNavigation() {
    const navImages = document.getElementById('nav-images');
    const navTags = document.getElementById('nav-tags');

    if (navImages) {
        navImages.addEventListener('click', showImageSection);
    }
    if (navTags) {
        navTags.addEventListener('click', showTagSection);
    }
}

function showImageSection() {
    document.getElementById('imageSection').style.display = 'block';
    document.getElementById('tagSection').style.display = 'none';
    document.getElementById('editImageSection').style.display = 'none';
    document.getElementById('editTagSection').style.display = 'none';
    image.loadImages();
}

function showTagSection() {
    document.getElementById('imageSection').style.display = 'none';
    document.getElementById('tagSection').style.display = 'block';
    document.getElementById('editImageSection').style.display = 'none';
    document.getElementById('editTagSection').style.display = 'none';
    tag.loadTags();
}

function setupUploadForm() {
    const uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', handleImageUpload);
    }
}

async function handleImageUpload(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    try {
        await image.uploadImage(formData);
        alert('Image uploaded successfully');
        e.target.reset();
        await image.loadImages();
    } catch (error) {
        handleError(error);
    }
}

function setupTagForm() {
    const tagForm = document.getElementById('tag-form');
    if (tagForm) {
        tagForm.addEventListener('submit', handleTagCreation);
    }
}

async function handleTagCreation(e) {
    e.preventDefault();
    const name = document.getElementById('tag-name').value;
    const description = document.getElementById('tag-description').value;
    try {
        await tag.createTag(name, description);
        alert('Tag created successfully');
        e.target.reset();
        await tag.loadTags();
    } catch (error) {
        handleError(error);
    }
}

function setupEditImageForm() {
    const editImageForm = document.getElementById('edit-image-form');
    if (editImageForm) {
        editImageForm.addEventListener('submit', handleImageEdit);
    }
    const applyCropButton = document.getElementById('apply-crop');
    if (applyCropButton) {
        applyCropButton.addEventListener('click', handleApplyCrop);
    }
}

function setupEditTagForm() {
    const editTagForm = document.getElementById('edit-tag-form');
    if (editTagForm) {
        editTagForm.addEventListener('submit', handleTagEdit);
    }
}

function setupImageListListeners() {
    const imagesList = document.getElementById('images-list');
    imagesList.addEventListener('click', function (e) {
        if (e.target.classList.contains('edit-image')) {
            const imageItem = e.target.closest('.image-item');
            const id = imageItem.dataset.id;
            const title = imageItem.dataset.title;
            const description = imageItem.dataset.description;
            const filePath = imageItem.dataset.filePath;
            const slug = imageItem.dataset.slug;
            const tags = JSON.parse(imageItem.dataset.tags);
            const sticky = imageItem.dataset.sticky === 'true';
            showEditImageSection(id, title, description, filePath, slug, tags, sticky);
        } else if (e.target.classList.contains('delete-image')) {
            const imageItem = e.target.closest('.image-item');
            const id = imageItem.dataset.id;
            deleteImage(id);
        }
    });
}

async function handleImageEdit(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const id = document.getElementById('edit-image-id').value;

    // Get selected tags
    const selectedTags = Array.from(document.getElementById('edit-image-tags').selectedOptions).map(option => option.value);

    // Create a JSON object to send
    const updateData = {
        title: encodeURIComponent(formData.get('title')),
        description: encodeURIComponent(formData.get('description')),
        slug: encodeURIComponent(formData.get('slug')),
        sticky: formData.get('sticky') === 'on',
        tags: selectedTags
    };

    try {
        await image.updateImage(id, updateData);
        alert('Image updated successfully');
        document.getElementById('editImageSection').style.display = 'none';
        await image.loadImages();
    } catch (error) {
        handleError(error);
    }
}

async function handleTagEdit(e) {
    e.preventDefault();
    const id = document.getElementById('edit-tag-id').value;
    const name = document.getElementById('edit-tag-name').value;
    const description = document.getElementById('edit-tag-description').value;
    try {
        await tag.updateTag(id, name, description);
        alert('Tag updated successfully');
        document.getElementById('editTagSection').style.display = 'none';
        await tag.loadTags();
    } catch (error) {
        handleError(error);
    }
}

async function handleApplyCrop() {
    const imageId = document.getElementById('edit-image-id').value;
    const cropData = cropper.getData();
    try {
        await image.createThumbnail(imageId, cropData);
        alert('Thumbnail created/updated successfully');
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

function setupTagCreation() {
    const addNewTagBtn = document.getElementById('add-new-tag-btn');
    const newTagInput = document.getElementById('new-tag-input');
    const tagSelect = document.getElementById('edit-image-tags');

    if (addNewTagBtn && newTagInput && tagSelect) {
        addNewTagBtn.addEventListener('click', async () => {
            const tagName = newTagInput.value.trim();
            if (tagName) {
                try {
                    const newTag = await tag.createTag(tagName, "");  // Using createTag instead of createTagIfNotExists
                    const option = document.createElement('option');
                    option.value = newTag.id;
                    option.textContent = newTag.name;
                    tagSelect.appendChild(option);
                    option.selected = true;
                    newTagInput.value = '';
                } catch (error) {
                    handleError(error);
                }
            }
        });
    }
}

export function showEditImageSection(id, title, description, imageSrc, slug, tags, sticky) {
    document.getElementById('imageSection').style.display = 'none';
    document.getElementById('tagSection').style.display = 'none';
    document.getElementById('editImageSection').style.display = 'block';
    document.getElementById('editTagSection').style.display = 'none';

    document.getElementById('edit-image-id').value = id;
    document.getElementById('edit-image-title').value = title;
    document.getElementById('edit-image-description').value = description;
    document.getElementById('edit-image-slug').value = slug;
    document.getElementById('edit-image-sticky').checked = sticky;
    document.getElementById('image-to-crop').src = imageSrc;

    const tagSelect = document.getElementById('edit-image-tags');
    tagSelect.innerHTML = '';

    console.log('Image tags:', tags);  // Add this line

    tag.loadTags().then((allTags) => {
        console.log('All tags:', allTags);  // Add this line
        allTags.forEach(tagOption => {
            const option = document.createElement('option');
            option.value = tagOption.id;
            option.textContent = tagOption.name;
            option.selected = tags.some(t => t.id === tagOption.id);
            tagSelect.appendChild(option);
            console.log('Created option:', option);  // Add this line
        });
    });

    if (cropper) {
        cropper.destroy();
    }
    cropper = new Cropper(document.getElementById('image-to-crop'), {
        aspectRatio: 1,
        viewMode: 1,
    });
}

export function deleteImage(id) {
    return image.deleteImage(id);
}

export function deleteTag(id) {
    return tag.deleteTag(id);
}

document.addEventListener('DOMContentLoaded', () => {
    initializeAdmin().catch(error => {
        console.error('Error during admin initialization:', error);
        handleError(error);
    });
});