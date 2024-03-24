<script lang="ts">
    import Highlight from "svelte-highlight";
    import { initializeHighlighter } from "./highlighter-init";
    import defaultLanguageModule from "svelte-highlight/languages/bash";
    import { darkMode } from "../../../stores/darkMode";

    // Check outs themes here: https://highlightjs.org/demo
    import codeThemeDark from "svelte-highlight/styles/atom-one-dark";
    import codeThemeLight from "svelte-highlight/styles/atom-one-light";

    let codeTheme = codeThemeDark;

    let languageModule: any = defaultLanguageModule;

    export let text: string;
    export let lang: string;

    $: {
        if (lang) {
            initializeHighlighter(lang).then((module) => {
                languageModule = module;
            });
        }
    }

    import { onDestroy } from "svelte";

    let isDarkMode;

    // Subscribe to changes in the store
    const unsubscribeDarkMode = darkMode.subscribe((value) => {
        isDarkMode = value;
        if (isDarkMode) {
            codeTheme = codeThemeDark
        } else {
            codeTheme = codeThemeLight
        }
    });

    onDestroy(() => {
        unsubscribeDarkMode();
    });
</script>

<svelte:head>
    {@html codeTheme}
</svelte:head>

<div class="my-6 bg-gray-200 dark:bg-gray-600 rounded-md">
    <div
        class="flex flex-wrap items-center justify-between h-12 text-dark dark:text-light"
    >
        <div class="ml-4 text-sm">{lang}</div>
        <button class="h-full w-20 text-sm">Copy</button>
    </div>
    {#if languageModule}
        <Highlight language={languageModule} code={text} />
    {:else}
        <p>Loading ...</p>
    {/if}
</div>

