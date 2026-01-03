import axios from 'axios';
import { accessToken } from './authStore';
import { get } from 'svelte/store';

const api = axios.create({ baseURL: '/api' });

api.interceptors.request.use(
    (config) => {
        const token = get(accessToken);
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);
export default api;