// Project: luchoh.com refactoring
// File: frontend/config.js

const dotenv = require('dotenv');
dotenv.config();

module.exports = {
    apiBaseUrl: process.env.API_BASE_URL || 'http://localhost:8000/api/v1',
};