import { AuthApiError } from "@supabase/supabase-js"
import { fail } from "@sveltejs/kit"
import type { Actions } from "../$types"

export const actions: Actions = {
    register: async ({ request, locals }) => {
        const body = await request.formData();
        const firstName = body.get('firstName');
        const lastName = body.get('lastName');

        return {
            status: 201,
            statusText: 'Created'
        }
    },
}