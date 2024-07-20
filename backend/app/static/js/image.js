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

export async function updateImage(id, title, description) {
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
            imageElement.innerHTML = `
                <h3>${img.title}</h3>
                <p>${img.description}</p>
                <button onclick="editImage(${img.id}, '${img.title}', '${img.description}')">Edit</button>
                <button onclick="deleteImage(${img.id})">Delete</button>
            `;
            imagesList.appendChild(imageElement);
        });
        console.log('Images fetched successfully:', images);
    } catch (error) {
        handleError(error);
    }
}