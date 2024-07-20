// Project: luchoh.com refactoring
// File: backend/app/static/js/utils.js

import { logout } from './auth.js';

export function handleError(error) {
    if (error.message === 'Unauthorized') {
        alert('Your session has expired. Please log in again.');
        logout();
    } else {
        alert(error.message);
    }
}