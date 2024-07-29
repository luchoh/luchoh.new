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

document.addEventListener('DOMContentLoaded', async () => {
    await fetchConfig();
    setupTagNavigation();
    setupLightbox();
    setupMobileMenu();
});