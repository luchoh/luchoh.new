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

async function fetchTagsAndImages(tagName = null) {
    const tagsResponse = await fetch(`${config.apiBaseUrl}/tags/`);
    const tags = await tagsResponse.json();

    const imagesUrl = tagName
        ? `${config.apiBaseUrl}/images/by_tag/${tagName}`
        : `${config.apiBaseUrl}/images/`;
    const imagesResponse = await fetch(imagesUrl);
    const images = await imagesResponse.json();

    return { tags, images };
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