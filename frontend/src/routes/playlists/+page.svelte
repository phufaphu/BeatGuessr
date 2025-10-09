<script lang="ts">
    import api from '$lib/api';
    import { user } from '$lib/authStore';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { SquarePen, Gamepad2, Plus } from 'lucide-svelte';

    interface SimplePlaylist {
        id: number;
        name: string;
    }

    let playlists: SimplePlaylist[] = $state([]);
    let isLoading: boolean = $state(true);

    onMount(async () => {
        isLoading = true;
        try {
            const response = await api.get('/playlists/');
            playlists = response.data;
        } catch (error) {
            console.error("Failed to load playlists", error);
        } finally {
            isLoading = false;
        }
    });

    function handlePlay(playlistId: number) {
        goto('/', { state: { playlistId: playlistId } });
    }
</script>

<div class="container mx-auto p-4 md:p-8">
    <div class="flex items-center justify-between mb-6">
        <h1 class="text-4xl font-bold text-white">Playlists</h1>
        
        {#if $user?.is_staff}
            <a href="/playlists/create" class="inline-flex items-center justify-center gap-2 rounded-lg bg-green-600 px-4 py-2 font-bold text-white transition hover:bg-green-700">
                <Plus class="h-5 w-5"/>
                Create New
            </a>
        {/if}
    </div>

    {#if isLoading}
        <div class="text-center py-10">
            <p class="text-white text-lg">Loading playlists...</p>
        </div>
    {:else if playlists.length === 0}
         <div class="text-center py-10 rounded-lg bg-gray-800/50">
            <p class="text-white text-xl">No playlists found.</p>
            {#if $user?.is_staff}
                <p class="text-gray-400 mt-2">Click "Create New" to get started.</p>
            {/if}
        </div>
    {:else}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each playlists as playlist (playlist.id)}
                <div class="flex flex-col justify-between rounded-lg bg-gray-800/50 p-6 transition hover:shadow-lg hover:ring-2 hover:ring-purple-500">
                    <div>
                        <h2 class="text-2xl font-bold text-purple-300 truncate">{playlist.name}</h2>
                    </div>
                    
                    <div class="mt-4 flex items-center gap-2">
                        <button 
                            onclick={() => handlePlay(playlist.id)}
                            class="flex-1 inline-flex items-center justify-center gap-2 rounded-md bg-purple-600 px-3 py-2 text-sm font-bold text-white hover:bg-purple-700"
                        >
                            <Gamepad2 class="h-4 w-4"/>
                            Play
                        </button>
                        
                        {#if $user?.is_staff}
                            <a 
                                href={`/playlists/${playlist.id}/edit`}
                                title="Edit Playlist"
                                class="inline-flex items-center justify-center gap-2 rounded-md border border-gray-500 p-2 text-gray-300 hover:bg-gray-700"
                            >
                                <SquarePen class="h-4 w-4"/>
                            </a>
                        {/if}
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</div>