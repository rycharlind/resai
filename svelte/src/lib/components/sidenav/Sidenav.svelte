<script lang="ts">
    import {
        FolderOutline,
        MessageCaptionOutline,
        ChartLineUpSolid,
        HomeOutline,
        CogOutline,
        UserOutline,
        SearchOutline
    } from "flowbite-svelte-icons";
    
    import { BoxArrowRight, PersonCircle } from "svelte-bootstrap-icons";
    import NavButton from "../nav/NavButton.svelte";
    import NavLink from "../nav/NavLink.svelte";
    import NavBrandButton from "../nav/NavBrandButton.svelte";
    import SidenavSplitter from "./SidenavSplitter.svelte";
    import { page } from "$app/stores";
    import type { Session, SupabaseClient } from "@supabase/supabase-js";
    
    $: activeUrl = $page.url.pathname;

    export let session: Session | null;
    export let supabase: SupabaseClient;

    function handleSignOut() {
        supabase.auth.signOut();
    }
</script>

<div
    class="absolute left-0 top-0 flex flex-col w-14 h-full border-r border-r-zinc-200 dark:border-r-zinc-700 px-2 dark:bg-dark bg-light py-2"
>
    <NavBrandButton />
    <NavLink title="Home" icon={HomeOutline} url="/" />
    <SidenavSplitter />
    <NavLink title="Search" icon={SearchOutline} url="/search" />
    <NavLink title="Storage" icon={FolderOutline} url="/storage" />
    <NavLink title="Chat" icon={MessageCaptionOutline} url="/chat" />
    <NavLink title="Forms" icon={ChartLineUpSolid} url="/forms" />
    <div class="flex grow"></div>
    <NavLink title="Settings" icon={CogOutline} url="/settings" />
    <NavLink title="Me" icon={PersonCircle} url="/account/me" />
    <NavButton title="Sign Out" icon={BoxArrowRight} onClick={handleSignOut} />
</div>
