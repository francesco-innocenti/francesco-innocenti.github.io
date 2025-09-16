// AI Assistant Configuration
// This file contains the API configuration for the AI Assistant

const AI_ASSISTANT_CONFIG = {
    // API URL - Update this to your deployed backend URL
    // For local development: 'http://localhost:5001'
    // For production: 'https://your-backend-url.up.railway.app' (Railway)
    API_URL: 'http://localhost:5001',

    // Environment detection
    isProduction: window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1',

    // Auto-detect production URL if on GitHub Pages
    getApiUrl: function () {
        if (this.isProduction) {
            // Replace with your actual deployed backend URL
            // For Railway: 'https://your-backend-url.up.railway.app'
            return 'https://your-backend-service.up.railway.app';
        }
        return this.API_URL;
    }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AI_ASSISTANT_CONFIG;
}
