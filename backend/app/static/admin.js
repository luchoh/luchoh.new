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
                loadGalleries();
                loadImages();
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
                await createImage(file, name, title, description);
                alert('Image uploaded successfully');
                // Clear the form
                uploadForm.reset();
            } catch (error) {
                handleError(error);
            }
        });
    }

    // Gallery form handler
    const galleryForm = document.getElementById('gallery-form');
    if (galleryForm) {
        galleryForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const title = document.getElementById('gallery-title').value;
            const description = document.getElementById('gallery-description').value;
            try {
                await createGallery(title, description);
                alert('Gallery created successfully');
                galleryForm.reset();
                loadGalleries();
            } catch (error) {
                handleError(error);
            }
        });
    }

    // Edit image form handler
    const editImageForm = document.getElementById('edit-image-form');
    if (editImageForm) {
        editImageForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const id = document.getElementById('edit-image-id').value;
            const title = document.getElementById('edit-image-title').value;
            const description = document.getElementById('edit-image-description').value;
            try {
                await updateImage(id, title, description);
                alert('Image updated successfully');
                editImageForm.style.display = 'none';
            } catch (error) {
                handleError(error);
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
    console.log('Token set:', token);
}

function getToken() {
    return localStorage.getItem('token');
}

function removeToken() {
    localStorage.removeItem('token');
}

function isLoggedIn() {
    return !!getToken();
}

function logout() {
    removeToken();
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('adminContent').style.display = 'none';
}

async function checkLoginStatus() {
    if (isLoggedIn()) {
        document.getElementById('loginForm').style.display = 'none';
        document.getElementById('adminContent').style.display = 'block';
        loadGalleries();
        loadImages();
    } else {
        document.getElementById('loginForm').style.display = 'block';
        document.getElementById('adminContent').style.display = 'none';
    }
}

async function uploadImage(file, name, title, description) {
    const formData = new FormData();
    formData.append('file', file);

    const uploadResponse = await fetch('/api/v1/upload/uploadfile/', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${getToken()}`
        },
        body: formData,
    });

    if (uploadResponse.status === 401) {
        throw new Error('Unauthorized');
    }

    if (!uploadResponse.ok) {
        throw new Error('Failed to upload image file');
    }

    const uploadResult = await uploadResponse.json();
    console.log('Upload result:', uploadResult);  // Debug log

    if (!uploadResult.file_path) {
        console.error('Upload result does not contain file_path');
        throw new Error('Upload result does not contain file_path');
    }

    // Now create the image record
    return createImage(uploadResult.file_path, title, description);
}



async function createGallery(title, description) {
    const response = await fetch('/api/v1/galleries/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getToken()}`
        },
        body: JSON.stringify({ title, description })
    });

    if (response.status === 401) {
        throw new Error('Unauthorized');
    }

    if (!response.ok) {
        throw new Error('Failed to create gallery');
    }

    return await response.json();
}

async function createImage(file, title, description) {
    const token = getToken();

    // First, upload the file
    const formData = new FormData();
    formData.append('file', file);

    const uploadResponse = await fetch('/api/v1/upload/uploadfile/', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: formData
    });

    if (!uploadResponse.ok) {
        const errorData = await uploadResponse.json();
        throw new Error(`Failed to upload file: ${JSON.stringify(errorData)}`);
    }

    const uploadResult = await uploadResponse.json();
    console.log('Upload result:', uploadResult);  // Debug log

    // Now create the image record
    const imageData = {
        file_path: uploadResult.file_path,
        title: title,
        description: description
    };

    const createResponse = await fetch('/api/v1/images/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getToken()}`
        },
        body: JSON.stringify(imageData)
    });

    if (!createResponse.ok) {
        const errorData = await createResponse.json();
        throw new Error(`Failed to create image record: ${JSON.stringify(errorData)}`);
    }

    const responseData = await createResponse.json();
    console.log('Response data:', responseData);  // Debug log
    return responseData;
}

async function loadGalleries() {
    if (!isLoggedIn()) return;
    console.log('Current token:', getToken());

    const response = await fetch('/api/v1/galleries/', {
        headers: {
            'Authorization': `Bearer ${getToken()}`
        }
    });

    if (response.status === 401) {
        logout();
        return;
    }

    if (!response.ok) {
        throw new Error('Failed to load galleries');
    }

    const galleries = await response.json();
    const galleriesList = document.getElementById('galleries-list');
    galleriesList.innerHTML = '';

    galleries.forEach(gallery => {
        const galleryElement = document.createElement('div');
        galleryElement.innerHTML = `
            <h3>${gallery.title}</h3>
            <p>${gallery.description}</p>
            <button onclick="editGallery(${gallery.id})">Edit</button>
            <button onclick="deleteGallery(${gallery.id})">Delete</button>
        `;
        galleriesList.appendChild(galleryElement);
    });
}

async function loadImages() {
    if (!isLoggedIn()) return;
    console.log('Current token:', getToken());

    const response = await fetch('/api/v1/images/', {
        headers: {
            'Authorization': `Bearer ${getToken()}`
        }
    });

    if (response.status === 401) {
        logout();
        return;
    }

    if (!response.ok) {
        throw new Error('Failed to load galleries');
    }

    const images = await response.json();
    const imagesList = document.getElementById('images-list');
    imagesList.innerHTML = '';

    images.forEach(image => {
        const imageElement = document.createElement('div');
        imageElement.innerHTML = `
            <h3>${image.title}</h3>
            <p>${image.description}</p>
            <button onclick="editImage(${image.id})">Edit</button>
            <button onclick="deleteImage(${image.id})">Delete</button>
        `;
        imagesList.appendChild(imageElement);
    });
}

async function updateImage(id, title, description) {
    const response = await fetch(`/api/v1/images/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getToken()}`
        },
        body: JSON.stringify({ title, description })
    });

    if (response.status === 401) {
        throw new Error('Unauthorized');
    }

    if (!response.ok) {
        throw new Error('Failed to update image');
    }

    loadImages();  // Reload images after update
    return await response.json();
}

function editImage(id, title, description) {
    const form = document.getElementById('edit-image-form');
    document.getElementById('edit-image-id').value = id;
    document.getElementById('edit-image-title').value = title;
    document.getElementById('edit-image-description').value = description;
    form.style.display = 'block';
}

async function deleteGallery(id) {
    if (!confirm('Are you sure you want to delete this gallery?')) return;

    const response = await fetch(`/api/v1/galleries/${id}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${getToken()}`
        }
    });

    if (response.status === 401) {
        logout();
        return;
    }

    if (!response.ok) {
        throw new Error('Failed to delete gallery');
    }

    loadGalleries();
}

async function deleteImage(id) {
    if (!confirm('Are you sure you want to delete this image?')) return;

    const response = await fetch(`/api/v1/images/${id}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${getToken()}`
        }
    });

    if (response.status === 401) {
        logout();
        return;
    }

    if (!response.ok) {
        throw new Error('Failed to delete image');
    }

    loadImages();
}

function handleError(error) {
    if (error.message === 'Unauthorized') {
        alert('Your session has expired. Please log in again.');
        logout();
    } else {
        alert(error.message);
    }
}

// Note: editGallery function is not implemented yet
function editGallery(id) {
    alert('Edit gallery functionality not implemented yet.');
    // Implement the edit gallery functionality here
}