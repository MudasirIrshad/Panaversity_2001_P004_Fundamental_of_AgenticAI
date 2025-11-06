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
poet_agent = Agent(
    name="Poet Agent", 
    instructions="You are an AI poet. Your task is to write poem about a given topic", 
    model=llm,
    handoff_description="I can tell you a poem about the given topic"
    )

assistant_agent = Agent(
    name="Assistant",
    model=llm,
    handoffs=[poet_agent],
    instructions="you are an AI assistant. Your task is to answer the given question. If uer wants a poem, you can ask Poet Agent to write a poem about a given topic"
    )

# Run a query
result: RunResult = Runner.run_sync(
    starting_agent=assistant_agent,
    input="Write a poem about LM Arena the AI models",
    
)

print(result.last_agent.name)
print(result.final_output)