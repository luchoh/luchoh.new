/*Project: luchoh.com refactoring
File: frontend/src/js/main.js*/

async function fetchGalleries() {
    try {
        const response = await fetch('/api/v1/galleries/');
        const galleries = await response.json();
        const galleryList = document.getElementById('gallery-list');
        galleries.forEach(gallery => {
            const li = document.createElement('li');
            li.innerHTML = `<a href="/gallery/${gallery.slug}/">${gallery.title}</a>`;
            galleryList.appendChild(li);
        });
    } catch (error) {
        console.error('Error fetching galleries:', error);
    }
}

async function fetchImages(gallerySlug) {
    try {
        const response = await fetch(`/api/v1/galleries/${gallerySlug}/images`);
        const images = await response.json();
        const imageList = document.getElementById('image-list');
        images.forEach(image => {
            const div = document.createElement('div');
            div.innerHTML = `
                <a href="/image/${image.slug}/">
                    <img src="${image.thumbnail}" alt="${image.title}">
                    <p>${image.title}</p>
                </a>
            `;
            imageList.appendChild(div);
        });
    } catch (error) {
        console.error('Error fetching images:', error);
    }
}

// Call these functions when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const galleryList = document.getElementById('gallery-list');
    const imageList = document.getElementById('image-list');

    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems);

    if (galleryList) {
        fetchGalleries();
    }

    if (imageList) {
        const gallerySlug = imageList.dataset.gallerySlug;
        fetchImages(gallerySlug);
    }

    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.button-collapse');
    const mobileMenu = document.querySelector('#mobile-menu');

    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('active');
        });
    }

    // Initialize Lightbox
    if (typeof lightbox !== 'undefined') {
        lightbox.option({
            'resizeDuration': 200,
            'wrapAround': true,
            'albumLabel': "Image %1 of %2",
            'fadeDuration': 300
        });
    }
});

window.addEventListener('load', function () {
    if (typeof lightbox !== 'undefined') {
        lightbox.init();
    }
});