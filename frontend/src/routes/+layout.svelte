<script lang="ts">
  import "../app.css";
  import favicon from '$lib/assets/favicon.svg';
  import type { LayoutProps } from './$types';
  let { children }: LayoutProps = $props();

  import { user, clearAuth } from '$lib/authStore';
  import { goto } from '$app/navigation';

  function handleLogout() {
    clearAuth();
    goto('/login');
  }
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>
<div class="min-h-screen bg-gray-900 text-white">
  <nav class="bg-gray-800 p-4 flex justify-between items-center">
    <a href="/" class="text-xl font-bold">BeatGuessr</a>
    <div>
      {#if $user}
        <span>Welcome, {$user.username}!</span>
        <button onclick={handleLogout} class="ml-4 p-2 bg-red-600"
          >Logout</button
        >
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
