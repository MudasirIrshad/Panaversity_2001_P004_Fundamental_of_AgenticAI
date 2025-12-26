from dotenv import load_dotenv
import os
import chainlit as cl
from agents import Agent, RunConfig, RunResult, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI


# Load environment variables
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

# Initialize client

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


llm : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)

agent : Agent = Agent(
    name="Assistant",
    instructions="You are an AI assistant that helps users with their questions.",
    model=llm
)

@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...

    msg = await cl.Message(content="Thinking...").send()

    # Run the agent with the user's message
    result: RunResult = await Runner.run(
        starting_agent=agent,
        input=message.content,
    )

    msg.content = f"AGENT: {result.final_output}"
    await msg.update()