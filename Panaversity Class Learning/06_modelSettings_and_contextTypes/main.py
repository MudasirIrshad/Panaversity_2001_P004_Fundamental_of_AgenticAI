from dotenv import load_dotenv
import os

from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, ModelSettings, function_tool
from openai import AsyncOpenAI
from openai.types.shared import Reasoning


set_tracing_disabled(True)
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

client = AsyncOpenAI(
    api_key= api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


@function_tool
def get_weather(city: str)->str:
    """You are an weather fetching tool for city"""
    return f"weather in city {city} is very good."

llm: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client)

agent: Agent = Agent(name="Assistant", instructions="You are a motivational assistant", 
tools=[get_weather],
model=llm, model_settings=ModelSettings(
    # temperature=0.7,
    # top_p=1,
    # reasoning = Reasoning(
    #     generate_summary="concise",
    #     summary="concise"
    # )
    tool_choice="required" # ["auto", "required", "none"]
))

result = Runner.run_sync(agent, "Quetta?")

print(result.final_output)