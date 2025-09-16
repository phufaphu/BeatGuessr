const BASE_URL = 'http://127.0.0.1:8000';

export interface Playlist {
    id: number;
    name: string;
    description: string;
}

export interface Song {
    id: number;
    title: string;
    audio_preview_url: string;
}

export interface PlaylistDetail extends Playlist {
    songs: Song[];
}

// functions to call the API

// Playlists
export async function getPlaylists(): Promise<Playlist[]> {
    const response = await fetch(`${BASE_URL}/api/playlists`);
    
    if (!response.ok) {
        throw new Error('Failed to fetch playlists');
    }
    
    return await response.json();
}

// Get details of a specific playlist by ID
export async function getPlaylistById(playlistId: number): Promise<PlaylistDetail> {
    const response = await fetch(`${BASE_URL}/api/playlists/${playlistId}`);

    if (!response.ok) {
        throw new Error(`Failed to fetch playlist with id ${playlistId}`);
    }
    
    return await response.json();
}