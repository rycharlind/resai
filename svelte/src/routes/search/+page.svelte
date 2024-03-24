<script lang="ts">
    import { onMount } from "svelte";
    import { Input, Button, CloseButton, Spinner } from "flowbite-svelte";
    import { Heading } from "flowbite-svelte";

    import SearchDrawer from "$lib/components/search/SearchDrawer.svelte";
    import SearchResultsGrid from "$lib/components/search/SearchResultsGrid.svelte";

    const apiUrl = import.meta.env.VITE_PY_API_URL;

    let searchResults: any = null;
    let searchText = "";
    let isLoading: boolean = false;

    onMount(() => {
        search(searchText, "");
    });

    const search = async (searchText: string, filePath: String) => {
        console.log("Search");

        try {
            isLoading = true;
            const response = await fetch(`${apiUrl}/search`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    search_text: searchText,
                    file_path: filePath
                }),
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const respBody = await response.json();
            console.log("Response Body:");
            console.log(respBody);
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

    const submitSearch = async (event: any) => {
        event.preventDefault();
        search(searchText, "");
    };

    const clearSearch = async (event: any) => {
        event.preventDefault();
        searchText = "";
        search(searchText, "");
    };
</script>

<div class="w-full h-full">
    <Heading level="1" class="mb-4">Search</Heading>

    <form on:submit={submitSearch}>
        <div>
            <Input
                bind:value={searchText}
                type="text"
                id="searchText"
                name="searchText"
                placeholder="Search Text"
            >
                <CloseButton slot="right" on:click={clearSearch} />
            </Input>
            <div class="my-4"></div>
            <Button type="submit" size="xl" disabled={isLoading}>
                {#if isLoading}
                    <Spinner class="me-3" size="4" color="white" />
                {/if}
                <span>Search</span>
            </Button>
        </div>
    </form>

    <SearchResultsGrid {searchResults} {isLoading} columns={4} />
    <SearchDrawer />
</div>
