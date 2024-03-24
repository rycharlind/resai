<script lang="ts">
    import { Input, Label, Button, Alert } from "flowbite-svelte";
    import { Heading, P } from "flowbite-svelte";
    import {
        EyeOutline,
        EyeSlashOutline,
        InfoCircleSolid,
    } from "flowbite-svelte-icons";

    let showPassword = false;

    import type { ActionData } from "./$types";
    import Logo from "$lib/components/brand/Logo.svelte";
    export let form: ActionData;
</script>

<div class="flex w-full h-full">
    <div class="flex-1 h-full">
        <div class="flex w-full h-full justify-center items-center">
            <div class="w-1/2">
                <Heading
                    tag="h1"
                    class="mb-4"
                    customSize="text-4xl font-extrabold  md:text-5xl lg:text-6xl"
                    >Login</Heading
                >

                <form action="?/login" method="POST" style="margin:16px 0px">
                    {#if form?.invalid}
                        <Alert color="red" rounded={false} class="border-t-4">
                            <InfoCircleSolid />
                            <span class="font-medium">Whoops!</span>
                            Invalid credentials. Try again.
                        </Alert>
                    {/if}

                    <div style="margin: 16px 0px">
                        <div class="mb-6">
                            <Label for="email" class="mb-2">Email address</Label
                            >
                            <Input
                                type="email"
                                id="email"
                                name="email"
                                placeholder="Enter your email address"
                                required
                            />
                        </div>
                        <div class="mb-6">
                            <Label for="show-password" class="mb-2"
                                >Password</Label
                            >
                            <Input
                                id="password"
                                name="password"
                                type={showPassword ? "text" : "password"}
                                placeholder="Enter your password"
                                size="lg"
                            >
                                <button
                                    slot="right"
                                    on:click={() =>
                                        (showPassword = !showPassword)}
                                    class="pointer-events-auto"
                                    tabindex="-1"
                                    type="button"
                                >
                                    {#if showPassword}
                                        <EyeOutline />
                                    {:else}
                                        <EyeSlashOutline />
                                    {/if}
                                </button>
                            </Input>
                        </div>
                        <div class="flex justify-between">
                            <Button
                                color="primary"
                                type="submit"
                                size="xl"
                                style="width:200px">Login</Button
                            >
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
    <div class="flex-1 h-full">
        <div class="w-full h-full bg-primary-300 flex justify-center items-center">
            <Logo />
        </div>
    </div>
</div>
