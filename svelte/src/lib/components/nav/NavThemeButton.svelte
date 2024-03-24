<script lang="ts">
    import { onMount } from "svelte";
    import NavButton from "./NavButton.svelte";
    import { MoonOutline, SunOutline } from "flowbite-svelte-icons";
    let isDark: boolean = true;

    onMount(() => {
        isDark = localStorage.getItem("darkMode") === "true";
        updateTheme();
    });

    function toggleTheme() {
        console.log("toggle theme");
        isDark = !isDark;
        localStorage.setItem("darkMode", isDark);
        updateTheme();
    }

    function updateTheme() {
        if (isDark) {
            document.body.classList.add("dark");
        } else {
            document.body.classList.remove("dark");
        }
    }
</script>

<NavButton
    title="Toggle Theme"
    icon={isDark ? SunOutline : MoonOutline}
    onClick={toggleTheme}
/>
