from dataclasses import dataclass
from dotenv import load_dotenv
import os

from agents import Agent, ModelSettings, RunConfig, RunResult, Runner, OpenAIChatCompletionsModel, set_default_openai_api, set_default_openai_client, set_tracing_disabled, RunContextWrapper
from openai import AsyncOpenAI
from dataclasses import dataclass

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

llm: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)


# Creating Context Class

@dataclass
class UserInfo:
    tier: str # Free, Pro
    username: str
    user_language: None | str

# Dynamic Instructions
# make a function with parameters of context and the agent isntacne.

def hello_instructions(context: RunContextWrapper, agent: Agent):
    # print("This is the context: \n",context.context)
    # print("\n\nThis is the agent: \n",agent)


    user_tier = context.context.tier
    user_language = context.context.user_language or "en"

    if user_tier == "pro":
        return f"""Your name is {agent.name}. Always reply in simple {user_language}.
        Your tier is {user_tier}. so give me more featuristic toned reply and polite"""
    
    return f"""Your name is {agent.name}. Always reply in simple {user_language}.
    Your tier is {user_tier}. so give me more basic and dull toned reply"""


agent: Agent = Agent(
    name="Math Agent", 
    instructions=hello_instructions, 
    model=llm,
    model_settings=ModelSettings(
        temperature=2.0
    )
    
    )

# Run a query
result: RunResult = Runner.run_sync(
    starting_agent=agent,
    input="Hello how are you man",
    context=UserInfo(tier="free", username="Mudasir Irshad", user_language="Roman Urdu")
)

print(result.final_output)