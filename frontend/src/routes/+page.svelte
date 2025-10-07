<script lang="ts">
  import { untrack } from "svelte";
  import api from "$lib/api";
  import {
    Gamepad2,
    Music,
    CircleCheck,
    CircleX,
    RefreshCw,
    Trophy,
    Timer,
  } from "lucide-svelte";
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  const ROUND_DURATION = 15;

  let gameState = $state<
    "idle" | "loading" | "playing" | "answered" | "finished"
  >("idle");
  let gameId = $state<number | null>(null);
  let score = $state(0);
  let displayedRound = $state<any>(null);
  let currentRound = $state<any>(null);
  let lastAnswer = $state<{ isCorrect: boolean; correctSongId: number } | null>(
    null
  );

  let audioPlayer = $state<HTMLAudioElement | null>(null);
  let timerInterval: any = null;
  let timerValue = $state(ROUND_DURATION);

  $effect(() => {
    if (gameState === "playing" && displayedRound && audioPlayer) {
      console.log("Effect triggered: Playing audio for new round.");
      audioPlayer.currentTime = 0;
      audioPlayer.play().catch((e) => console.error("Audio play failed:", e));
    }
  });

  const progress = $derived((timerValue / ROUND_DURATION) * 100);

  onMount(() => {
        const state = $page.state as { playlistId?: number };
        if (state && state.playlistId) {
            startGame(state.playlistId);
        }
    });

  async function startRoundTimer() {
    clearInterval(timerInterval);
    timerValue = ROUND_DURATION;
    timerInterval = setInterval(() => {
      untrack(() => timerValue--);
      if (timerValue <= 0) {
        clearInterval(timerInterval);
        submitGuess(0);
      }
    }, 1000);
  };

  async function startGame(playlistId: number = 1) {
    gameState = "loading";
    try {
      const response = await api.post('/game/start/', { playlist_id: playlistId });
      const data = response.data;
      gameId = data.game_id;
      score = data.score;
      currentRound = data.current_round;
      displayedRound = currentRound;
      lastAnswer = null;
      gameState = "playing";
      startRoundTimer();
    } catch (error) {
      console.error("Failed to start game:", error);
      alert("Could not start the game. Is the backend server running?");
      gameState = "idle";
    }
  };

  const goToNextRound = () => {
    if (currentRound) {
      lastAnswer = null;
      displayedRound = currentRound;
      gameState = "playing";
      startRoundTimer();
    } else {
      gameState = "finished";
    }
  };

 async function submitGuess(choiceId: number) {
		if (untrack(() => gameState) !== 'playing') {
			console.warn('Submit guess blocked because gameState is not "playing".');
			return;
		}
		clearInterval(timerInterval);
		try {
			const response = await api.post('/game/guess/', {
				game_id: gameId,
				round_id: currentRound.round_id,
				choice_id: choiceId
			});
			const result = response.data;

			gameState = 'answered';
			score = result.new_score;
			lastAnswer = {
				isCorrect: result.is_correct,
				correctSongId: result.correct_song_id
			};
			currentRound = result.next_round;

			setTimeout(goToNextRound, 2500);
		} catch (error) {
			gameState = 'playing';
			startRoundTimer();
		}
	};

  const resetGame = () => {
    gameState = "idle";
    gameId = null;
    score = 0;
    currentRound = null;
    displayedRound = null;
    lastAnswer = null;
    clearInterval(timerInterval);
  }
</script>

<main
  class="relative flex min-h-screen items-center justify-center bg-gradient-to-br from-indigo-900 via-purple-800 to-pink-900 p-4 font-sans text-white"
