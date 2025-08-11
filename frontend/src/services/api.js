import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response.data;
  },
  (error) => {
    console.error('API Response Error:', error);
    
    if (error.response) {
      // Server responded with error status
      throw new Error(error.response.data?.error || 'Server error occurred');
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('No response from server. Please check your connection.');
    } else {
      // Something else happened
      throw new Error('Request failed. Please try again.');
    }
  }
);

const apiService = {
  // User registration
  registerUser: async (name) => {
    return await api.post('/register-user', { name });
  },

  // Send chat message
  sendMessage: async (messageData) => {
    return await api.post('/chat', messageData);
  },

  // Get user data
  getUserData: async (userId) => {
    return await api.get(`/user/${userId}`);
  },

  // Get user summary
  getUserSummary: async (userId) => {
    return await api.get(`/user/${userId}/summary`);
  },

  // Health check
  healthCheck: async () => {
    return await api.get('/health');
  }
};

export default apiService;
