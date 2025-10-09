import { writable } from 'svelte/store';

export interface Toast {
    id: number;
    message: string;
    type: 'success' | 'error' | 'info';
}

export const toasts = writable<Toast[]>([]);

export function addToast(message: string, type: 'success' | 'error' | 'info' = 'info', duration: number = 3000) {
    const id = Date.now();

    toasts.update(allToasts => [...allToasts, { id, message, type }]);

    setTimeout(() => {
        toasts.update(allToasts => allToasts.filter(t => t.id !== id));
    }, duration);
}