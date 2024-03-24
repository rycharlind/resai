import { AuthApiError } from "@supabase/supabase-js"
import { fail } from "@sveltejs/kit"
import type { Actions } from "./$types"

export const actions: Actions = {
    register: async ({ request, locals }) => {
        const body = await request.formData();
        const email = body.get('email');
        const password = body.get('password');
        const firstName = body.get('firstName');
        const lastName = body.get('lastName');
        const company = body.get('company');
        const phone = body.get('phone');

        const { data, error: err } = await locals.supabase.auth.signUp({
            email: email as string,
            password: password as string,
        })

        if (err) {
            console.log(err);
            if (err instanceof AuthApiError) {
                if (err.status === 400) {
                    return fail(400, { invalid: true, message: err.message })
                }
                if (err.status === 422) {
                    return fail(422, { invalid: true, message: err.message })
                }
            }

            return fail(500, {
                invalid: true,
                message: "Server error. Try again later.",
            })
        }

        console.log(data);

        if (data.user) {

            const { error } = await locals.supabase
                .from('profiles')
                .insert({ id: data.user.id, first_name: firstName, last_name: lastName, company: company, phone: phone })

            if (error) {
                console.log(error);
                return fail(500, { invalid: true, message: 'Something broke.' })
            }
        }

        return {
            status: 201,
            data: data
        }
    },
}