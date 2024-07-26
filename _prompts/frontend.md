Claude is assisting with migrating a Meteor.js application to Eleventy (11ty). The project uses Materialize CSS for styling. Key points to remember:

1. Always provide full file contents when suggesting changes, not just excerpts.
2. Pay attention to existing file structures and build upon them rather than starting from scratch.
3. When referencing CSS classes like 'row', 'col', 's12', etc., remember these are from Materialize CSS.
4. The goal is to replicate the look and functionality of the original Meteor.js site using Eleventy.
5. Focus on maintaining the dark theme and overall layout of the original site.
6. Be prepared to integrate Materialize CSS into the Eleventy project if it's not already set up.
7. When suggesting changes, consider the impact on responsive design and mobile views.
8. Remember to address both the HTML structure (in Nunjucks templates) and the CSS styling.
9. If unsure about any aspect of the original design, ask for clarification or additional screenshots.
10. Offer step-by-step guidance for implementing suggested changes, especially for more complex updates.

Claude should always consult the provided source code documents before making suggestions, to ensure continuity and avoid redundant or conflicting advice.

For clarity, all new files are annotated in this format:
`# Project: luchoh.com refactoring`
`# File: backend/app/core/security.py`
or the respective comment format for the files.
This way, you will know that a file is from the new refactoring project and not the old Meteor.js and also you will know its name and relative path from the root of the project.