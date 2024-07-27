// Project: luchoh.com refactoring
// File: backend/app/static/js/image.js

import { getToken } from './auth.js';
import { handleError } from './utils.js';

export async function uploadImage(file, title, description) {
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
            'Authorization': `Bearer ${token}`
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

export async function updateImage(id, formData) {
    const token = getToken();

    // Convert FormData to a plain object
    const updateData = {};
    for (let [key, value] of formData.entries()) {
        if (key === 'tags') {
            updateData[key] = value.split(',').map(tag => tag.trim());
        } else if (key === 'sticky') {
            updateData[key] = value === 'on';
        } else {
            updateData[key] = value;
        }
    }

    // Remove id from updateData as it's in the URL
    delete updateData.id;

    const response = await fetch(`/api/v1/images/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(updateData)
    });

    if (response.status === 401) {
        throw new Error('Unauthorized');
    }

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`Failed to update image: ${JSON.stringify(errorData)}`);
    }

    return await response.json();
}


export async function deleteImage(id) {
    const response = await fetch(`/api/v1/images/${id}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${getToken()}`
        }
    });

    if (response.status === 401) {
        throw new Error('Unauthorized');
    }

    if (!response.ok) {
        throw new Error('Failed to delete image');
    }
}

export async function loadImages() {
    console.log('Starting to load images');
    try {
        const token = getToken();
        console.log('Token used for images request:', token);
        const response = await fetch('/api/v1/images/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.status === 401) {
            throw new Error('Unauthorized');
        }

        if (!response.ok) {
            throw new Error('Failed to load images');
        }

        const images = await response.json();
        const imagesList = document.getElementById('images-list');
        imagesList.innerHTML = '';

        images.forEach(img => {
            const imageElement = document.createElement('div');
            imageElement.className = 'image-item';
            imageElement.dataset.id = img.id;
            imageElement.dataset.title = img.title;
            imageElement.dataset.description = img.description;
            imageElement.dataset.filePath = img.file_path;
            imageElement.dataset.slug = img.slug;
            imageElement.dataset.tags = JSON.stringify(img.tags);
            imageElement.dataset.sticky = img.sticky;

            imageElement.innerHTML = `
                <h3>${escapeHtml(img.title)}</h3>
                <p>${escapeHtml(img.description)}</p>
                <img src="${escapeHtml(img.file_path)}" alt="${escapeHtml(img.title)}" style="max-width: 200px;">
                <img class="thumbnail" src="${escapeHtml(img.thumbnail_url || img.file_path)}" alt="Thumbnail" style="max-width: 100px;">
                <button class="edit-image">Edit</button>
                <button class="delete-image">Delete</button>
            `;
            imagesList.appendChild(imageElement);
        });
        console.log('Images fetched successfully:', images);
    } catch (error) {
        console.error('Error in loadImages:', error);
        handleError(error);
    }
}

export async function createThumbnail(imageId, cropData) {
    const response = await fetch(`/api/v1/images/${imageId}/thumbnail`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getToken()}`
        },
        body: JSON.stringify(cropData)
    });

    if (response.status === 401) {
        throw new Error('Unauthorized');
    }

    if (!response.ok) {
        throw new Error('Failed to create thumbnail');
    }

    return await response.json();
}

// Helper function to escape HTML special characters
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Helper function to escape JavaScript string content
function escapeJS(unsafe) {
    return unsafe
        .replace(/\\/g, "\\\\")
        .replace(/'/g, "\\'")
        .replace(/"/g, '\\"')
        .replace(/\n/g, "\\n")
        .replace(/\r/g, "\\r")
        .replace(/\t/g, "\\t");
}