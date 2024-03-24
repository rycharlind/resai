<script lang="ts">
    import { onMount } from "svelte";

    import {
        Alert,
        Button,
        Heading,
        Input,
        Label
    } from "flowbite-svelte";

    import type { PageData } from "../$types";
    export let data: PageData;
    let { supabase, session } = data;
    $: ({ supabase, session } = data);

    import type { ActionData } from "../$types";
    export let form: ActionData;

    let loading = false;
    let firstName: string | null = null;
    let lastName: string | null = null;
    let company: string | null = null;
    let phone: string | null = null;

    async function getProfile() {
        try {
            loading = true;
            const { user } = session;

            const { data, error, status } = await supabase
                .from("user_profiles")
                .select("first_name, last_name, company, phone")
                .eq("id", user.id)
                .single();

            if (error && status !== 406) throw error;

            if (data) {
                firstName = data.first_name;
                lastName = data.last_name;
                company = data.company;
                phone = data.phone;
            }
        } catch (error) {
            if (error instanceof Error) {
                alert(error.message);
            }
        } finally {
            loading = false;
        }
    }

    async function updateProfile() {
        try {
            loading = true;
            const { user } = session;

            const updates = {
                id: user.id,
                first_name: firstName,
                last_name: lastName,
                company: company,
                phone: phone
            };

            let { error } = await supabase.from("user_profiles").upsert(updates);

            if (error) {
                throw error;
            }
        } catch (error) {
            if (error instanceof Error) {
                alert(error.message);
            }
        } finally {
            loading = false;
        }
    }

    onMount(async () => {
        await getProfile();
    });
</script>

<div class="page-body">
    <div class="page-content">
        <Heading
            tag="h1"
            class="mb-4"
            customSize="text-4xl font-extrabold  md:text-5xl lg:text-6xl"
            >Profile</Heading
        >

        <!-- <Toast color="green">
            <svelte:fragment slot="icon">
                <Icon name="check-circle-solid" class="w-5 h-5" />
                <span class="sr-only">Check icon</span>
            </svelte:fragment>
            Profile updated.
        </Toast> -->

        <form on:submit|preventDefault={updateProfile} style="margin:16px 0px">
            {#if form?.invalid}
                <Alert border color="red">
                    <span class="font-medium">Woops, </span>
                    {form?.message}
                </Alert>
            {/if}

            <div style="margin: 16px 0px">
                <div class="grid gap-6 mb-6 md:grid-cols-2">
                    <div>
                        <Label for="firstName" class="mb-2">First name</Label>
                        <Input type="text" id="firstName" bind:value={firstName} />
                    </div>
                    <div>
                        <Label for="lastName" class="mb-2">Last name</Label>
                        <Input type="text" id="lastName" bind:value={lastName}/>
                    </div>
                    <div>
                        <Label for="company" class="mb-2"
                            >Company (optional)</Label
                        >
                        <Input type="text" id="company" bind:value={company} />
                    </div>
                    <div>
                        <Label for="phone" class="mb-2"
                            >Phone number (optional)</Label
                        >
                        <Input type="tel" id="phone" bind:value={phone} />
                    </div>
                </div>
                <div class="mb-6">
                    <Label for="email" class="mb-2">Email address</Label>
                    <Input
                        type="email"
                        id="email"
                        required
                        name="email"
                        disabled
                        bind:value={session.user.email}
                    />
                </div>
                <Button type="submit" size="xl" style="width:200px" disabled={loading}
                    >{loading ? 'Saving ...' : 'Update profile'}</Button
                >
            </div>
        </form>
    </div>
</div>
