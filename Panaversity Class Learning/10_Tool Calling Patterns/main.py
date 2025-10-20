
from dotenv import load_dotenv 
import os

from agents import Agent, RunConfig, RunContextWrapper, RunResult, Runner, OpenAIChatCompletionsModel, function_tool, trace
from openai import AsyncOpenAI


# Load environment variables
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


llm: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)


agent = Agent(
    name="My Assistant", 
    instructions="You are my assistant", 
    model=llm
    )
result: RunResult = Runner.run_sync(
    agent,
    input="what is the answer if we add 9 and 5, what is the answer if we 9 minus 5, both with steps?"
    )

print(result.final_output)

