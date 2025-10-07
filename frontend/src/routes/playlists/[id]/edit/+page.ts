import api from '$lib/api';
import { error } from '@sveltejs/kit';

export async function load({ params }) {
    try {
        const response = await api.get(`/playlists/${params.id}/`);
        return {
            playlist: response.data
        };
    } catch (e) {
        throw error(404, 'Playlist not found');
    }
}