<script lang="ts">
    import api from '$lib/api';
    import { user } from '$lib/authStore';
    import { onMount } from 'svelte';

    let playlists: any[] = $state([]);
    let isLoading: boolean = $state(true);

    onMount(async () => {
        try {
            const response = await api.get('/playlists/');
            playlists = response.data;
        } catch (error) {
            console.error("Failed to load playlists", error);
        } finally {
            isLoading = false;
        }
    });
</script>

<div class="container mx-auto p-8">
    <div class="flex items-center justify-between mb-6">
        <h1 class="text-4xl font-bold text-white">Playlists</h1>
        
        {#if $user?.is_staff}
            <a href="/playlists/create" class="rounded-lg bg-green-600 px-4 py-2 font-bold text-white hover:bg-green-700">
                Create New Playlist
            </a>
        {/if}
    </div>

    {#if isLoading}
        <p class="text-white">Loading playlists...</p>
    {:else}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each playlists as playlist}
                <a href="/" class="block rounded-lg bg-gray-800/50 p-6 transition hover:bg-gray-700/50">
                    <h2 class="text-2xl font-bold text-purple-300">{playlist.name}</h2>
                </a>
            {/each}
        </div>
    {/if}
</div>