// Determine if we're in development or production
const isDevelopment = window.location.hostname === 'localhost' || 
                      window.location.hostname === '127.0.0.1';

// Set the base URL based on the environment
export const API_BASE_URL = isDevelopment 
  ? 'http://localhost:8000' 
  : 'https://bcit-anthony-sh-s.com/lumisenseai/api/v1';

// Function to get the full API URL for a given endpoint
export const getApiUrl = (endpoint: string): string => {
  return `${API_BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;
};
