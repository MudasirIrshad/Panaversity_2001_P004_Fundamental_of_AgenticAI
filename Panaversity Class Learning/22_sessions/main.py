from dotenv import load_dotenv
import os

from agents import Agent, RunResult, Runner, OpenAIChatCompletionsModel, trace, SQLiteSession
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

# Define session storage
session_storage = SQLiteSession("user_123","conversation_123.db")

# Define agents
agent = Agent(name="Assistant", instructions="You are a an AI assistant", model=llm)

# Run a query
with trace("Session workflow"):

    while True:
        prompt = input("Enter your question (or 'exit' to quit): ")
        if prompt.lower() == 'exit':
            break

        result: RunResult = Runner.run_sync(
            starting_agent=agent,
            input=prompt,
            session=session_storage
        )
        print(result.final_output)