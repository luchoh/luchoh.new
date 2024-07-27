// Project: luchoh.com refactoring
// File: frontend/src/js/tag.js

import { getToken } from './auth.js';
import { handleError } from './utils.js';

export async function createTag(name, description) {
    const response = await fetch('/api/v1/tags/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getToken()}`
        },
        body: JSON.stringify({ name, description })
    });

    if (response.status === 401) {
        throw new Error('Unauthorized');
    }

    if (!response.ok) {
        throw new Error('Failed to create tag');
    }

    return await response.json();
}

export async function deleteTag(id) {
    const response = await fetch(`/api/v1/tags/${id}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${getToken()}`
        }
    });

    if (response.status === 401) {
        throw new Error('Unauthorized');
    }

    if (!response.ok) {
        throw new Error('Failed to delete tag');
    }
}

export function showEditTagSection(id, name, description) {
    const imageSection = document.getElementById('imageSection');
    const tagSection = document.getElementById('tagSection');
    const editImageSection = document.getElementById('editImageSection');
    const editTagSection = document.getElementById('editTagSection');

    if (imageSection) imageSection.style.display = 'none';
    if (tagSection) tagSection.style.display = 'none';
    if (editImageSection) editImageSection.style.display = 'none';
    if (editTagSection) editTagSection.style.display = 'block';

    const editTagId = document.getElementById('edit-tag-id');
    const editTagName = document.getElementById('edit-tag-name');
    const editTagDescription = document.getElementById('edit-tag-description');

    if (editTagId) editTagId.value = id;
    if (editTagName) editTagName.value = name;
    if (editTagDescription) editTagDescription.value = description;
}

export async function updateTag(id, name, description) {
    const response = await fetch(`/api/v1/tags/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getToken()}`
        },
        body: JSON.stringify({ name, description })
    });

    if (response.status === 401) {
        throw new Error('Unauthorized');
    }

    if (!response.ok) {
        throw new Error('Failed to update tag');
    }

    return await response.json();
}

export async function loadTags() {
    console.log('Starting to load tags');
    try {
        const token = getToken();
        console.log('Token used for tags request:', token);
        const response = await fetch('/api/v1/tags/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.status === 401) {
            throw new Error('Unauthorized');
        }

        if (!response.ok) {
            throw new Error('Failed to load tags');
        }

        const tags = await response.json();
        const tagsList = document.getElementById('tags-list');
        if (!tagsList) {
            console.error('Element with id "tags-list" not found');
            return;
        }
        tagsList.innerHTML = '';

        tags.forEach(tag => {
            const tagElement = document.createElement('div');
            tagElement.innerHTML = `
                <h3>${tag.name}</h3>
                <p>${tag.description}</p>
                <button onclick="editTag(${tag.id}, '${tag.name}', '${tag.description}')">Edit</button>
                <button onclick="deleteTag(${tag.id})">Delete</button>
            `;
            tagsList.appendChild(tagElement);
        });
        console.log('Tags fetched successfully:', tags);
    } catch (error) {
        console.error('Error in loadTags:', error);
        handleError(error);
    }
}