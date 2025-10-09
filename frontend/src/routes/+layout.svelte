<script lang="ts">
  import "../app.css";
  import favicon from "$lib/assets/favicon.svg";
  import type { LayoutProps } from "./$types";
  let { children }: LayoutProps = $props();
  import { user, isAuthReady, initializeAuth, clearAuth } from "$lib/authStore";
  import { goto } from "$app/navigation";
  import ToastContainer from "$lib/components/ToastContainer.svelte";
  import { addToast } from "$lib/toastStore";
  import { onMount } from "svelte";

  onMount(() => {
    initializeAuth();
  });

  function handleLogout() {
    clearAuth();
	addToast("Logged out successfully.", 'info');
    goto("/login");
  }
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>
<ToastContainer />
{#if !$isAuthReady}
  <div class="flex min-h-screen items-center justify-center bg-gradient-to-tr from-[#1E1F29] via-[#2A2D3E] to-[#3A0CA3]">
    <p class="text-white font-bold text-3xl">Initializing application...</p>
  </div>
{:else}
  <div class="min-h-screen bg-gradient-to-tr from-[#1E1F29] via-[#2A2D3E] to-[#3A0CA3] p-4 font-poppins text-white flex flex-col">
    <nav class="relative flex justify-between items-center top-4 glass p-4 mx-52">
      <div class="flex items-center gap-8">
        <a href="/" class="text-2xl font-extrabold font-orbitron">BeatGuessr</a>
        <a href="/playlists" class="text-md text-white font-bold hover:text-[#FF5ACD] transition">Playlists</a>
      </div>
      <div>
        {#if $user}
          <div class="flex items-center gap-4">
            <a href="/profile" class="transition hover:text-[#FF5ACD]">
              Welcome, {$user.username}!
            </a>
            <button
              onclick={handleLogout}
              class="rounded bg-[#A855F7] px-3 py-2 text-md font-bold hover:bg-[#9133ea] transition"
              >Logout</button
            >
          </div>
        {:else}
          <a href="/login" class="px-3 py-2 text-md font-bold hover:text-[#FF5ACD] transition">Login</a>
          <a href="/register" class="px-3 py-2 text-md font-bold hover:text-[#FF5ACD] transition">Register</a>
        {/if}
      </div>
    </nav>
    <main class="flex-1 flex items-center justify-center">
      {@render children?.()}
    </main>
  </div>
{/if}
