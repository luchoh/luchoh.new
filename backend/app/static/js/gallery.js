// Project: luchoh.com refactoring
// File: backend/app/static/js/gallery.js

import { getToken } from './auth.js';
import { handleError } from './utils.js';

export async function createGallery(title, description) {
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

export async function deleteGallery(id) {
    const response = await fetch(`/api/v1/galleries/${id}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${getToken()}`
        }
    });

    if (response.status === 401) {
        throw new Error('Unauthorized');
    }

    if (!response.ok) {
        throw new Error('Failed to delete gallery');
    }
}

export function editGallery(id) {
    alert('Edit gallery functionality not implemented yet.');
    // Implement the edit gallery functionality here
}

export async function loadGalleries() {
    console.log('Starting to load images');
    try {
        const token = getToken();
        console.log('Token used for galleries request:', token);  // Add this line for debugging
        const response = await fetch('/api/v1/galleries/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.status === 401) {
            throw new Error('Unauthorized');
        }

        if (!response.ok) {
            throw new Error('Failed to load galleries');
        }

        const galleries = await response.json();
        const galleriesList = document.getElementById('galleries-list');
        galleriesList.innerHTML = '';

        galleries.forEach(g => {
            const galleryElement = document.createElement('div');
            galleryElement.innerHTML = `
                <h3>${g.title}</h3>
                <p>${g.description}</p>
                <button onclick="editGallery(${g.id})">Edit</button>
                <button onclick="deleteGallery(${g.id})">Delete</button>
            `;
            galleriesList.appendChild(galleryElement);
        });
        console.log('Galleries fetched successfully:', galleries);
    } catch (error) {
        handleError(error);
    }
}