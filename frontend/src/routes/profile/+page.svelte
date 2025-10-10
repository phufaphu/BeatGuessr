<script lang="ts">
	import api from '$lib/api';
	import { user } from '$lib/authStore';
	import { onMount } from 'svelte';
	import { Gamepad2, Calendar, Star } from 'lucide-svelte';
	import { addToast } from '$lib/toastStore';
	import { goto } from '$app/navigation';
    import { clearAuth } from '$lib/authStore';
	// --- State ---
	let history: any[] = $state([]);
	let isLoading = $state(true);
	let error: string | null = $state(null);

	// --- Data Fetching ---
	onMount(async () => {
		try {
			const response = await api.get('/users/me/history/');
			history = response.data;
		} catch (err) {
			console.error("Failed to fetch game history:", err);
			error = "Could not load your game history. Please try again later.";
		} finally {
			isLoading = false;
		}
	});

	// --- Helper function for formatting date ---
	function formatDate(dateString: string) {
		const date = new Date(dateString);
		return date.toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'long',
			day: 'numeric',
			hour: '2-digit',
			minute: '2-digit'
		});
	}

	function handleLogout() {
      clearAuth();
	  addToast("Logged out successfully.", 'info');
      goto("/login");
  }
</script>

<div class="min-h-screen container mx-auto md:p-4 text-white">
	<!-- User Profile Header -->
	{#if $user}
		<div class="mb-8 mt-8 glass p-6 text-center">
			<h1 class="text-4xl font-bold">{$user.username}'s Profile</h1>
			<p class="mt-2 text-lg text-white/70">{$user.email}</p>
			<div class="flex flex-col md:flex-row items-center justify-center md:gap-4">
				<a href="/profile/change-password" class="w-52 mt-4 inline-block rounded-lg border border-[#00c4e5] py-2 text-[#5bf3ff] font-bold transition hover:bg-[#00c4e5]">
					Change Password
				</a>
				<button
				onclick={handleLogout}
				class="w-52 mt-4 inline-block rounded-lg border border-[#00c4e5] py-2 text-[#5bf3ff] font-bold transition hover:bg-[#00c4e5]"
				>Logout</button
				>
			</div>
		</div>
	{/if}

	<!-- Game History Section -->
	<h2 class="mb-4 text-3xl font-semibold">Game History</h2>

	{#if isLoading}
		<div class="text-center">
			<p>Loading your epic gaming moments...</p>
		</div>
	{:else if error}
		<div class="rounded-md bg-red-800/50 p-4 text-center text-red-300">
			<p>{error}</p>
		</div>
	{:else if history.length === 0}
		<div class="glass p-6 text-center">
			<p class="text-xl">No games played yet!</p>
			<p class="mt-2 text-white/70">Time to make history. Go play a game!</p>
			<a href="/" class="mt-4 inline-flex items-center gap-2 glass px-4 py-2 font-bold transition hover:bg-[#009cc0]">
				<Gamepad2 />
				Play Now
			</a>
		</div>
	{:else}
		<div class="space-y-4">
			{#each history as game}
				<div class="flex flex-col md:flex-row items-center justify-between gap-4 rounded-lg glass p-4">
					<!-- Playlist Info -->
					<div class="flex-1 text-center md:text-left">
						<p class="text-xl font-bold">{game.playlist.name}</p>
						<div class="mt-1 flex items-center justify-center md:justify-start gap-2 text-white/70">
							<Calendar class="h-4 w-4" />
							<span>{formatDate(game.created_at)}</span>
						</div>
					</div>
					
					<!-- Score -->
					<div class="flex items-center gap-2 text-3xl font-bold text-yellow-400">
						<Star />
						<span>{game.score}</span>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>