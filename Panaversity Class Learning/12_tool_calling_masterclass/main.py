from dotenv import load_dotenv
import os

from agents import Agent, RunResult, Runner, OpenAIChatCompletionsModel 
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
# Define agents
math_agent = Agent(name="Assistant", instructions="You are a Math assistant", model=llm)


chemistry_agent = Agent(name="Assistant", instructions="You are a Chemistry assistant", model=llm)

# Run a query
result: RunResult = Runner.run_sync(
    math_agent,
    input="Why learn math for AI agents?",
    
)

print(result.final_output)