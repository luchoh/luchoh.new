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

// Add a custom filter for debugging
nunjucksEnv.addFilter('debug', function (obj) {
    return JSON.stringify(obj, null, 2);
});

nunjucksEnv.addFilter('dateYear', function () {
    return DateTime.now().toFormat('yyyy');
});

// Serve static files
app.use(express.static(path.join(__dirname, 'src')));
app.use('/css', express.static(path.join(__dirname, 'node_modules/materialize-css/dist/css')));
app.use('/js', express.static(path.join(__dirname, 'node_modules/materialize-css/dist/js')));

// Define routes
app.get('/', async (req, res) => {
    try {
        const tagsResponse = await fetch(`${config.apiBaseUrl}/tags/`);
        const tags = await tagsResponse.json();

        const imagesResponse = await fetch(`${config.apiBaseUrl}/images/`);
        const images = await imagesResponse.json();

        console.log(tags);
        console.log(images);

        res.render('index.njk', {
            tags,
            images,
            user: {
                isAuthenticated: req.session && req.session.userId ? true : false // Adjust based on your auth system
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
        const tagName = req.params.tagName;
        const tagResponse = await fetch(`${config.apiBaseUrl}/tags/${tagName}`);
        const tag = await tagResponse.json();

        const imagesResponse = await fetch(`${config.apiBaseUrl}/tags/${tagName}/images`);
        const images = await imagesResponse.json();

        const tagsResponse = await fetch(`${config.apiBaseUrl}/tags/`);
        const tags = await tagsResponse.json();

        res.render('tag.njk', {
            tag,
            images,
            tags,
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

app.get('/image/:_id', async (req, res) => {
    try {
        const imageId = req.params._id;
        const imageResponse = await fetch(`${config.apiBaseUrl}/images/${imageId}`);
        const image = await imageResponse.json();

        const tagsResponse = await fetch(`${config.apiBaseUrl}/tags/`);
        const tags = await tagsResponse.json();

        res.render('image.njk', {
            image,
            tags,
            user: {
                isAuthenticated: req.session && req.session.userId ? true : false // Adjust based on your auth system
            },
            logoImage: '/images/luchoh-logo-invert.png',
            bannerImage: '/images/banner.jpg'
        });
    } catch (error) {
        console.error('Error fetching image data:', error);
        res.status(500).send('Error fetching image data');
    }
});

app.get('/image/:id-:slug', async (req, res) => {
    try {
        const response = await fetch(`${config.apiBaseUrl}/images/${req.params.id}-${req.params.slug}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Received image data:', data);
        res.render('image.njk', {
            image: data,
            user: {
                isAuthenticated: req.session && req.session.userId ? true : false
            },
            logoImage: '/images/luchoh-logo-invert.png',
            bannerImage: '/images/banner.jpg'
        });
    } catch (error) {
        console.error('Error fetching image:', error);
        res.status(500).send('Error fetching image');
    }
});

app.get('/admin', (req, res) => {
    res.render('admin.html');
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});