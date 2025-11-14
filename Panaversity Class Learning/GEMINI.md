Do these things when asked to setup a new project for this repository

1. Create new project
   '''
   uv init <topic_name>
   '''

2. Add a new package
   '''
   uv add openai-agents
   uv add google-genai
   '''

3. Add this boiler code
   '''python
   from dotenv import load_dotenv
   import os

from agents import Agent, RunConfig, RunResult, Runner, OpenAIChatCompletionsModel
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

agent = Agent(name="Assistant", instructions="You are a an AI assistant", model=llm)

# Run a query

result: RunResult = Runner.run_sync(
starting_agent=agent,
input="Why learn math for AI agents?",

)

print(result.final_output)
'''
4. create a GEMINI.md file too in project