<script lang="ts">
	import axios from 'axios';
	import { Gamepad2, Music, CheckCircle2, XCircle } from 'lucide-svelte';

    const API_BASE_URL = 'http://127.0.0.1:8000/api';

	let gameState: 'idle' | 'loading' | 'playing' | 'answered' | 'finished' = $state('idle');
	let gameId: number | null = $state(null);
	let score: number = $state(0);
	let currentRound: any = $state(null);
	let lastAnswer: { isCorrect: boolean; correctSongId: number } | null = $state(null);

	const startGame = async () => {
		gameState = 'loading';
		try {
            const response = await axios.post(`${API_BASE_URL}/game/start/`, { playlist_id: 1 });
			const data = response.data;
			
			gameId = data.game_id;
			score = data.score;
			currentRound = data.current_round;
			lastAnswer = null;
			gameState = 'playing';

		} catch (error) {
			console.error("Failed to start game:", error);
			alert("Could not start the game. Is the backend server running?");
			gameState = 'idle';
		}
	}

    const submitGuess = async (choiceId: number) => {
        alert(`You chose song ID: ${choiceId}. Next step is to check the answer!`);
    };
</script>

<main class="relative flex min-h-screen items-center justify-center bg-gradient-to-br from-indigo-900 via-purple-800 to-pink-900 p-4 font-sans text-white">
	<div class="w-full max-w-md rounded-2xl border border-white/20 bg-white/10 p-6 text-white shadow-lg backdrop-blur-xl md:p-8">
		<!-- Header -->
		<div class="mb-6 flex items-center justify-center gap-3">
			<Music class="h-8 w-8 text-purple-300" />
			<h1 class="text-4xl font-bold tracking-wider">BeatGuessr</h1>
		</div>
		<!-- State: IDLE -->
		{#if gameState === 'idle'}
			<div class="text-center">
				<p class="mb-6 text-white/80">Guess the song from the audio clip. Are you ready?</p>
				<button onclick={startGame} class="flex w-full items-center justify-center gap-2 rounded-lg bg-purple-600 px-4 py-3 font-bold transition hover:bg-purple-700">
					<Gamepad2 />
					Start New Game
				</button>
			</div>
		{/if}
		<!-- State: LOADING -->
		{#if gameState === 'loading'}
			<div class="flex flex-col items-center justify-center gap-4 py-10">
				<div class="h-12 w-12 animate-spin rounded-full border-4 border-white/20 border-t-purple-400"></div>
				<p class="text-lg text-white/80">Starting the game...</p>
			</div>
		{/if}
		<!-- State: PLAYING or ANSWERED -->
		{#if (gameState === 'playing' || gameState === 'answered') && currentRound}
			<div class="space-y-5">
				<!-- Score & Round Info -->
				<div class="flex justify-between text-lg">
					<span class="font-semibold">Score: <span class="text-purple-300">{score}</span></span>
				</div>

				<!-- Audio Player -->
				<audio controls src={currentRound.snippet_url} class="hidden" autoplay></audio>

				<!-- Choices -->
				<div class="grid grid-cols-1 gap-3 pt-2">
					{#each currentRound.choices as choice}
						<button 
							onclick={() => submitGuess(choice.id)}
							class="group w-full rounded-lg border-2 border-white/30 p-3 text-left transition hover:bg-white/20"
						>
							<p class="font-semibold">{choice.title}</p>
							<p class="text-sm text-white/70">{choice.artist_name}</p>
						</button>
					{/each}
				</div>
			</div>
		{/if}
	</div>
</main>