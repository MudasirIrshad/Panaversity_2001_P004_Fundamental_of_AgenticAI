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

whatsapp_message: Agent = Agent(
    name="Whatsapp message Agent",
    model=llm
)
facebook_content_wirter: Agent = Agent(
    name="Facebook Content Writer Agent",
    model=llm
)


orchestrator_agent: Agent = Agent(
    name="Orchestrator Agent",
    instructions="You are my assistant",
    model=llm,
    handoffs=[whatsapp_message, facebook_content_wirter]
)

result = Runner.run_sync(
    # input="""Salam""",
    input="""
    I am making a product named ShoeBurner:
    
    2. Write a short whatsapp message for promotion.
    """,
    starting_agent=orchestrator_agent
)

print(result.final_output)
print("\n\n\n",result.last_agent.name)

