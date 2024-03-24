<script lang="ts">
    import { Avatar } from "flowbite-svelte";
    import SvelteMarkdown from "svelte-markdown";
    import CodeBlock from "$lib/components/markdown/CodeBlock.svelte";
    import CodeSpan from "$lib/components/markdown/CodeSpan.svelte";

    // todo: use the profile pic from the user's profile
    import type { Session } from "@supabase/supabase-js";
    export let session: Session | null;

    export let role = "";
    export let content = "";
</script>

<div class="chat-block" style="margin: 8px 0px">
    <div class="flex">
        <Avatar
            size="sm"
            style="margin-right: 8px;"
            src={role === "user"
                ? "https://lh3.googleusercontent.com/a/AAcHTte6dv2uLGkYDXIv1QXogx0ZqKiRc4U-BoIe73xb2xe5vP0=s288-c-no"
                : "https://irp.cdn-website.com/df735c7c/dms3rep/multi/MicrosoftTeams-image+%28123%29.png"}
        />
        <span
            class="text-md text-gray-800 dark:text-gray-400"
            style="padding: 0px 16px"
        >
            <SvelteMarkdown
                source={content}
                renderers={{ code: CodeBlock, codespan: CodeSpan }}
            />
        </span>
    </div>
</div>
