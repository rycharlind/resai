<script lang="ts">
    import { Tooltip } from "flowbite-svelte";
    export let title: string = ""
    export let icon: any;
    export let onClick: any = () => {};
</script>

<button
    class="group h-10 w-10 flex items-center justify-center hover:bg-dark-transparent rounded-lg"
    on:click={onClick}
>
    <svelte:component
        this={icon}
        class="w-4 h-4 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
    />
    <Tooltip placement="right" class="z-10">{title}</Tooltip>
</button>
