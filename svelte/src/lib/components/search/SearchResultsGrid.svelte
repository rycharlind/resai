<script lang="ts">
    import {
        searchDrawerHidden,
        selectedSearchItem,
    } from "../../../stores/searchStore";
    import SearchItem from "./SearchItem.svelte";

    export let searchResults: any = null;
    export let isLoading: boolean = false;
    export let columns = 1;

    const selectSearchItem = (searchItem: any) => {
        selectedSearchItem.set(searchItem);
        searchDrawerHidden.set(false);
    };
</script>

<div class="w-full h-full text-dark dark:text-white mt-6">
    {#if !isLoading}
        {#if searchResults}
            <div class={`grid grid-cols-${columns} gap-4`}>
                {#each searchResults as searchItem}
                    <SearchItem {searchItem} onClick={selectSearchItem} />
                {/each}
            </div>
        {:else}
            <p>No data available</p>
        {/if}
    {:else}
        <p>Loading...</p>
    {/if}
</div>
