import OpenAI from 'openai';
import { OpenAIStream, StreamingTextResponse } from 'ai';
import dotenv from 'dotenv';
import { json } from '@sveltejs/kit';

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

    const assistantName = "Math Tutor";

    const assistant = await openai.beta.assistants.create({
        name: assistantName,
        instructions: "You are a personal math tutor. Write and run code to answer math questions.",
        tools: [{ type: "code_interpreter" }],
        model: "gpt-4-1106-preview"
    });

    const thread = await openai.beta.threads.create({});

    const message = await openai.beta.threads.messages.create(
        thread.id,
        {
            role: "user",
            content: "I need to solve the equation `3x + 11 = 14`. Can you help me?"
        }
    );

    console.log(message);

    const run = await openai.beta.threads.runs.create(
        thread.id,
        {
            assistant_id: assistant.id,
            instructions: "Please address the user as Jane Doe. The user has a premium account."
        }
    );

    const run2 = await openai.beta.threads.runs.retrieve(
        thread.id,
        run.id
    );

    const messages2 = await openai.beta.threads.messages.list(
        thread.id
    );

    return json({ "assistant": assistantName, "messages": messages2 });
}