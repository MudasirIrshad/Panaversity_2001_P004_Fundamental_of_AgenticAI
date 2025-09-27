from dotenv import load_dotenv
import os

from agents import Agent, RunConfig, RunResult, Runner, OpenAIChatCompletionsModel, set_default_openai_api, set_default_openai_client, set_tracing_disabled
from openai import AsyncOpenAI


# Load environment variables
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

# Initialize client

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


set_tracing_disabled(True)
set_default_openai_api("chat_completions")
set_default_openai_client(client)


# Define agents
math_agent = Agent(name="Assistant", instructions="You are a Math assistant", model="gemini-2.5-flash")


chemistry_agent = Agent(name="Assistant", instructions="You are a Chemistry assistant", model="gemini-2.5-flash")

# Run a query
result: RunResult = Runner.run_sync(
    math_agent,
    input="Why learn math for AI agents?",
    
)

print(result.final_output)