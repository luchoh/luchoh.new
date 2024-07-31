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
    try {
        const [tagsResponse, imagesResponse] = await Promise.all([
            fetch(`${config.apiBaseUrl}/tags/`),
            fetch(`${config.apiBaseUrl}/images/by_tag/${tagName}`)
        ]);

        if (!tagsResponse.ok || !imagesResponse.ok) {
            throw new Error('Failed to fetch data');
        }

        const tags = await tagsResponse.json();
        const images = await imagesResponse.json();

        // Filter out the 'sticky' tag from the menu
        const menuTags = tags.filter(tag => tag.name !== config.defaultTag);

        return { tags: menuTags, images };
    } catch (error) {
        console.error('Error fetching tags and images:', error);
        throw error;
    }
}

app.get('/', async (req, res) => {
    try {
        const { tags, images } = await fetchTagsAndImages();
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
        console.error('Error fetching data:', error);
        res.status(500).send('Error fetching data');
    }
});

app.get('/tag/:tagName', async (req, res) => {
    try {
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
        res.status(500).send('Error fetching tag data');
    }
});

app.get('/config', (req, res) => {
    res.json({
        apiBaseUrl: config.apiBaseUrl
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});