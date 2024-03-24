import OpenAI from 'openai';
import { OpenAIStream, StreamingTextResponse } from 'ai';
import dotenv from 'dotenv';

dotenv.config();

const { OPENAI_API_KEY } = process.env;

// Create an OpenAI API client (that's edge friendly!)
const openai = new OpenAI({
    apiKey: OPENAI_API_KEY,
});

// Set the runtime to edge for best performance
export const config = {
    runtime: 'edge'
};

export async function POST({ request }) {
    const { messages } = await request.json();

    // Always start with a system message
    messages.unshift({
        role: "system",
        content: 'You are an AI assistant. Respond in Markdown format.'
    })

    const response = await openai.chat.completions.create({
        messages: messages,
        model: "gpt-3.5-turbo",
        stream: true,
    });

    const stream = OpenAIStream(response, {
        async onFinal(completion) {
            // Cache the response. Note that this will also cache function calls.
            console.log('Ready to cache the response!');
        },
    });

    return new StreamingTextResponse(stream);
}