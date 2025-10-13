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

<div class="container mx-auto p-4 glass">
    <h1 class="text-4xl font-bold text-white mt-2">Create New Playlist</h1>
    <form onsubmit={createPlaylist} class="mt-4 max-w-lg">
        <input bind:value={name} placeholder="Playlist Name" required class="w-full rounded-lg p-2 text-white placeholder-white/20 focus:outline-none"/>
        <button type="submit" class="mt-4 p-2 bg-[#A855F7] text-white rounded-md hover:bg-[#A855F7]/80 transition">Create and Edit</button>
        {#if error}<p class="text-red-500 mt-2">{error}</p>{/if}
    </form>
</div>