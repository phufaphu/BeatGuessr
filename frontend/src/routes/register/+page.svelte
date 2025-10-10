<script lang="ts">
	import api from '$lib/api';
	import { goto } from '$app/navigation';
	import { setAuth } from '$lib/authStore';
    import { addToast } from '$lib/toastStore';
	let username = $state('');
	let password = $state('');
	let email = $state('');
	let error: string | null = $state(null);
	let isLoading = $state(false);

	async function handleRegister() {
		isLoading = true;
		error = null;
		try {
			await api.post('/users/register/', {
				username,
				password,
				email
			});
			const tokenResponse = await api.post('/token/', { username, password });
			const newAccessToken = tokenResponse.data.access;
			const userResponse = await api.get('/users/me/', {
				headers: {
					Authorization: `Bearer ${newAccessToken}`
				}
			});
			const newUser = userResponse.data;
            localStorage.setItem('accessToken', newAccessToken);
            localStorage.setItem('user', JSON.stringify(newUser));
			setAuth(newAccessToken, newUser);
            addToast("Registration successful! Welcome aboard.", 'success');
			goto('/');
		} catch (err: any) {
			if (err.response && err.response.data) {
				error = Object.values(err.response.data).join(' ');
			} else {
				error = 'An unknown error occurred during registration.';
			}
			console.error('Registration failed:', err);
			addToast("Registration failed. Please try again.", 'error');
		} finally {
			isLoading = false;
		}
	}
</script>

<div class="w-full max-w-xl glass p-4 md:p-8">
	<h1 class="mb-4 text-center text-3xl font-bold text-white">Create an Account</h1>
	<form onsubmit={handleRegister} class="space-y-4">
		<div>
			<label for="username" class="mb-1 block text-sm font-medium text-white/70">Username</label>
			<input
				bind:value={username}
				id="username"
				name="username"
				type="text"
				required
				class="w-full rounded-lg border border-white/20 p-2 text-white placeholder-white/20 focus:border-[#00c4e5] focus:outline-none focus:ring-[#00c4e5]"
				placeholder="Choose a username"
			/>
		</div>
		<div>
			<label for="email" class="mb-1 block text-sm font-medium text-white/70">Email Address</label>
			<input
				bind:value={email}
				id="email"
				name="email"
				type="email"
				required
				class="w-full rounded-lg border border-white/20 p-2 text-white placeholder-white/20 focus:border-[#00c4e5] focus:outline-none focus:ring-[#00c4e5]"
				placeholder="Enter your email address"
			/>
		</div>
		<div>
			<label for="password" class="mb-1 block text-sm font-medium text-white/70">Password</label>
			<input
				bind:value={password}
				id="password"
				name="password"
				type="password"
				required
				class="w-full rounded-lg border border-white/20 p-2 text-white placeholder-white/20 focus:border-[#00c4e5] focus:outline-none focus:ring-[#00c4e5]"
				placeholder="Create a password"
			/>
		</div>

		{#if error}
			<p class="text-sm text-red-400">{error}</p>
		{/if}

		<button
			type="submit"
			disabled={isLoading}
			class="w-full rounded-lg mt-2 bg-[#00e0ff] px-4 py-2 font-bold text-black transition hover:bg-[#00c4e5] disabled:cursor-not-allowed disabled:bg-[#009cc0]"
		>
			{#if isLoading}
				<span>Registering...</span>
			{:else}
				<span>Sign Up</span>
			{/if}
		</button>
	</form>
	<p class="mt-4 text-center text-sm text-white/70">
		Already have an account? <a href="/login" class="font-medium text-[#00e0ff] hover:underline">Log in</a>
	</p>
</div>
