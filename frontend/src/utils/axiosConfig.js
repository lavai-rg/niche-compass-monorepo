import axios from 'axios';

// Create axios instance
const api = axios.create({
    baseURL: 'http://localhost:5000',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor - automatically add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('authToken');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor - handle auth errors
api.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.response?.status === 401) {
            // Token expired or invalid
            localStorage.removeItem('authToken');
            localStorage.removeItem('userData');
            window.location.href = '/';
        }
        return Promise.reject(error);
    }
);

// Helper functions for API calls
export const apiClient = {
    // Authentication
    login: (credentials) => api.post('/api/auth/login', credentials),
    register: (userData) => api.post('/api/auth/register', userData),
    logout: () => api.post('/api/auth/logout'),
    getProfile: () => api.get('/api/auth/me'),
    
    // Keywords
    searchKeywords: (query) => api.get(`/api/keywords/search?q=${encodeURIComponent(query)}`),
    analyzeKeyword: (keyword) => api.post('/api/keywords/analyze', { keyword }),
    
    // Niches
    getNiches: () => api.get('/api/niches'),
    analyzeNiche: (niche) => api.post('/api/niches/analyze', { niche }),
    
    // Products
    getProducts: () => api.get('/api/products'),
    analyzeProduct: (productUrl) => api.post('/api/products/analyze', { product_url: productUrl }),
    
    // AI Services
    analyzeImage: (imageData) => api.post('/api/ai/vision/analyze', imageData),
    analyzeText: (textData) => api.post('/api/ai/text/analyze', textData),
    getAIMonitoring: () => api.get('/api/ai/monitoring/health'),
    
    // Health checks
    health: () => api.get('/api/health'),
    authHealth: () => api.get('/api/auth/health'),
    aiHealth: () => api.get('/api/ai/health'),
};

export default api;
