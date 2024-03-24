<script lang="ts">
  import "../app.postcss";
  import "./styles.css";
  import LayoutSlim from "$lib/components/layout/LayoutSlim.svelte";

  import { onMount } from "svelte";
  import { invalidate } from "$app/navigation";

  import type { PageData } from "./$types";
  export let data: PageData;
  let { supabase, session } = data;
  $: ({ supabase, session } = data);

  onMount(() => {
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((event, _session) => {
      if (_session?.expires_at !== session?.expires_at) {
        invalidate("supabase:auth");
      }
    });

    return () => subscription.unsubscribe();
  });
</script>

{#if session}
  <LayoutSlim {session} {supabase}>
    <slot />
  </LayoutSlim>
{/if}

{#if !session}
  <div class="flex h-full w-full">
    <slot />
  </div>
{/if}
