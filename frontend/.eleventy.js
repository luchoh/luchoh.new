const { DateTime } = require("luxon");
const fetch = require('node-fetch');

const API_BASE_URL = 'http://localhost:8000';

module.exports = function (eleventyConfig) {

    eleventyConfig.setBrowserSyncConfig({
        server: {
            baseDir: 'dist',
            serveStaticOptions: {
                extensions: ['html', 'css']
            }
        },
        files: ['dist/**/*'],
        snippetOptions: {
            rule: {
                match: /<\/head>/i,
                fn: function (snippet, match) {
                    return snippet + match;
                }
            }
        }
    });

    // Correct the passthrough copy for CSS
    eleventyConfig.addPassthroughCopy("src/css");
    eleventyConfig.addPassthroughCopy("src/js");
    eleventyConfig.addPassthroughCopy("src/images");

    eleventyConfig.addPassthroughCopy({
        'node_modules/materialize-css/dist/css/materialize.min.css': 'css/materialize.min.css',
        'node_modules/materialize-css/dist/js/materialize.min.js': 'js/materialize.min.js'
    });

    eleventyConfig.on('eleventy.after', () => {
        console.log('CSS file should be at:', __dirname + '/dist/css/styles.css');
        const fs = require('fs');
        if (fs.existsSync(__dirname + '/dist/css/styles.css')) {
            console.log('CSS file exists');
        } else {
            console.log('CSS file does not exist');
        }
    });

    // Fetch galleries from the API
    eleventyConfig.addGlobalData("galleries", async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/galleries/`);
            return await response.json();
        } catch (error) {
            console.error("Failed to fetch galleries:", error);
            return []; // Return empty array in case of error
        }
    });

    // Fetch images from the API
    eleventyConfig.addGlobalData("images", async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/images/`);
            return await response.json();
        } catch (error) {
            console.error("Failed to fetch images:", error);
            return []; // Return empty array in case of error
        }
    });

    // Add a date filter
    eleventyConfig.addFilter("date", (dateObj, format) => {
        return DateTime.fromJSDate(dateObj).toFormat(format);
    });

    // Add a dateYear filter
    eleventyConfig.addFilter("dateYear", () => {
        return new Date().getFullYear();
    });

    // Set the logo image
    eleventyConfig.addGlobalData("logoImage", "/images/luchoh-logo-invert.png");
    // Set the banner image
    eleventyConfig.addGlobalData("bannerImage", "/images/banner.jpg");

    return {
        dir: {
            input: "src",
            output: "dist",
            includes: "_includes"
        },
        async: true,
        defer: true,
        templateFormats: ["njk", "md", "html"],
        markdownTemplateEngine: "njk",
        htmlTemplateEngine: "njk",
        dataTemplateEngine: "njk",
    };
};