>
  <div
    class="w-full max-w-md rounded-2xl border border-white/20 bg-white/10 p-6 text-white shadow-lg backdrop-blur-xl md:p-8"
  >
    <!-- Header -->
    <div class="mb-6 flex items-center justify-center gap-3">
      <Music class="h-8 w-8 text-purple-300" />
      <h1 class="text-4xl font-bold tracking-wider">BeatGuessr</h1>
    </div>

    <!-- State: IDLE -->
    {#if gameState === "idle"}
      <div class="text-center">
        <p class="mb-6 text-white/80">
          Guess the song from the audio clip. Are you ready?
        </p>
        <button
          onclick={() => startGame()}
          class="flex w-full items-center justify-center gap-2 rounded-lg bg-purple-600 px-4 py-3 font-bold transition hover:bg-purple-700 active:scale-95"
        >
          <Gamepad2 />
          Start New Game
        </button>
      </div>
    {/if}

    <!-- State: LOADING -->
    {#if gameState === "loading"}
      <div class="flex flex-col items-center justify-center gap-4 py-10">
        <div
          class="h-12 w-12 animate-spin rounded-full border-4 border-white/20 border-t-purple-400"
        ></div>
        <p class="text-lg text-white/80">Checking answer...</p>
      </div>
    {/if}

    <!-- State: PLAYING or ANSWERED -->
    {#if (gameState === "playing" || gameState === "answered") && displayedRound}
      <div class="space-y-5">
        <div class="flex justify-between text-lg">
          <span class="font-semibold"
            >Score: <span class="text-purple-300">{score}</span></span
          >
          <div
            class="flex items-center gap-2 rounded-full bg-black/20 px-3 py-1 text-purple-300"
          >
            <Timer class="h-5 w-5" />
            <span class="font-mono text-xl font-bold">{timerValue}</span>
            <div class="w-full rounded-full bg-white/10">
              <div
                class="rounded-full h-2 transition-all duration-1000 ease-linear"
                class:bg-green-500={progress > 50}
                class:bg-yellow-500={progress <= 50 && progress > 25}
                class:bg-red-500={progress <= 25}
                style="width: {progress}%"
              ></div>
            </div>
          </div>
        </div>
        <audio
          controls
          src={displayedRound.snippet_url}
          class="w-full hidden"
          bind:this={audioPlayer}
        >
          Your browser does not support the audio element.
        </audio>

        <div class="grid grid-cols-1 gap-3 pt-2">
          {#each displayedRound.choices as choice}
            {@const isCorrect = lastAnswer?.correctSongId === choice.id}
            {@const isSelectedWrong =
              !isCorrect && lastAnswer && gameState === "answered"}

            <button
              onclick={() => submitGuess(choice.id)}
              disabled={gameState === "answered"}
              class={`group w-full rounded-lg border-2 p-3 text-left transition
								${isCorrect && gameState === "answered" ? "border-green-500" : ""}
								${isSelectedWrong ? "border-red-500" : ""}
								${!lastAnswer || gameState !== "answered" ? "border-white/30" : ""}
								${gameState === "playing" ? "hover:bg-white/20" : ""}
								${gameState === "answered" ? "cursor-wait" : ""}
							`}
            >
              <div class="flex items-center justify-between">
                <div>
                  <p class="font-semibold">{choice.title}</p>
                  <p class="text-sm text-white/70">{choice.artist_name}</p>
                </div>
                {#if gameState === "answered"}
                  {#if isCorrect}
                    <CircleCheck class="text-green-400" />
                  {:else}
                    <CircleX class="text-red-400 opacity-50" />
                  {/if}
                {/if}
              </div>
            </button>
          {/each}
        </div>
      </div>
    {/if}

    <!-- State: FINISHED (จบเกม) -->
    {#if gameState === "finished"}
      <div class="text-center">
        <Trophy class="mx-auto mb-4 h-16 w-16 text-yellow-400" />
        <h2 class="text-3xl font-bold">Game Over!</h2>
        <p class="mt-2 text-xl text-white/80">Your final score is:</p>
        <p class="my-4 text-7xl font-bold text-purple-300">{score}</p>
        <button
          onclick={resetGame}
          class="flex w-full items-center justify-center gap-2 rounded-lg bg-purple-600 px-4 py-3 font-bold transition hover:bg-purple-700 active:scale-95"
        >
          <RefreshCw />
          Play Again
        </button>
      </div>
    {/if}
  </div>
</main>
