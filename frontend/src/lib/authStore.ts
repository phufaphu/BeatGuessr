import { writable, type Writable } from 'svelte/store';
import type { User } from './types';

export const user: Writable<User | null> = writable(null);
export const accessToken: Writable<string | null> = writable(null);
export const isAuthReady = writable<boolean>(false);

export function initializeAuth() {
    if (typeof window !== 'undefined') {
        const storedToken = localStorage.getItem('accessToken');
        const storedUser = localStorage.getItem('user');
        if (storedToken && storedUser) {
            accessToken.set(storedToken);
            user.set(JSON.parse(storedUser));
        }
        isAuthReady.set(true);
    }
}

export function setAuth(newAccessToken: string, newUser: User) {
    accessToken.set(newAccessToken);
    user.set(newUser);
}

export function clearAuth() {
    accessToken.set(null);
    user.set(null);
	if (typeof window !== 'undefined') {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('user');
    }
}