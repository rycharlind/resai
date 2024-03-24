<script>
    import { Banner, Skeleton, ImagePlaceholder } from "flowbite-svelte";
</script>

<Banner id="default-banner">
    <p
        class="flex items-center text-sm font-normal text-gray-500 dark:text-gray-400"
    >
        <span
            class="inline-flex p-1 mr-3 bg-gray-200 rounded-full dark:bg-gray-600"
        >
            <span class="sr-only">Light bulb</span>
        </span>
        <span>
            Currently in <strong>PRIVATE BETA</strong>.
            <a
                href="/register"
                class="inline font-medium text-primary-600 underline dark:text-primary-500 underline-offset-2 decoration-600 dark:decoration-500 decoration-solid hover:no-underline"
            >
                Register
            </a>
            to request early access.
        </span>
    </p>
</Banner>
