<script lang="ts">
  import { setAuth } from '$lib/authStore';
  import api from '$lib/api';
  import { goto } from '$app/navigation';
  import type { User } from '$lib/types';
  import { addToast } from '$lib/toastStore';

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
      addToast("Login successful! Welcome back.", 'success');
      goto('/');
    } catch (err) {
      error = 'Invalid username or password.';
      addToast(error, 'error');
    }
  }
</script>

<div class="w-full max-w-xl glass p-4 md:p-8">
  <h1 class="text-3xl font-sembold mb-4">Login</h1>
  <form onsubmit={handleLogin} class="space-y-4">
    <label for="username" class="mb-1 block text-sm font-medium text-white/70">Username</label>
    <input bind:value={username} id="username" name="username" type="text" required class="w-full rounded-lg border border-white/20 p-2 text-white placeholder-white/70 focus:border-[#00c4e5] focus:outline-none focus:ring-[#00c4e5]" />
    <label for="password" class="mb-1 block text-sm font-medium text-white/70">Password</label>
    <input bind:value={password} id="password" name="password" type="password" required class="w-full rounded-lg border border-white/20 p-2 text-white placeholder-white/70 focus:border-[#00c4e5] focus:outline-none focus:ring-[#00c4e5]" />
    <button type="submit" class="w-full rounded-lg mt-3 bg-[#00e0ff] px-4 py-2 font-bold text-black transition hover:bg-[#00c4e5] disabled:cursor-not-allowed disabled:bg-[#009cc0]">Login</button>
  </form>
  <p class="mt-4 text-center text-sm text-white/70">
		Don't have an account? <a href="/register" class="font-medium text-[#00e0ff] hover:underline">Sign up</a>
	</p>
</div>