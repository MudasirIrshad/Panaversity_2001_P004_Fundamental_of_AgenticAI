from dataclasses import dataclass
from dotenv import load_dotenv
import os

from agents import Agent, RunContextWrapper, RunResult, Runner, OpenAIChatCompletionsModel, StopAtTools , function_tool
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


# @function_tool
# def add_numbers(a, b):
#     ""
#     print("Add two number tool called")
#     return a+b
# @function_tool
# def sub_numbers(a, b):
#     ""
#     print("Subtract Tool")
#     return a-b
# # Define agents





# agent = Agent(
#     name="Assistant",
#     instructions="You are a Math assistant, which answer math queries and give answer with a joke always",
#     tools=[add_numbers, sub_numbers], 
#     model=llm,
#     tool_use_behavior="stop_on_first_tool" #Will call tools but give only first tool answer.
#     # tool_use_behavior=StopAtTools(stop_at_tool_names=["sub_numbers"]) #Stops on specific tool
#     )


# # Run a query
# result: RunResult = Runner.run_sync(
    
#     starting_agent=agent,
#     input="sum 1 from 5, sub 5 and 29",
#     max_turns=3
    
# )

# print(result.final_output)


# Example 2
@dataclass
class user_info:
    is_study_session: bool


def check_boolean(user_context: RunContextWrapper[user_info], agent: Agent)->bool: 
    return not user_context.context.is_study_session


@function_tool(is_enabled=check_boolean) # type: ignore
def search_google(query: str)->str:
    print("Google Search TOOL")
    return f"Searching google for query: {query}"

# is_enabled: bool | ((RunContextWrapper[Any], AgentBase[Any]) -> MaybeAwaitable[bool]) = True

agent: Agent = Agent(
    name="Study Agent",
    model=llm,
    tools=[search_google]
)

user_context = user_info(is_study_session=False)

runner = Runner.run_sync(
    starting_agent=agent,
    input="Search google for Who is Obama?",
    context=user_context
)

print(runner.final_output)