from dotenv import load_dotenv
import os

from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from openai import AsyncOpenAI
from tavily import TavilyClient
load_dotenv()


tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))



set_tracing_disabled(True)
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

client = AsyncOpenAI(
    api_key= api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

llm: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client)

@function_tool
def binance_coin_price(question: str):
    """Search the web for the answer only related to binance this may include prediction fo future prices too, if anything else return 'question not acceptable' """
    print("BINANCE COIN PRICE TOOL CALLED")
    res = tavily_client.search(f"{question}")
    return res


@function_tool
def null_response(question: str) ->str:
    """give response 'i only give you insights about binance and future price prediction no other questions are applicable for me' when user ask about questions which are not about digital trading"""
    print("NULL RESPONSE TOOL CALLED")
    return f"{question}"
agent: Agent = Agent(name="Assistant", instructions="use all the tools and send question to required tool than use LLM power to answer the query base on question",model=llm, tools=[binance_coin_price, null_response])

result = Runner.run_sync(starting_agent=agent, input="price of potatos today?")

print(result.final_output)