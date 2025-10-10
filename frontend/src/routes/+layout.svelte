<script lang="ts">
  import "../app.css";
  import favicon from "$lib/assets/favicon.svg";
  import type { LayoutProps } from "./$types";
  let { children }: LayoutProps = $props();
  import { user, isAuthReady, initializeAuth } from "$lib/authStore";
  import ToastContainer from "$lib/components/ToastContainer.svelte";
  import { onMount } from "svelte";
  import { User } from 'lucide-svelte';

  onMount(() => {
    initializeAuth();
  });
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>
<ToastContainer />
{#if !$isAuthReady}
  <div class="flex min-h-screen items-center justify-center bg-gradient-to-tr from-[#1E1F29] via-[#2A2D3E] to-[#3A0CA3]">
    <p class="text-white font-bold text-3xl text-center px-4">Initializing application...</p>
  </div>
{:else}
  <div class="min-h-screen bg-gradient-to-tr from-[#1E1F29] via-[#2A2D3E] to-[#3A0CA3] p-4 font-poppins text-white flex flex-col">
    <nav
      class="relative flex flex-wrap justify-between items-center top-4 glass p-4 sm:mx-8 md:mx-20 lg:mx-40 xl:mx-52 rounded-2xl gap-4"
    >
      <div class="flex flex-wrap items-center gap-4 sm:gap-6 md:gap-8">
        <a href="/" class="text-xl sm:text-2xl font-extrabold font-orbitron">BeatGuessr</a>
        <a href="/playlists" class="text-sm sm:text-md text-white font-bold hover:text-[#FF5ACD] transition">
          Playlists
        </a>
      </div>
      <div class="flex items-center gap-3 sm:gap-4">
        {#if $user}
          <a href="/profile" class="transition hover:text-[#FF5ACD]">
            <User class="h-6 w-6 sm:h-7 sm:w-7 md:h-8 md:w-8" />
          </a>
        {:else}
          <a href="/login" class="px-2 sm:px-3 py-1 sm:py-2 text-sm sm:text-md font-bold hover:text-[#FF5ACD] transition">
            Login
          </a>
          <a href="/register" class="px-2 sm:px-3 py-1 sm:py-2 text-sm sm:text-md font-bold hover:text-[#FF5ACD] transition">
            Register
          </a>
        {/if}
      </div>
    </nav>
    <main class="flex-1 flex items-center justify-center mt-4 sm:mt-6 md:mt-8 text-center">
      {@render children?.()}
    </main>
  </div>
{/if}