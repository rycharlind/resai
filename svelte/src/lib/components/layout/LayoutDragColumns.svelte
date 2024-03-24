<script lang="ts">
    import Sidenav from "../sidenav/Sidenav.svelte";
    import SidenavIcons from "../sidenav/SidenavIcons.svelte";

    let dragging = false;
    let startX: number;
    let startWidth: number;
    let column1: Element;
    let column2: HTMLDivElement;

    function dragStart(event: { clientX: number }) {
        dragging = true;
        startX = event.clientX;
        startWidth = parseFloat(getComputedStyle(column1).width);
    }

    function drag(event: { clientX: number }) {
        if (dragging) {
            let newWidth = startWidth + event.clientX - startX;
            column1.style.width = `${newWidth}px`;
            column2.style.width = `calc(100% - ${newWidth}px - 10px)`;
        }
    }

    function dragEnd() {
        dragging = false;
    }
</script>

<div class="grid">
    <div class="column" bind:this={column1}>
        <SidenavIcons />
    </div>
    <div
        class="resizer"
        role="button"
        tabindex="0"
        on:mousedown={dragStart}
    ></div>
    <div
        class="column"
        bind:this={column2}
        style="width: calc(100% - 200px - 10px);"
    >
        <slot />
    </div>
</div>

<svelte:window on:mousemove={drag} on:mouseup={dragEnd} />

<style>
    .grid {
        display: flex;
        width: 100%;
        height: 100vh;
    }

    .column {
        height: 100vh;
        background-color: #f5f5f5;
        width: 50%;
    }

    .resizer {
        width: 5px;
        height: 100vh;
        /* background-color: #ccc; */
        background-color: #fff;
        cursor: ew-resize;
    }
</style>
