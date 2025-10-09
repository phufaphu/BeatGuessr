<script lang="ts">
    import type { Toast } from '$lib/toastStore';
    import { CircleCheck, CircleX, Info } from 'lucide-svelte';
    import { slide } from 'svelte/transition';

	const { toast } = $props<{ toast: Toast }>();

	const colorClass = {
		success: 'bg-green-600 text-white',
		error: 'bg-red-600 text-white',
		info: 'bg-blue-600 text-white'
	}[toast.type as 'success' | 'error' | 'info'];

	const IconComponent = {
		success: CircleCheck,
		error: CircleX,
		info: Info
	}[toast.type as 'success' | 'error' | 'info'];
    
</script>

<div in:slide={{ duration: 300, axis: 'x' }} class="flex items-center gap-4 rounded-md p-4 shadow-lg {colorClass}">
	{#if IconComponent}
		<IconComponent class="h-6 w-6" />
	{/if}
	<p>{toast.message}</p>
</div>