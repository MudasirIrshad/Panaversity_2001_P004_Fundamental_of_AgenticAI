import asyncio
from dotenv import load_dotenv
import os

from agents import Agent, RunConfig, RunResult, Runner, OpenAIChatCompletionsModel, trace
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent


# Load environment variables
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

# Initialize client
# This is for Google Gemini via the OpenAI API compatibility layer
# client = AsyncOpenAI(
#     api_key=api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )


# This client if for local AI model 
client = AsyncOpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1"
)



llm : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="qwen3-coder:480b-cloud",
    openai_client=client
)
# Define agents

# Run a query
async def main():
    agent = Agent(name="Assistant", instructions="You are a an AI assistant", model=llm)
    with trace("main run"):
        result  = Runner.run_streamed(
            starting_agent=agent,
            input="write a 200 word essay on the benefits of AI",
        )
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())