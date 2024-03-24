let languageModule: any;

async function loadLanguage(lang: any) {
    if (lang === 'python') {
        languageModule = await import('svelte-highlight/languages/python');
    } else if (lang === 'sql') {
        languageModule = await import('svelte-highlight/languages/sql');
    } else if (lang === 'javascript') {
        languageModule = await import('svelte-highlight/languages/javascript');
    } else if (lang === 'java') {
        languageModule = await import('svelte-highlight/languages/java');
    } else if (lang === 'cpp') {
        languageModule = await import('svelte-highlight/languages/cpp');
    } else if (lang === 'go') {
        languageModule = await import('svelte-highlight/languages/go');
    } else if (lang === 'rust') {
        languageModule = await import('svelte-highlight/languages/rust');
    } else {
        languageModule = await import('svelte-highlight/languages/shell');
    }

    return languageModule.default;
}

export function initializeHighlighter(lang: any) {
    return loadLanguage(lang);
}