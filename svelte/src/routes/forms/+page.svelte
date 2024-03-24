<script lang="ts">
    import CreateOptionForm from "$lib/components/form/example/options/CreateOptionForm.svelte";
    import { Heading, P } from "flowbite-svelte";
</script>

<Heading
    tag="h1"
    class="mb-4"
    customSize="text-4xl font-extrabold md:text-5xl lg:text-6xl">Forms</Heading
>

<div class="grid grid-cols-2 gap-4">
    <div>
        <Heading
            customSize="text-4xl font-extrabold  md:text-5xl lg:text-6xl"
            >Form Data</Heading
        >
        <CreateOptionForm />
    </div>

    <div>
        <Heading
            tag="h2"
            class="mb-4"
            customSize="text-4xl font-extrabold  md:text-5xl lg:text-6xl"
            >Chat</Heading
        >
    </div>
</div>
