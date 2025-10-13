<script lang="ts">
  import api from "$lib/api";
  import { ArrowLeft } from "lucide-svelte";
  import { addToast } from "$lib/toastStore";
  import { goto } from "$app/navigation";

  let oldPassword = $state("");
  let newPassword = $state("");
  let confirmPassword = $state("");

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
      await api.post("/users/me/set-password/", {
        old_password: oldPassword,
        new_password: newPassword,
      });
      successMessage = "Your password has been changed successfully!";
      addToast(successMessage, "success");
      oldPassword = "";
      newPassword = "";
      confirmPassword = "";
      goto("/profile");
    } catch (err: any) {
      if (err.response && err.response.data) {
        error = Object.entries(err.response.data)
          .map(([key, value]) => `${key}: ${value}`)
          .join(" ");
        addToast(error, "error");
      } else {
        error = "An unknown error occurred.";
        addToast(error, "error");
      }
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="w-full max-w-xl glass p-4 md:p-8">
  <a
    href="/profile"
    class="inline-flex items-center gap-2 text-[#5bf3ff] hover:underline transition"
  >
    <ArrowLeft class="h-6 w-6" />
    Back to Profile
  </a>
  <!-- Back to Profile Link -->

  <div class="rounded-lg p-4">
    <h1 class="text-3xl font-bold">Change Password</h1>
    <p class="mt-2 text-gray-400">
      Choose a strong password that you're not using anywhere else.
    </p>

    <form onsubmit={handleChangePassword} class="mt-6 space-y-4">
      <div>
        <label
          for="old_password"
          class="mb-1 block text-sm font-medium text-white/70"
        >
          Current Password
        </label>
        <input
          bind:value={oldPassword}
          id="old_password"
          type="password"
          required
          class="w-full rounded-lg border border-white/20 p-2 text-white placeholder-white/20 focus:border-[#00c4e5] focus:outline-none focus:ring-[#00c4e5]"
        />
      </div>
      <div>
        <label
          for="new_password"
          class="mb-1 block text-sm font-medium text-white/70"
        >
          New Password
        </label>
        <input
          bind:value={newPassword}
          id="new_password"
          type="password"
          required
          minlength="8"
          class="w-full rounded-lg border border-white/20 p-2 text-white placeholder-white/20 focus:border-[#00c4e5] focus:outline-none focus:ring-[#00c4e5]"
        />
      </div>
      <div>
        <label
          for="confirm_password"
          class="mb-1 block text-sm font-medium text-white/70"
        >
          Confirm New Password
        </label>
        <input
          bind:value={confirmPassword}
          id="confirm_password"
          type="password"
          required
          class="w-full rounded-lg border border-white/20 p-2 text-white placeholder-white/20 focus:border-[#00c4e5] focus:outline-none focus:ring-[#00c4e5]"
        />
      </div>
      <button
        type="submit"
        disabled={isLoading}
        class="w-full mt-1 rounded-md bg-[#A855F7] px-4 py-2 font-bold text-white transition hover:bg-[#A855F7]/80 disabled:cursor-not-allowed disabled:bg-[#A855F7]/60"
      >
        {isLoading ? "Changing..." : "Change Password"}
      </button>
    </form>
  </div>
</div>
