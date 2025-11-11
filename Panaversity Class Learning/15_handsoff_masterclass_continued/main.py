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


spanish_agent = Agent(
    name="Spanish Assistant",
    instructions="You translate the user's input into Spanish.",
    handoff_description="An english to Spanish translator.",
    model=llm
)
french_agent = Agent(
    name="French Assistant",
    instructions="You translate the user's input into French.",
    handoff_description="An english to French translator.",
    model=llm
)
urdu_agent = Agent(
    name="Urdu Assistant",
    instructions="You translate the user's input into Urdu.",
    handoff_description="An english to Urdu translator.",
    model=llm
)

@dataclass
class HandoffDetail:
    agent_name: str


# agent_context = HandoffDetail(agent_name="")
# def log_handoff_detail(ctx: RunContextWrapper):
    # print(f"Handoff Detail Logged")

def log_handoff_spanish(ctx: RunContextWrapper):
    print(f"Handoff to Spanish Agent Logged")

def log_handoff_french(ctx: RunContextWrapper):
    print(f"Handoff to French Agent Logged")

def log_handoff_urdu(ctx: RunContextWrapper):
    print(f"Handoff to Urdu Agent Logged")

main_agent = Agent(
    name="Main Agent", 
    instructions="You are a helpful assistant that can hand off tasks to specialized agents when needed.",
    # handoffs=[spanish_agent, french_agent, urdu_agent], #BASIC WAY TO ADD HANDOFFS,


    #ADVANCED WAY TO ADD HANDOFFS
    handoffs = [
        handoff(
            agent=spanish_agent,
            tool_description_override="translate_to_spanish",
            on_handoff=log_handoff_spanish
            ), 
        handoff(
            agent=french_agent,
            tool_description_override="translate_to_french",
            on_handoff=log_handoff_french
        ), 
        handoff(
            agent=urdu_agent,
            tool_description_override="translate_to_urdu",
            on_handoff=log_handoff_urdu
        )
    ], 
    model=llm)



# Run a query
result: RunResult = Runner.run_sync(
    starting_agent=main_agent,
    input="Translate 'what is your name?' into urdu.",
    
)

print(result.last_agent.name, "\n")
print(result.final_output)