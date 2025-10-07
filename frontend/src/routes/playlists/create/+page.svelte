<script lang="ts">
    import api from '$lib/api';
    import { goto } from '$app/navigation';

    let name = $state('');
    let error: string | null = $state(null);

    async function createPlaylist() {
        try {
            const response = await api.post('/playlists/', { name });
            goto(`/playlists/${response.data.id}/edit`);
        } catch (err) {
            error = "Failed to create playlist.";
        }
    }
</script>

<div class="container mx-auto p-8">
    <h1 class="text-4xl font-bold text-white">Create New Playlist</h1>
    <form onsubmit={createPlaylist} class="mt-6 max-w-lg">
        <input bind:value={name} placeholder="Playlist Name" required class="p-2 w-full text-black rounded-md">
        <button type="submit" class="mt-4 p-2 bg-purple-600 text-white rounded-md">Create and Edit</button>
        {#if error}<p class="text-red-500 mt-2">{error}</p>{/if}
    </form>
</div>