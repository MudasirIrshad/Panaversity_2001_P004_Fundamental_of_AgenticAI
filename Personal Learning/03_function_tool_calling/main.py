from dotenv import load_dotenv
import os
import requests
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, ModelSettings, function_tool
from openai.types.responses import ResponseTextDeltaEvent
from openai import AsyncOpenAI


load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

client = AsyncOpenAI(
    api_key= api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

llm: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    openai_client=client, model="gemini-2.5-flash"
)


@function_tool
def get_weather(city: str) -> str:
    print("WEATHER TOOL CALLED")
    api_key = os.getenv("OPENWEATHER_API_KEY")  # Get a real key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    resp = requests.get(url).json()
    
    if resp.get("cod") != 200:
        return f"Could not fetch weather for {city}."
    
    temp = resp["main"]["temp"]
    desc = resp["weather"][0]["description"]
    return f"The current temperature in {city} is {temp}°C with {desc}."


@function_tool
def get_famous_plaes(city:str)->str:
    print("GET FAMOUS PLACES TOOL CALLED")
    return f"You are a Travel broadcasting assistant, and you need to search best places within {city}"



agent: Agent = Agent(name="AI Assistant", instructions="You are AI assistant and choose tools based on user query.", model=llm, tools=[get_weather, get_famous_plaes])

run_cfg = RunConfig(
    model_settings=ModelSettings(temperature=0.3)
)

res = Runner.run_sync(agent, input("What you want to ask? "), run_config=run_cfg)

print(res.final_output)