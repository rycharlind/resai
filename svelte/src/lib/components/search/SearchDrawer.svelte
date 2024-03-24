<script lang="ts">
    import { Badge } from "flowbite-svelte";
    import { Drawer, CloseButton, Card } from "flowbite-svelte";
    import { sineIn } from "svelte/easing";
    import {
        searchDrawerHidden,
        selectedSearchItem,
    } from "../../../stores/searchStore";
    import SearchResultsGrid from "./SearchResultsGrid.svelte";

    let transitionParamsRight = {
        x: 320,
        duration: 200,
        easing: sineIn,
    };

    const apiUrl = import.meta.env.VITE_PY_API_URL;

    let searchItem: any;

    let searchResults: any = null;

    let isLoading = false;

    const search = async (
        filePath: String,
        tags: string[],
        content: string,
    ) => {
        console.log("Search with Item");

        try {
            isLoading = true;

            const requestBody = {
                search_text: tags.join(" "),
                file_path: filePath,
                top: 6,
            };

            const response = await fetch(`${apiUrl}/search`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(requestBody),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const respBody = await response.json();
            searchResults = respBody?.data?.value;

            isLoading = false;
        } catch (error: any) {
            console.error(
                "There was a problem with the fetch operation: " +
                    error.message,
            );
            isLoading = false;
        }
    };

    $: {
        searchItem = $selectedSearchItem;

        if (searchItem) {
            search(searchItem.file_path, searchItem.tags, searchItem.content);
        }
    }

    function decodeString(text: string) {
        return decodeURIComponent(text);
    }
</script>

<Drawer
    placement="right"
    transitionType="fly"
    transitionParams={transitionParamsRight}
    bind:hidden={$searchDrawerHidden}
    id="imageDrawer"
    class="w-1/2"
>
    <div class="flex items-center">
        <h5
            id="drawer-label"
            class="inline-flex items-center mb-4 text-base font-semibold text-gray-500 dark:text-gray-400"
        >
            {decodeString(searchItem.title)}
        </h5>
        <CloseButton
            on:click={() => searchDrawerHidden.set(true)}
            class="mb-4 dark:text-white"
        />
    </div>
    <img src={searchItem.file_path} alt={searchItem.title} class="rounded" />
    <div class="my-2">
        {#each searchItem.tags as tag}
            <Badge class="mr-1">{tag}</Badge>
        {/each}
    </div>
    <div class="mt-2 h-40 overflow-y-auto">
        <p class="font-normal text-gray-700 dark:text-gray-400 leading-tight">
            {searchItem.content}
        </p>
    </div>
    <h3>Similar Items:</h3>
    <SearchResultsGrid {searchResults} {isLoading} columns={3} />
</Drawer>
