/*Project: luchoh.com refactoring
File: backend/app/static/admin.js*/
// admin.js

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const uploadForm = document.getElementById('upload-form');
    const loginFormDiv = document.getElementById('loginForm');
    const adminContentDiv = document.getElementById('adminContent');
    const galleryList = document.getElementById('gallery-list');

    // Login form submission
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('/api/v1/auth/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.access_token);
                loginFormDiv.style.display = 'none';
                adminContentDiv.style.display = 'block';
                fetchGalleries();
            } else {
                alert('Login failed. Please try again.');
            }
        } catch (error) {
            console.error('Login error:', error);
            alert('An error occurred. Please try again.');
        }
    });

    // Image upload form submission
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(uploadForm);

        try {
            const response = await fetch('/api/v1/upload/uploadfile/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                },
                body: formData,
            });

            if (response.ok) {
                alert('Image uploaded successfully!');
                uploadForm.reset();
            } else {
                alert('Upload failed. Please try again.');
            }
        } catch (error) {
            console.error('Upload error:', error);
            alert('An error occurred. Please try again.');
        }
    });

    // Fetch and display galleries
    async function fetchGalleries() {
        try {
            const response = await fetch('/api/v1/galleries/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                },
            });

            if (response.ok) {
                const galleries = await response.json();
                galleryList.innerHTML = galleries.map(gallery =>
                    `<li>${gallery.title}</li>`
                ).join('');

                // Populate gallery dropdown in upload form
                const gallerySelect = document.getElementById('gallery');
                gallerySelect.innerHTML = galleries.map(gallery =>
                    `<option value="${gallery.id}">${gallery.title}</option>`
                ).join('');
            } else {
                console.error('Failed to fetch galleries');
            }
        } catch (error) {
            console.error('Error fetching galleries:', error);
        }
    }
});