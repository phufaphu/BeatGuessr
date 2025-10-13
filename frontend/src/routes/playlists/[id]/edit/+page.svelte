<script lang="ts">
  import type { PageData } from "./$types";
  import api from "$lib/api";
  import { X } from "lucide-svelte";
  import { writable } from "svelte/store";
  import { addToast } from "$lib/toastStore";
  
  const { data } = $props<{ data: PageData }>();

  let playlist = $state(writable(data.playlist));
  let logs = $state<string[]>([]);
  let ws: WebSocket | null = null;
  let youtubeUrl = $state("");
  let youtubePlaylistUrl = $state("");
  let isImporting = $state(false);
  let importMessage = $state<string | null>(null);
  let title = $state("");
  let artist = $state("");
  let isAdding = $state(false);
  let formError = $state<string | null>(null);
  let selectedOption = $state<'playlist' | 'song'>('playlist');

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
      addToast('Song added successfully!', 'success');
    } catch (err: any) {
      formError = err.response?.data?.detail || "Failed to add song.";
      addToast(formError ?? "Failed to add song.", 'error');
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
      addToast('Song removed from playlist.', 'info');
    } catch (error) {
      console.error("Failed to remove song", error);
      addToast("Could not remove the song.", 'error');
    }
  }

  async function handleImportPlaylist() {
    isImporting = true;
    importMessage = null;
    setupWebSocket($playlist.id);
    try {
      const response = await api.post(
        `/playlists/${$playlist.id}/import-playlist/`,
        {
          youtube_playlist_url: youtubePlaylistUrl,
        }
      );
      importMessage = response.data.status;
      youtubePlaylistUrl = "";
      addToast(importMessage ?? "Import started successfully.", 'success');
    } catch (error) {
      importMessage = "Failed to start import process.";
      addToast(importMessage, 'error');
    } finally {
      isImporting = false;
    }
  }

  function setupWebSocket(playlistId: number) {
    if (ws) {
      console.log("Closing existing WebSocket connection.");
      ws.close();
    }
    const wsUrl = `ws://127.0.0.1:8000/ws/import-logs/${playlistId}/`;
    ws = new WebSocket(wsUrl);
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      logs.push(data.message);
      if (logs.length > 100) {
        logs.shift();
      }
    };
  }
</script>

<div class="p-4 space-y-4 text-white">
	<h1 class="text-3xl font-bold">Editing: {$playlist.name}</h1>

	<!-- Combined Add/Import Section -->
	<div class="p-6 rounded-lg glass space-y-4">
		<h2 class="text-2xl font-semibold">Add to Playlist</h2>
		<div class="flex flex-col space-y-4">
			<div>
				<label for="add-type" class="block mb-2 text-sm font-medium text-white/70"
					>I want to add a...</label
				>
				<select
					bind:value={selectedOption}
					id="add-type"
					class="w-full p-3 text-white glass"
				>
					<option class="text-black" value="playlist">YouTube Playlist</option>
					<option class="text-black" value="song">Single Song</option>
				</select>
			</div>

			{#if selectedOption === 'playlist'}
				<div>
					<p class="text-white/70 text-sm mb-2">
						Paste a YouTube playlist URL to automatically import all videos as songs. This process
						runs in the background.
					</p>
					<div class="grid grid-cols-[1fr_1fr_auto] gap-4 items-center">
						<div class="col-span-2">
              <input
                type="text"
                placeholder="https://www.youtube.com/playlist?list=..."
                class="w-full p-3 rounded-xl glass placeholder-white/25 focus:outline-none focus:ring-2 focus:ring-[#00E0FF]"
                bind:value={youtubePlaylistUrl}
              />
            </div>
						<button
							class="px-6 py-3 rounded-xl bg-[#00E0FF] text-black font-semibold hover:bg-[#00c4e5] transition"
              onclick={handleImportPlaylist}
						>
							{isImporting ? 'Starting Import...' : 'Start Import'}
						</button>
					</div>
					{#if importMessage}
						<div class="mt-4 p-4 rounded-md bg-green-600 bg-opacity-30 text-white">
							{importMessage}
							<p class="text-sm text-gray-200">
								Note: It may take a few minutes for songs to appear. You can refresh the page to
								check progress.
							</p>
						</div>
					{/if}
				</div>
			{:else}
				<!-- Add Single Song UI -->
				<div>
          <p class="text-white/70 text-sm mb-2">
            Paste a YouTube URL and enter the title and artist to add a single song.
          </p>
          <div class="mb-4">
            <input
              bind:value={youtubeUrl}
              id="youtube-url"
              type="text"
              placeholder="https://www.youtube.com/watch?v=..."
              class="w-full p-3 rounded-xl glass placeholder-white/25 focus:outline-none focus:ring-2 focus:ring-[#00E0FF]"
            />
          </div>
					<div class="grid grid-cols-1 md:grid-cols-[1fr_1fr_auto] gap-4 items-end">
	          <div>
              <input
                id="song-title"
                type="text"
                placeholder="Enter title"
                class="w-full p-3 rounded-xl glass placeholder-white/25 focus:outline-none focus:ring-2 focus:ring-[#00E0FF]"
                bind:value={title}
              />
	          </div>
            <div>
              <input
                id="artist-name"
                type="text"
                placeholder="Enter artist"
                class="w-full p-3 rounded-xl glass placeholder-white/25 focus:outline-none focus:ring-2 focus:ring-[#00E0FF]"
                bind:value={artist}
              />
            </div>
            <button
              class="w-full md:w-auto px-6 py-3 rounded-xl bg-[#00E0FF] text-black font-semibold hover:bg-[#00c4e5] transition"
              onclick={handleAddSong}
            >
              {isAdding ? 'Processing...' : 'Add Song'}
            </button>
          </div>
					{#if formError}
						<div class="mt-4 p-4 rounded-md bg-red-600 bg-opacity-30 text-white">
							{formError}
						</div>
					{/if}
				</div>
			{/if}
		</div>
	</div>

	{#if selectedOption === 'playlist'}
		<div class="p-6 rounded-lg glass space-y-4">
			<h2 class="text-2xl font-semibold">Import Logs</h2>
			<div class="p-4 rounded-md min-h-[150px] border border-white/20 bg-whie/20 overflow-y-auto max-h-64">
				{#if logs.length > 0}
					<ul class="space-y-2">
						{#each logs as log (log)}
							<li class="font-poppins text-sm text-gray-100">{log}</li>
						{/each}
					</ul>
				{:else}
					<p class="text-white/70">Logs will appear here when you start an import.</p>
				{/if}
			</div>
		</div>
	{/if}

	<!-- Current Songs Section -->
	<div class="p-6 rounded-lg glass">
		<h2 class="text-2xl font-semibold mb-4">Current Songs ({$playlist.songs.length})</h2>
		<div class="space-y-4">
			{#each $playlist.songs as song (song.id)}
				<div
					class="flex items-center justify-between p-4 glass"
				>
					<div>
						<p class="font-bold">{song.title}</p>
						<p class="text-sm text-white/70">{song.artist_name}</p>
					</div>
					<button
						onclick={() => handleRemoveSong(song.id)}
						title="Remove Song"
						class="p-2 rounded-full text-gray-400 transition hover:bg-[#FF5ACD] hover:text-white"
					>
						<X />
					</button>
				</div>
			{:else}
				<p class="text-white/70">This playlist is empty. Add a song to get started!</p>
			{/each}
		</div>
	</div>
</div>