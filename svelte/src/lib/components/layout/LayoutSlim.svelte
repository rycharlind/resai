<script lang="ts">
    import Header from "$lib/components/header/Header.svelte";
    import Sidenav from "../sidenav/Sidenav.svelte";

    import type { Session, SupabaseClient } from "@supabase/supabase-js";
    export let session: Session | null;
    export let supabase: SupabaseClient;
</script>

<div class="w-full h-full">
    <Header />
    <Sidenav {session} {supabase} />
    <div class="absolute left-14 top-14 bottom-12 right-0 overflow-scroll p-8">
        <slot />    
    </div>
</div>
