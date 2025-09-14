import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_URL || "https://atlan-helpdesk-api.onrender.com" || "http://localhost:8000";

// Log API URL for debugging
console.log('API Base URL:', API_BASE_URL);

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 30000, // 30 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API Response Error:', {
      url: error.config?.url,
      status: error.response?.status,
      message: error.message,
      data: error.response?.data
    });
    return Promise.reject(error);
  }
);

export const fetchTickets = async () => {
  try {
    return await api.get("/tickets");
  } catch (error) {
    console.error('Failed to fetch tickets:', error);
    throw error;
  }
};

export const classifyAnswer = async (text) => {
  try {
    return await api.post("/classify_answer", { text });
  } catch (error) {
    console.error('Failed to classify answer:', error);
    throw error;
  }
};


export default api;
