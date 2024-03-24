<script lang="ts">
	import { Heading, P, Button } from "flowbite-svelte";
	import type { PageData } from "./$types";

	export let data: PageData;
	let { session, supabase } = data;
	$: ({ session, supabase } = data);

	function handleSignOut() {
        supabase.auth.signOut();
    }
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="ResAI" />
</svelte:head>

<div class="text-center" style="padding: 200px 0px">
	<Heading
		tag="h1"
		class="mb-4"
		customSize="text-4xl font-extrabold md:text-5xl lg:text-6xl"
		>AI powered Research</Heading
	>

	<P class="mb-6 text-lg lg:text-xl sm:px-16 xl:px-48 dark:text-gray-400 text-center"
		>Your Personalized AI Assistant for Efficient Research.</P
	>
	<Button on:click={handleSignOut}>
		Sign Out
	</Button>
</div>

<style>
</style>
