// Project: luchoh.com refactoring
// File: frontend/server.js

const express = require('express');
const nunjucks = require('nunjucks');
const fetch = require('node-fetch');
const path = require('path');
const { DateTime } = require('luxon');
const config = require('./config');

const app = express();
const port = 3333;

// Set up Nunjucks
const nunjucksEnv = nunjucks.configure(['src', 'src/_includes'], {
    autoescape: true,
    express: app,
    watch: true
});

nunjucksEnv.addFilter('dateYear', function () {
    return DateTime.now().toFormat('yyyy');
});

// Serve static files
app.use(express.static(path.join(__dirname, 'src')));
app.use('/css', express.static(path.join(__dirname, 'node_modules/materialize-css/dist/css')));
app.use('/js', express.static(path.join(__dirname, 'node_modules/materialize-css/dist/js')));

async function fetchTagsAndImages(tagName = config.defaultTag || "sticky") {
    console.log(`Fetching data for tag: ${tagName}`);
    console.log(`API Base URL: ${config.apiBaseUrl}`);
    
    try {
        // First fetch tags
        const tagsResponse = await fetch(`${config.apiBaseUrl}/tags/`).catch(error => {
            console.error('Error fetching tags:', error);
            throw new Error(`Failed to fetch tags: ${error.message}`);
        });

        if (!tagsResponse.ok) {
            const errorText = await tagsResponse.text();
            console.error('Tags response not OK:', tagsResponse.status, errorText);
            throw new Error(`Tags API error: ${tagsResponse.status} - ${errorText}`);
        }

        const tags = await tagsResponse.json();
        
        // Find the tag ID for the requested tag name
        const targetTag = tags.find(t => t.name === tagName);
        if (!targetTag) {
            console.log(`Tag "${tagName}" not found, fetching all images`);
            // If tag not found, fetch all images
            const imagesResponse = await fetch(`${config.apiBaseUrl}/images/`);
            if (!imagesResponse.ok) {
                const errorText = await imagesResponse.text();
                console.error('Images response not OK:', imagesResponse.status, errorText);
                throw new Error(`Images API error: ${imagesResponse.status} - ${errorText}`);
            }
            const images = await imagesResponse.json();
            return { tags, images };
        }

        // Fetch images for the specific tag
        const imagesResponse = await fetch(`${config.apiBaseUrl}/tags/${targetTag.id}/images`).catch(error => {
            console.error('Error fetching images:', error);
            throw new Error(`Failed to fetch images: ${error.message}`);
        });

        if (!imagesResponse.ok) {
            const errorText = await imagesResponse.text();
            console.error('Images response not OK:', imagesResponse.status, errorText);
            throw new Error(`Images API error: ${imagesResponse.status} - ${errorText}`);
        }

        const images = await imagesResponse.json();

        // Filter out the default tag from the menu
        const menuTags = tags.filter(tag => tag.name !== config.defaultTag);

        console.log('Successfully fetched data:', { 
            tagCount: menuTags.length, 
            imageCount: images.length,
            tagName,
            tagId: targetTag.id
        });
        
        return { tags: menuTags, images };
    } catch (error) {
        console.error('Error in fetchTagsAndImages:', error);
        throw error;
    }
}

app.get('/', async (req, res) => {
    try {
        console.log('Processing root route request');
        const { tags, images } = await fetchTagsAndImages();
        console.log(`Rendering index with ${tags.length} tags and ${images.length} images`);
        res.render('index.njk', {
            tags,
            images,
            apiBaseUrl: config.apiBaseUrl,
            user: {
                isAuthenticated: req.session && req.session.userId ? true : false
            },
            logoImage: '/images/luchoh-logo-invert.png',
            bannerImage: '/images/banner.jpg'
        });
    } catch (error) {
        console.error('Error processing root route:', error);
        res.status(500).render('error.njk', {
            error: {
                message: 'Error fetching data',
                details: process.env.NODE_ENV === 'development' ? error.message : undefined
            }
        });
    }
});

app.get('/tag/:tagName', async (req, res) => {
    try {
        console.log(`Processing tag route request for tag: ${req.params.tagName}`);
        const { tags, images } = await fetchTagsAndImages(req.params.tagName);
        res.render('index.njk', {
            tags,
            images,
            user: {
                isAuthenticated: req.session && req.session.userId ? true : false
            },
            logoImage: '/images/luchoh-logo-invert.png',
            bannerImage: '/images/banner.jpg'
        });
    } catch (error) {
        console.error('Error fetching tag data:', error);
        res.status(500).render('error.njk', {
            error: {
                message: 'Error fetching tag data',
                details: process.env.NODE_ENV === 'development' ? error.message : undefined
            }
        });
    }
});

app.get('/config', (req, res) => {
    res.json({
        apiBaseUrl: config.apiBaseUrl
    });
});

app.get('/health', async (req, res) => {
    try {
        const response = await fetch(`${config.apiBaseUrl}/`);
        if (response.ok) {
            res.json({ status: 'ok', api: 'connected' });
        } else {
            res.status(503).json({ 
                status: 'error', 
                message: 'API not responding correctly',
                statusCode: response.status
            });
        }
    } catch (error) {
        res.status(503).json({ 
            status: 'error', 
            message: 'Cannot connect to API',
            error: error.message
        });
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});