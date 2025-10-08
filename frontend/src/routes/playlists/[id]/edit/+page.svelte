<script lang="ts">
  import type { PageData } from "./$types";
  import api from "$lib/api";
  import { X } from "lucide-svelte";
  const { data } = $props<{ data: PageData }>();
  import { writable } from "svelte/store";
  let playlist = $state(writable(data.playlist));

  let youtubeUrl = $state("");
  let title = $state("");
  let artist = $state("");
  let isAdding = $state(false);
  let formError = $state<string | null>(null);

  async function handleAddSong() {
    isAdding = true;
    formError = null;
    try {
      const response = await api.post(`/playlists/${$playlist.id}/add-song/`, {
        youtube_url: youtubeUrl,
        title: title,
        artist: artist,
      });
      playlist.set(response.data);
      youtubeUrl = "";
      title = "";
      artist = "";
    } catch (err: any) {
      formError = err.response?.data?.detail || "Failed to add song.";
    } finally {
      isAdding = false;
    }
  }
  async function handleRemoveSong(songId: number) {
    if (
      !confirm("Are you sure you want to remove this song from the playlist?")
    ) {
      return;
    }

    try {
      const response = await api.post(
        `/playlists/${$playlist.id}/remove-song/`,
        {
          song_id: songId,
        }
      );
      playlist.set(response.data);
    } catch (error) {
      console.error("Failed to remove song", error);
      alert("Could not remove the song.");
    }
  }
</script>

<div class="container mx-auto p-8 text-white">
  <h1 class="text-4xl font-bold">Editing: {$playlist.name}</h1>

  <!-- Form for adding a new song -->
  <div class="my-8 p-6 rounded-lg bg-gray-800/50">
    <h2 class="text-2xl font-semibold mb-4">Add a New Song</h2>
    <form onsubmit={handleAddSong} class="space-y-4">
      <input
        bind:value={youtubeUrl}
        type="url"
        placeholder="YouTube URL"
        required
        class="w-full p-2 text-white rounded-md"
      />
      <input
        bind:value={title}
        type="text"
        placeholder="Song Title"
        required
        class="w-full p-2 text-white rounded-md"
      />
      <input
        bind:value={artist}
        type="text"
        placeholder="Artist Name"
        required
        class="w-full p-2 text-white rounded-md"
      />
      <button
        type="submit"
        disabled={isAdding}
        class="p-2 bg-green-600 rounded-md disabled:bg-gray-500"
      >
        {isAdding ? "Processing..." : "Add Song to Playlist"}
      </button>
      {#if formError}<p class="text-red-400 mt-2">{formError}</p>{/if}
    </form>
  </div>

  <!-- List of current songs -->
  <div>
        <h2 class="text-2xl font-semibold mb-4">Current Songs ({$playlist.songs.length})</h2>
        <div class="space-y-2">
            {#each $playlist.songs as song (song.id)}
                <div class="flex items-center justify-between p-3 bg-gray-700/50 rounded-md">
                    <div>
                        <p class="font-bold">{song.title}</p>
                        <p class="text-sm text-gray-400">{song.artist_name}</p>
                    </div>
                    <button 
                        onclick={() => handleRemoveSong(song.id)}
                        title="Remove Song"
                        class="p-2 rounded-full text-gray-400 transition hover:bg-red-500 hover:text-white"
                    >
                        <X class="h-5 w-5"/>
                    </button>
                </div>
            {:else}
                <p class="text-gray-400">This playlist is empty. Add a song to get started!</p>
            {/each}
        </div>
    </div>
</div>
