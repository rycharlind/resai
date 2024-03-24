import { redirect } from '@sveltejs/kit'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async ({ url, locals: { getSession }, depends }) => {
    depends('supabase:auth') // This is required in order the logout to work.

    const session = await getSession()

    if (!session) {
        throw redirect(303, '/login')
    }

    return { url: url.origin }
}