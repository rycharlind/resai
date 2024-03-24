<script lang="ts">
    import { useChat } from "ai/svelte";
    import ChatBlock from "$lib/components/chat/ChatBlock.svelte";
    import { writable } from "svelte/store";

    import { Input, Button } from "flowbite-svelte";

    let { input, handleSubmit, messages } = useChat({
        api: "/api/chat",
    });

    const inputStore = writable(""); // Initialize the store with an empty string
    $: $input = $inputStore; // Update the store when the input value changes

    import type { PageData } from "./$types";
    export let data: PageData;
    let { session } = data;
    $: ({ session } = data);

    const prompt1 = `
How can I write a Python function using Pandas that will
read in a CSV file, transform it into JSON and
write it back out as a NDJSON file?
`;

    const prompt2 = `
Show me how to write a deep neural network in Python with PyTorch? Explain it step by step.
`;

    const prompt3 = `
List 5 sentences on how AI can help companies analyze
and mange data faster. Provide example use cases for each.
`;

    function handlePromptClick(newInput: string) {
        console.log(newInput);
        inputStore.set(newInput); // Update the store with the new input value
        $input = newInput; // Update the hidden input value
    }
</script>

<div>
    <ul>
        {#each $messages as message}
            <div style="margin-top: 16px">
                <ChatBlock
                    {session}
                    role={message.role}
                    content={message.content}
                />
            </div>
        {/each}
    </ul>
    <form on:submit={handleSubmit} style="margin-top: 16px">
        <div
            class="resai-prompt-grid grid grid-cols-3 gap-4"
            style="margin: 12px 0px"
        >
            <div class="resai-prompt-grid-cell">
                <Button
                    color="alternative"
                    on:click={() => handlePromptClick(prompt1)}
                    >{prompt1}</Button
                >
            </div>
            <div class="resai-prompt-grid-cell">
                <Button
                    color="alternative"
                    on:click={() => handlePromptClick(prompt2)}
                    >{prompt2}</Button
                >
            </div>
            <div class="resai-prompt-grid-cell">
                <Button
                    color="alternative"
                    on:click={() => handlePromptClick(prompt3)}
                    >{prompt3}</Button
                >
            </div>
        </div>
        <input type="hidden" name="prompt" bind:value={$inputStore} />
        <Input
            type="text"
            id="prompt"
            placeholder="Type something ..."
            bind:value={$input}
        />
        <Button type="submit" size="xl" style="width:200px;margin-top: 16px;"
            >Send</Button
        >
    </form>
</div>
