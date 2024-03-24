<script lang="ts">
    import { BellOutline } from "flowbite-svelte-icons";
    import NavButton from "../nav/NavButton.svelte";
    import NavThemeButton from "../nav/NavThemeButton.svelte";
</script>

<div
    class="h-14 absolute left-14 top-0 right-0 border-b border-b-zinc-200 dark:border-b-zinc-700 flex items-center px-6 dark:bg-dark bg-light"
>
    <div></div>
    <div class="flex grow"></div>
    <div class="flex">
        <NavThemeButton />
        <NavButton title="Notifications" icon={BellOutline} />
    </div>
</div>
