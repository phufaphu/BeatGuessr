<script lang="ts">
  import Nav from '../Nav.svelte';
</script>

<div class="min-h-screen bg-gray-900 text-white">
  <Nav />
  <div class="p-8">
    <h1 class="text-4xl font-bold text-cyan-500">Welcome to BeatGuessr!</h1>
    <p class="mt-4 text-lg">This page was rendered by Svelte on the "Home" template.</p>
  </div>
  <form action="/api/guess" method="POST">
    <input type="text" name="guess" placeholder="Enter your guess" class="p-2 rounded" />
    <button type="submit" class="ml-2 p-2 bg-cyan-500 rounded">Submit</button>
  </form>
</div>