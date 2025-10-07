<script lang="ts">
	import api from '$lib/api';
	import { ArrowLeft } from 'lucide-svelte';

	let oldPassword = $state('');
	let newPassword = $state('');
	let confirmPassword = $state('');

	let isLoading = $state(false);
	let error: string | null = $state(null);
	let successMessage: string | null = $state(null);

	async function handleChangePassword() {
		isLoading = true;
		error = null;
		successMessage = null;

		if (newPassword !== confirmPassword) {
			error = "New passwords do not match.";
			isLoading = false;
			return;
		}

		try {
			await api.post('/users/me/set-password/', {
				old_password: oldPassword,
				new_password: newPassword
			});
			successMessage = "Your password has been changed successfully!";
			oldPassword = '';
			newPassword = '';
			confirmPassword = '';
		} catch (err: any) {
			if (err.response && err.response.data) {
				error = Object.entries(err.response.data).map(([key, value]) => `${key}: ${value}`).join(' ');
			} else {
				error = "An unknown error occurred.";
			}
		} finally {
			isLoading = false;
		}
	}
</script>

<div class="container mx-auto p-4 md:p-8 text-white">
	<div class="mx-auto max-w-lg">
		<!-- Back to Profile Link -->
		<a href="/profile" class="mb-6 inline-flex items-center gap-2 text-purple-300 hover:underline">
			<ArrowLeft class="h-4 w-4" />
			Back to Profile
		</a>

		<div class="rounded-lg bg-gray-800/50 p-6">
			<h1 class="text-3xl font-bold">Change Password</h1>
			<p class="mt-2 text-gray-400">
				Choose a strong password that you're not using anywhere else.
			</p>

			<form onsubmit={handleChangePassword} class="mt-6 space-y-4">
				<div>
					<label for="old_password" class="mb-1 block text-sm font-medium text-gray-300">
						Current Password
					</label>
					<input
						bind:value={oldPassword}
						id="old_password"
						type="password"
						required
						class="w-full rounded-md border border-gray-600 bg-gray-700 p-2 text-white placeholder-gray-400 focus:border-purple-500 focus:outline-none focus:ring-purple-500"
					/>
				</div>
				<div>
					<label for="new_password" class="mb-1 block text-sm font-medium text-gray-300">
						New Password
					</label>
					<input
						bind:value={newPassword}
						id="new_password"
						type="password"
						required
						minlength="8"
						class="w-full rounded-md border border-gray-600 bg-gray-700 p-2 text-white placeholder-gray-400 focus:border-purple-500 focus:outline-none focus:ring-purple-500"
					/>
				</div>
				<div>
					<label for="confirm_password" class="mb-1 block text-sm font-medium text-gray-300">
						Confirm New Password
					</label>
					<input
						bind:value={confirmPassword}
						id="confirm_password"
						type="password"
						required
						class="w-full rounded-md border border-gray-600 bg-gray-700 p-2 text-white placeholder-gray-400 focus:border-purple-500 focus:outline-none focus:ring-purple-500"
					/>
				</div>
				
				{#if successMessage}
					<p class="text-sm text-green-400">{successMessage}</p>
				{/if}
				{#if error}
					<p class="text-sm text-red-400">{error}</p>
				{/if}

				<button
					type="submit"
					disabled={isLoading}
					class="w-full rounded-md bg-purple-600 px-4 py-2 font-bold text-white transition hover:bg-purple-700 disabled:cursor-not-allowed disabled:bg-purple-800"
				>
					{isLoading ? 'Changing...' : 'Change Password'}
				</button>
			</form>
		</div>
	</div>
</div>