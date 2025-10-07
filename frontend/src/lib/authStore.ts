import { writable } from 'svelte/store';
import type { User } from './types';

export const user = writable<User | null>(null);
export const accessToken = writable<string | null>(null);

export function setAuth(newAccessToken: string, newUser: User) {
    accessToken.set(newAccessToken);
    user.set(newUser);
}

export function clearAuth() {
    accessToken.set(null);
    user.set(null);
}