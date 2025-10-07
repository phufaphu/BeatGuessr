<script lang="ts">
  import { setAuth } from '$lib/authStore';
  import api from '$lib/api';
  import { goto } from '$app/navigation';
  import type { User } from '$lib/types';

  let username = $state('');
  let password = $state('');
  let error = $state<string | null>(null);

  async function handleLogin() {
    try {
      const tokenResponse = await api.post('/token/', { username, password });
      const newAccessToken = tokenResponse.data.access;
      const userResponse = await api.get('/users/me/', {
        headers: {
          Authorization: `Bearer ${newAccessToken}`
        }
      });
      const newUser = userResponse.data as User;
      localStorage.setItem('accessToken', newAccessToken);
      localStorage.setItem('user', JSON.stringify(newUser));
      setAuth(newAccessToken, newUser);
      goto('/');
    } catch (err) {
      error = 'Invalid username or password.';
    }
  }
</script>

<div class="p-8">
  <h1 class="text-3xl mb-4">Login</h1>
  <form onsubmit={handleLogin} class="space-y-4">
    <input bind:value={username} placeholder="Username" class="p-2 w-full text-white">
    <input bind:value={password} type="password" placeholder="Password" class="p-2 w-full text-white">
    <button type="submit" class="p-2 bg-purple-600 w-full">Login</button>
    {#if error}<p class="text-red-500">{error}</p>{/if}
  </form>
</div>