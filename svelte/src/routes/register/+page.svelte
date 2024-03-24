<script lang="ts">
    import {
        Input,
        Label,
        Helper,
        Button,
        Checkbox,
        A,
        Heading,
        Card,
        Alert,
    } from "flowbite-svelte";
    import { Icon } from "flowbite-svelte-icons";

    let showPassword = false;

    import type { ActionData } from "./$types";
    export let form: ActionData;
</script>

<div class="page-body">
    <div class="page-content">
        <Heading
            tag="h1"
            class="mb-4"
            customSize="text-4xl font-extrabold  md:text-5xl lg:text-6xl"
            >Register</Heading
        >

        {#if form?.data && form?.status == 201}
            <Card style="max-width: 600px; margin-top:32px">
                <h5
                    class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white"
                >
                    Thank you for registering!
                </h5>
                <p
                    class="mb-3 font-normal text-gray-700 dark:text-gray-400 leading-tight"
                >
                    A confirmation email has been sent. Please check your inbox.
                    We will review your application and get back to you as soon
                    as possible.
                </p>
                <Button class="w-fit" href="/login">
                    Sign In <Icon
                        name="arrow-right-outline"
                        class="w-3.5 h-3.5 ml-2 text-white"
                    />
                </Button>
            </Card>
        {/if}

        {#if !form?.data}
            <form action="?/register" method="POST" style="margin:16px 0px">
                {#if form?.invalid}
                    <Alert border color="red">
                        <Icon
                            name="info-circle-solid"
                            slot="icon"
                            class="w-4 h-4"
                        />
                        <span class="font-medium">Woops, </span>
                        {form?.message}
                    </Alert>
                {/if}

                <div style="margin: 16px 0px">
                    <div class="grid gap-6 mb-6 md:grid-cols-2">
                        <div>
                            <Label for="firstName" class="mb-2"
                                >First name</Label
                            >
                            <Input
                                type="text"
                                id="firstName"
                                name="firstName"
                            />
                        </div>
                        <div>
                            <Label for="lastName" class="mb-2">Last name</Label>
                            <Input type="text" id="lastName" name="lastName" />
                        </div>
                        <div>
                            <Label for="company" class="mb-2"
                                >Company (optional)</Label
                            >
                            <Input type="text" id="company" name="company" />
                        </div>
                        <div>
                            <Label for="phone" class="mb-2"
                                >Phone number (optional)</Label
                            >
                            <Input
                                type="tel"
                                id="phone"
                                name="phone"
                            />
                        </div>
                    </div>
                    <div class="mb-6">
                        <Label for="email" class="mb-2">Email address</Label>
                        <Input type="email" id="email" required name="email" />
                    </div>
                    <div class="mb-6">
                        <Label for="show-password" class="mb-2"
                            >Password</Label
                        >
                        <Input
                            id="show-password"
                            type={showPassword ? "text" : "password"}
                            placeholder="***********"
                            size="lg"
                            name="password"
                        >
                            <button
                                slot="left"
                                on:click={() => (showPassword = !showPassword)}
                                class="pointer-events-auto"
                                tabindex="-1"
                                type="button"
                            >
                                {#if showPassword}
                                    <Icon
                                        name="eye-outline"
                                        class="w-6 h-6"
                                        tabindex="-1"
                                    />
                                {:else}
                                    <Icon
                                        name="eye-slash-outline"
                                        class="w-6 h-6"
                                        tabindex="-1"
                                    />
                                {/if}
                            </button>
                        </Input>
                    </div>
                    <Checkbox class="mb-6 space-x-1" required>
                        I agree with the <A
                            href="/"
                            class="text-primary-700 dark:text-primary-600 hover:underline"
                            >terms and conditions</A
                        >.
                    </Checkbox>
                    <Button type="submit" size="xl" style="width:200px"
                        >Create</Button
                    >
                </div>
            </form>
        {/if}
    </div>
</div>
