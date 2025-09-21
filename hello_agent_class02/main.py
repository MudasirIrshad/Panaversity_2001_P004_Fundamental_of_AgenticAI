from dotenv import load_dotenv
import os

from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

client = AsyncOpenAI(
    api_key= api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

agent: Agent = Agent(name="Assistant", instructions="You are a motivational assistant", model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client))

result = Runner.run_sync(agent, "why learn math for AI Agents?")

print(result.final_output)