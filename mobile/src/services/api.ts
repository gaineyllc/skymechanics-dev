// SkyMechanics Mobile App - API Service
// Handles all backend API calls

import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE_URL = __DEV__ ? 'http://localhost:8200' : 'https://api.skymechanics.com';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for token
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid - clear and redirect
      AsyncStorage.removeItem('auth_token');
      // navigation.navigate('Login'); // Requires navigation ref
    }
    return Promise.reject(error);
  }
);

// Auth endpoints
export const auth = {
  login: (email: string, password: string) => api.post('/api/v1/auth/login', { email, password }),
  register: (email: string, password: string, name: string) => api.post('/api/v1/auth/register', { email, password, name }),
  refresh: (token: string) => api.post('/api/v1/auth/refresh', { token }),
};

// Jobs endpoints
export const jobs = {
  list: () => api.get('/api/v1/jobs'),
  get: (id: string) => api.get(`/api/v1/jobs/${id}`),
  create: (data: any) => api.post('/api/v1/jobs', data),
  update: (id: string, data: any) => api.put(`/api/v1/jobs/${id}`, data),
  updateStatus: (id: string, status: string) => api.patch(`/api/v1/jobs/${id}/status`, { status }),
};

// Mechanics endpoints
export const mechanics = {
  list: () => api.get('/api/v1/mechanics'),
  get: (id: string) => api.get(`/api/v1/mechanics/${id}`),
  updateLocation: (id: string, latitude: number, longitude: number) =>
    api.patch(`/api/v1/mechanics/${id}/location`, { latitude, longitude }),
};

// Profile endpoints
export const profile = {
  get: () => api.get('/api/v1/profile'),
  update: (data: any) => api.put('/api/v1/profile', data),
};

export default api;
