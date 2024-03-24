<script>
    import {
        Footer,
        FooterCopyright,
        FooterLinkGroup,
        FooterLink,
        FooterBrand,
        FooterIcon,
    } from "flowbite-svelte";
    import FlowbiteLogo from "$lib/images/flowbite-svelte-icon-logo.svg";
</script>

<Footer footerType="logo" class="w-full">
    <div class="sm:flex sm:items-center sm:justify-between">
        <FooterBrand
            href="/"
            src={FlowbiteLogo}
            alt="ResAI"
            name="ResAI"
        />
        <FooterLinkGroup
            ulClass="flex flex-wrap items-center mb-6 text-sm text-gray-500 sm:mb-0 dark:text-gray-400"
        >
            <FooterLink href="/about">About</FooterLink>
            <FooterLink href="/privacy">Privacy Policy</FooterLink>
            <FooterLink href="/">Contact</FooterLink>
        </FooterLinkGroup>
    </div>
    <hr class="my-6 border-gray-200 sm:mx-auto dark:border-gray-700 lg:my-8" />
    <FooterCopyright href="/" by="ResAI" />
</Footer>