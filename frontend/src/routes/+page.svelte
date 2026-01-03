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
  import { addToast } from "$lib/toastStore";
  import { user } from '$lib/authStore';
	import { goto } from '$app/navigation';

  const ROUND_DURATION = 15;

  let gameState = $state<
    "idle" | "loading" | "countdown" | "playing" | "answered" | "finished"
  >("idle");
  let gameId = $state<number | null>(null);
  let score = $state(0);
  let lastPlayedPlaylist = $state<any>(null);
  let displayedRound = $state<any>(null);
  let currentRound = $state<any>(null);
  let lastAnswer = $state<{ isCorrect: boolean; correctSongId: number } | null>(
    null
  );
  let countdownValue = $state(3);
  let countdownInterval: any = null;

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
      handleStartClick(state.playlistId);
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
  }

  async function fetchAndStartGame(playlistId: number | null) {
    gameState = "loading";
    try {
      const payload = { playlist_id: playlistId };
			const response = await api.post('/game/start/', payload);
      const data = response.data;

      gameId = data.game_id;
      score = data.score;
      currentRound = data.current_round;
      displayedRound = currentRound;
      lastAnswer = null;
      lastPlayedPlaylist = data.playlist; 
      gameState = "playing";
      startRoundTimer();
    } catch (error) {
      console.error("Failed to start game:", error);
      addToast("Failed to start game. Please try again.", "error");
      gameState = "idle";
    }
  }

  function startCountdown(playlistId: number | null = null) {
		gameState = 'countdown';
		countdownValue = 3;
		clearInterval(countdownInterval);
		countdownInterval = setInterval(() => {
			countdownValue--;
			if (countdownValue <= 0) {
				clearInterval(countdownInterval);
				fetchAndStartGame(playlistId);
			}
		}, 1000);
	}

  function goToNextRound() {
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
    if (untrack(() => gameState) !== "playing") {
      console.warn('Submit guess blocked because gameState is not "playing".');
      return;
    }
    clearInterval(timerInterval);
    try {
      const response = await api.post("/game/guess/", {
        game_id: gameId,
        round_id: currentRound.round_id,
        choice_id: choiceId,
      });
      const result = response.data;

      gameState = "answered";
      score = result.new_score;
      lastAnswer = {
        isCorrect: result.is_correct,
        correctSongId: result.correct_song_id,
      };
      currentRound = result.next_round;

      setTimeout(goToNextRound, 2500);
    } catch (error) {
      gameState = "playing";
      startRoundTimer();
    }
  }

  function resetGame() {
    startCountdown(lastPlayedPlaylist?.id ?? null);
  };
  
  function handleStartClick(playlistId: number | null = null) {
		if ($user) {
    // 🔊 Unlock audio for mobile
    if (audioPlayer) {
      audioPlayer.play().then(() => {
        if (audioPlayer) {
          audioPlayer.pause();
          audioPlayer.currentTime = 0;
        }
      }).catch(() => {
        console.log('Audio unlock failed (probably fine on desktop)');
      });
    }

    startCountdown(playlistId);
  } else {
    addToast("Please log in to start a game.");
    goto('/login');
  }
	}
</script>

<div
  class="w-full max-w-xl glass p-4 md:p-8"
>
  <!-- Header -->
  <div class="mb-6 flex items-center justify-center gap-3">
    <Music class="h-12 w-12 text-[#00E0FF]" />
    <h1 class="text-4xl font-bold font-orbitron tracking-wider">BeatGuessr</h1>
  </div>

  <!-- State: IDLE -->
  {#if gameState === "idle"}
    <div class="text-center">
      <p class="mb-6 text-white/70">
        Come prove your music knowledge!
      </p>
      <button
        onclick={() => handleStartClick()}
        class="flex w-full items-center justify-center gap-2 bg-[#00E0FF] text-black font-semibold px-4 py-3 rounded-lg shadow-[0_0_10px_#00E0FF,0_0_30px_#00E0FF] hover:scale-105 active:scale-95 transition-transform"
      >
        <Gamepad2 />
        Start New Game
      </button>
    </div>
  {/if}

  <!-- State: COUNTDOWN -->
  {#if gameState === "countdown"}
    <div class="flex flex-col items-center justify-center gap-4 py-10">
      <div class="relative flex h-32 w-32 items-center justify-center">
        <div
          class="absolute h-full w-full animate-ping rounded-full bg-[#00E0FF] opacity-75"
        ></div>
        <p class="relative text-8xl font-bold">{countdownValue}</p>
      </div>
    </div>
  {/if}

  <!-- State: LOADING -->
  {#if gameState === "loading"}
    <div class="flex flex-col items-center justify-center gap-4 py-10">
      <div
        class="h-16 w-16 animate-spin rounded-full border-4 border-white/25 border-t-[#00E0FF]"
      ></div>
      <p class="text-lg text-white/70">Checking answer...</p>
    </div>
  {/if}

  <!-- State: PLAYING or ANSWERED -->
  {#if (gameState === "playing" || gameState === "answered") && displayedRound}
    <div class="space-y-5">
      <div class="flex justify-between items-center text-lg">
        <div class="font-semibold text-2xl"
          >Score: <span class="text-[#5bf3ff]">{score}</span></div
        >
        <div
          class="flex items-center gap-2 rounded-full bg-black/20 px-3 py-1 text-[#5bf3ff] w-[45%]"
        >
          <Timer class="h-8 w-8" />
          <span class="text-xl font-bold">{timerValue}</span>
          <div class="w-full rounded-full bg-white/10 h-2 overflow-hidden">
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
        playsinline
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
                <p class="text-xl font-semibold">{choice.title}</p>
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
      <h2 class="text-3xl font-bold">Congratulations!</h2>
      <p class="mt-2 text-xl text-white/70">Your final score is:</p>
      <p class="my-4 text-7xl font-bold text-[#5bf3ff]">{score}</p>
      <button
        onclick={resetGame}
        class="flex w-full items-center justify-center gap-2 rounded-lg bg-[#00E0FF] px-4 py-3 font-bold transition hover:bg-[#00c4e5] hover:scale-105 active:scale-95"
      >
        <RefreshCw />
        Play Again
      </button>
    </div>
  {/if}
</div>
