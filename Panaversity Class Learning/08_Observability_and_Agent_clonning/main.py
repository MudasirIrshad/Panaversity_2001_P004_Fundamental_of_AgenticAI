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


@function_tool
def add_number(a:int, b:int)->int:
    """Show all the steps needed to add 2 numbers"""
    return a+b
@function_tool
def sub_number(a:int, b:int)->int:
    """Show all the steps needed to subtract 2 numbers"""
    return a-b

def get_instructions(context: RunContextWrapper, agent: Agent):
    return "Hi there, you are a Math assistant to solve basic questions using only tools."
# Define agents
agent = Agent(
    name="My Assistant", 
    instructions=get_instructions, 
    model=llm, tools=[add_number,sub_number])

agent.clone()

with trace("Math Trace"):
    result: RunResult = Runner.run_sync(
        agent,
        input="what is the answer if we add 9 and 5, what is the answer if we 9 minus 5, both with steps?",
    )

    print(result.final_output)

    # result: RunResult = Runner.run_sync(
    #     math_agent,
    #     input="what is the answer if we subtract 9 and 5 with steps?",
    # )

    # print(result.final_output)