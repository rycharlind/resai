import { writable } from 'svelte/store';

export const searchDrawerHidden = writable(true);
export const selectedSearchItem = writable(null); 