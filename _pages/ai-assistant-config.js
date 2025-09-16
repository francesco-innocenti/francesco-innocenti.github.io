// AI Assistant Configuration
// This file contains the API configuration for the AI Assistant

const AI_ASSISTANT_CONFIG = {
    // API URL - For local development
    API_URL: 'http://localhost:5001',

    // Environment detection
    isProduction: window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1',

    // Auto-detect production URL if on GitHub Pages
    getApiUrl: function () {
        if (this.isProduction) {
            // For production, you'll need to set up a public tunnel
            // Options: ngrok, cloudflare tunnel, or port forwarding
            return 'http://localhost:5001'; // Update this with your public URL
        }
        return this.API_URL;
    }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AI_ASSISTANT_CONFIG;
}
