from dotenv import load_dotenv
import os

from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from openai import AsyncOpenAI


set_tracing_disabled(True)
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

client = AsyncOpenAI(
    api_key= api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

llm: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client)

@function_tool
def search_weather(question: str)-> str:
    """Search the weather for the answer"""
    print("WEATHER TOOL CALLED")
    
    return f"Quetta weather is 30C today"


@function_tool
def math_function(question: str) ->str:
    """give answer with proper computation"""
    print("MATH TOOL CALLED")
    return f"{question}"
agent: Agent = Agent(name="Assistant", instructions="use all the tools and send question to required tool than use LLM power to answer the query base on question",model=llm, tools=[search_weather, math_function])

result = Runner.run_sync(starting_agent=agent, input="formula for quadratic equ?")

print(result.final_output)