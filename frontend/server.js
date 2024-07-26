// Project: luchoh.com refactoring
// File: frontend/server.js

const express = require('express');
const nunjucks = require('nunjucks');
const fetch = require('node-fetch');
const path = require('path');
const { DateTime } = require('luxon');


const app = express();
const port = 3333;

// Set up Nunjucks
const nunjucksEnv = nunjucks.configure(['src', 'src/_includes'], {
    autoescape: true,
    express: app,
    watch: true
});

// Add a custom filter for debugging
nunjucksEnv.addFilter('debug', function(obj) {
    return JSON.stringify(obj, null, 2);
});

nunjucksEnv.addFilter('dateYear', function() {
    return DateTime.now().toFormat('yyyy');
});

// Serve static files
app.use(express.static(path.join(__dirname, 'src')));
app.use('/css', express.static(path.join(__dirname, 'node_modules/materialize-css/dist/css')));
app.use('/js', express.static(path.join(__dirname, 'node_modules/materialize-css/dist/js')));

// Define routes
app.get('/', async (req, res) => {
    try {
        const galleriesResponse = await fetch('http://localhost:8000/api/v1/galleries/');
        const galleries = await galleriesResponse.json();

        const imagesResponse = await fetch('http://localhost:8000/api/v1/images/');
        const images = await imagesResponse.json();

        console.log(galleries);
        console.log(images);

        res.render('index.njk', { 
            galleries, 
            images,
            logoImage: '/images/luchoh-logo-invert.png',
            bannerImage: '/images/banner.jpg'
        });
    } catch (error) {
        console.error('Error fetching data:', error);
        res.status(500).send('Error fetching data');
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});