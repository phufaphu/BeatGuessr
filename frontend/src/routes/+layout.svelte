<script lang="ts">
  import "../app.css";
  import favicon from "$lib/assets/favicon.svg";
  import type { LayoutProps } from "./$types";
  let { children }: LayoutProps = $props();
  import { user, isAuthReady, initializeAuth, clearAuth } from "$lib/authStore";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  onMount(() => {
    initializeAuth();
  });

  function handleLogout() {
    clearAuth();
    goto("/login");
  }
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>
{#if !$isAuthReady}
  <div class="flex min-h-screen items-center justify-center bg-gray-900">
    <p class="text-white">Initializing application...</p>
  </div>
{:else}
  <div class="min-h-screen bg-gray-900 text-white">
    <nav class="bg-gray-800 p-4 flex justify-between items-center">
      <a href="/" class="text-xl font-bold">BeatGuessr</a>
      <div>
        {#if $user}
          <div class="flex items-center gap-4">
            <a href="/profile" class="transition hover:text-purple-300">
              Welcome, {$user.username}!
            </a>
            <button
              onclick={handleLogout}
              class="rounded bg-red-600 px-3 py-1 text-sm font-bold hover:bg-red-700"
              >Logout</button
            >
          </div>
        {:else}
          <a href="/login" class="p-2">Login</a>
          <a href="/register" class="p-2">Register</a>
        {/if}
      </div>
    </nav>
    <main>
      {@render children?.()}
    </main>
  </div>
{/if}
