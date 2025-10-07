import axios from 'axios';
import { accessToken } from './authStore';
import { get } from 'svelte/store';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api'
});

api.interceptors.request.use(config => {
    const token = get(accessToken); 
    
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;