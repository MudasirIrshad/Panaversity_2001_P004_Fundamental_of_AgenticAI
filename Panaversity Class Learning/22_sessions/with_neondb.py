from dotenv import load_dotenv
import os

from agents import Agent, RunResult, Runner, OpenAIChatCompletionsModel, trace, SQLiteSession
from openai import AsyncOpenAI
import asyncio
from agents.extensions.memory import SQLAlchemySession


# Load environment variables
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

# Initialize client

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


llm : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)


# Define agents

async def main():
    agent = Agent(name="Assistant", instructions="You are a an AI assistant", model=llm)

    # Create session using database URL
    session = SQLAlchemySession.from_url(
    "user-123",
    url="NEON URL",
    create_tables=True,
    engine_kwargs={
        "connect_args": {
            "ssl": True
            }
        }
    )

    with trace("agent_with_session_with_neon_db"):
        while True:
            prompt = input("what you want to ask? (type 'exit' to break the session): ")
            result = await Runner.run(agent, prompt, session=session)
            print(result.final_output)
            if prompt.lower() == 'exit':
                break


if __name__ == "__main__":
    asyncio.run(main())
