const { DateTime } = require("luxon");

module.exports = function (eleventyConfig) {
    eleventyConfig.addPassthroughCopy("src/css");
    eleventyConfig.addPassthroughCopy("src/js");
    eleventyConfig.addPassthroughCopy("src/images");

    // Add a date filter
    eleventyConfig.addFilter("date", (dateObj, format) => {
        return DateTime.fromJSDate(dateObj).toFormat(format);
    });

    eleventyConfig.addFilter("dateYear", function () {
        return new Date().getFullYear();
    });

    eleventyConfig.addGlobalData("bannerImage", "/images/luchoh-logo-invert.png");

    return {
        dir: {
            input: "src",
            output: "dist",
            includes: "_includes"
        },
        // This will create pages for galleries and images dynamically
        // You'll need to update these functions to fetch real data from your API
        async: true,
        defer: true,
        eleventyComputed: {
            galleries: async () => {
                // Fetch galleries from your API
                return [
                    { slug: 'nature', title: 'Nature', description: 'Beautiful nature photos' },
                    { slug: 'cities', title: 'Cities', description: 'Urban landscapes' }
                ];
            },
            images: async () => {
                // Fetch images from your API
                return [
                    { slug: 'sunset', title: 'Sunset', url: '/images/sunset.jpg', description: 'A beautiful sunset' },
                    { slug: 'mountains', title: 'Mountains', url: '/images/mountains.jpg', description: 'Majestic mountains' }
                ];
            }
        },
        templateFormats: ["njk", "md", "html"],
        markdownTemplateEngine: "njk",
        htmlTemplateEngine: "njk",
        dataTemplateEngine: "njk",
    };
};