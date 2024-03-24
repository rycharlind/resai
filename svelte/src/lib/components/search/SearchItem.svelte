<script lang="ts">
    import { Card, Badge, Tooltip } from "flowbite-svelte";
    import { FileSearchOutline } from "flowbite-svelte-icons";

    export let searchItem: any = null;
    export let onClick: (item: any) => void = () => {};

    function decodeString(text: string) {
        return decodeURIComponent(text);
    }
</script>

<Card img={searchItem.file_path}>
    <div class="text-xl font-bold tracking-tight text-gray-900 dark:text-white truncate text-ellipsis">
        <button
            class="text-left"
            type="button"
            on:click={() => onClick(searchItem)}
        >
            {decodeString(searchItem.title)}
        </button>
        <Tooltip>{decodeString(searchItem.title)}</Tooltip>
    </div>
    <div class="my-2">
        {#each searchItem.tags as tag}
            <Badge class="mr-1">{tag}</Badge>
        {/each}
    </div>
    <div class="mt-2">
        <Badge border color="dark">
            <FileSearchOutline class="w-2.5 h-2.5 me-1.5" />
            {searchItem["@search.score"]}
        </Badge>
    </div>
    <div class="mt-2 h-40 overflow-y-auto">
        {searchItem.content}
    </div>
</Card>

<style>
    .multiline-ellipsis {
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 3;
        overflow: hidden;
        text-overflow: ellipsis;
    }
</style>
