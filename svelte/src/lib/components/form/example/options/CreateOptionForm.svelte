<script lang="ts">
    import { Label, Button, Input, Tooltip } from "flowbite-svelte";

    const formElements = [
        {
            type: "input",
            id: "tradeName",
            name: "tradeName",
            label: "Trade Date",
            placeholder: "Your trade date",
            tooltip: "The date the trade was executed",
            required: true,
        },
        {
            type: "input",
            id: "expirationDate",
            name: "expirationDate",
            label: "Expiration Date",
            placeholder: "Your expiration date",
            tooltip: "The date the option expires",
            required: true,
        },
        {
            type: "select",
            id: "optionType",
            name: "optionType",
            label: "Option Type",
            required: true,
            tooltip: "The type of option",
            selectOptions: [
                { value: "call", label: "Call" },
                { value: "put", label: "Put" },
            ],
        },
    ];
</script>

<form action="?/form" method="POST" class="m-4">
    <div class="grid grid-cols-2 gap-4">
        {#each formElements as item, index}
            <div class="mb-6">
                {#if item.type === "select"}
                    <Label for={item.name} class="mb-2">{item.label}</Label>
                    <select
                        id={item.name}
                        name={item.name}
                        required={item.required}
                    >
                        {#each item.selectOptions as option}
                            <option value={option.value}>{option.label}</option>
                        {/each}
                    </select>
                    <Tooltip>{item.tooltip}</Tooltip>
                {:else if item.type === "input"}
                    <Label for={item.name} class="mb-2">{item.label}</Label>
                    <Input id={item.id} placeholder={item.placeholder} />
                    <Tooltip>{item.tooltip}</Tooltip>
                {/if}
                <!-- Add more conditions for other types -->
            </div>
        {/each}
    </div>
    <div class="flex justify-between">
        <Button type="submit" size="xl" class="w-48">Submit</Button>
    </div>
</form>
