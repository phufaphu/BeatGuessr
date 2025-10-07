<script lang="ts">
    import type { PageData } from './$types';
    import api from '$lib/api';

    const { data } = $props<{ data: PageData }>();
    
    let playlist = $state(data.playlist);

    let youtubeUrl = $state('');
    let title = $state('');
    let artist = $state('');
    let isAdding = $state(false);
    let formError = $state<string | null>(null);

    async function handleAddSong() {
        isAdding = true;
        formError = null;
        try {
            const response = await api.post(`/playlists/${playlist.id}/add-song/`, {
                youtube_url: youtubeUrl,
                title: title,
                artist: artist
            });
            playlist = response.data;
            youtubeUrl = '';
            title = '';
            artist = '';
        } catch (err: any) {
            formError = err.response?.data?.detail || "Failed to add song.";
        } finally {
            isAdding = false;
        }
    }
</script>

<div class="container mx-auto p-8 text-white">
    <h1 class="text-4xl font-bold">Editing: {playlist.name}</h1>

    <!-- Form for adding a new song -->
    <div class="my-8 p-6 rounded-lg bg-gray-800/50">
        <h2 class="text-2xl font-semibold mb-4">Add a New Song</h2>
        <form onsubmit={handleAddSong} class="space-y-4">
            <input bind:value={youtubeUrl} type="url" placeholder="YouTube URL" required class="w-full p-2 text-black rounded-md">
            <input bind:value={title} type="text" placeholder="Song Title" required class="w-full p-2 text-black rounded-md">
            <input bind:value={artist} type="text" placeholder="Artist Name" required class="w-full p-2 text-black rounded-md">
            <button type="submit" disabled={isAdding} class="p-2 bg-green-600 rounded-md disabled:bg-gray-500">
                {isAdding ? 'Processing...' : 'Add Song to Playlist'}
            </button>
            {#if formError}<p class="text-red-400 mt-2">{formError}</p>{/if}
        </form>
    </div>

    <!-- List of current songs -->
    <div>
        <h2 class="text-2xl font-semibold mb-4">Current Songs ({playlist.songs.length})</h2>
        <div class="space-y-2">
            {#each playlist.songs as song (song.id)}
                <div class="p-3 bg-gray-700/50 rounded-md">
                    <p class="font-bold">{song.title}</p>
                    <p class="text-sm text-gray-400">{song.artist_name}</p>
                </div>
            {:else}
                <p class="text-gray-400">This playlist is empty. Add a song to get started!</p>
            {/each}
        </div>
    </div>
</div>