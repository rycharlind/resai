import { AuthApiError } from "@supabase/supabase-js"
import { fail, redirect, error } from "@sveltejs/kit"
import type { Actions } from "./$types"

export const actions: Actions = {
    search: async ({ request, locals }) => {
        console.log('search');
        const body = await request.formData();
        const searchText = body.get('searchText');

        console.log(searchText);
    },
}