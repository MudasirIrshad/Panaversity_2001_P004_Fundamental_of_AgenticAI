from dataclasses import dataclass
from dotenv import load_dotenv
import os

from agents import Agent, RunConfig, RunContextWrapper, RunResult, Runner, OpenAIChatCompletionsModel, handoff
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

math_expert_agent: Agent = Agent(
    name="Math Expert Agent",
    model=llm,
    instructions="You are an AI math expert. Your task is to solve math problems",
    handoff_description="I can solve the given math problem"
)

@dataclass
class user_info:
    name: str

premium_users = ["Mudasir", "Alice", "Bob"]

def test_access(user_context:RunContextWrapper, agent:Agent) -> bool:
    return True if user_context.context.name in premium_users else False

assistant_agent = Agent(
    name="Assistant",
    model=llm,
    handoffs=[handoff(poet_agent, is_enabled=test_access)],
    instructions="you are an AI assistant. Your task is to answer the given question. If user wants a poem, you can ask Poet Agent to write a poem about a given topic. Only premium users can access Poet Agent, simple users must get notified to get premium account to write a poem.",
    )
# Run a query
user_name = input("Enter your name: ")

user_context = user_info(name=user_name)

result: RunResult = Runner.run_sync(
    starting_agent=assistant_agent,
    input="share a poem about Mirza Ghalib",
    context=user_context
)

print(result.last_agent.name)
print(result.final_output)