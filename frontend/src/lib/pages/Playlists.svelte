<!-- frontend/src/pages/Playlists.svelte -->
<script lang="ts">
  import { mount, onMount } from 'svelte';
  import { getPlaylists, type Playlist } from '../api';
  import Nav from '../Nav.svelte';

  let playlists: Playlist[] = [];
  let isLoading = true;
  let error: string | null = null;
  
  onMount(async () => {
    try {
      playlists = await getPlaylists();
    } catch (e: any) {
      error = e.message;
    } finally {
      isLoading = false;
    }
  });
</script>

<div class="min-h-screen bg-gray-900 text-white">
  <Nav />
  <main class="p-8">
    <h1 class="text-4xl font-bold mb-6">Choose a Playlist</h1>
    
    {#if isLoading}
      <p>Loading playlists...</p>
    {:else if error}
      <p class="text-red-500">Error: {error}</p>
    {:else}
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {#each playlists as playlist}
          <div class="bg-gray-800 p-6 rounded-lg shadow-lg hover:bg-gray-700 transition-colors">
            <h2 class="text-2xl font-bold mb-2">{playlist.name}</h2>
            <p class="text-gray-400">{playlist.description}</p>
            <button class="mt-4 bg-cyan-500 text-white font-bold py-2 px-4 rounded hover:bg-cyan-600">
              Play
            </button>
          </div>
        {/each}
      </div>
    {/if}
  </main>
</div>