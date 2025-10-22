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


# @function_tool
# def get_message()->str:
#     """Check and returns unread whastapp messages and share them"""
#     return "You have 1 message: 'Create a promotional facebook post and whatsapp message'"



# whatsapp_message: Agent = Agent(
#     name="Whatsapp message Agent",
#     instructions=(
#         "You are a WhatsApp message monitoring and task-delegating agent.\n\n"
#         "Use the 'get_message' tool to check for new messages.\n"
#         "Then decide what to do:\n"
#         "1. If the message requests a **Facebook promotional post**, "
#         "handoff to the **Facebook Content Writer Agent**.\n"
#         "2. If the message requests a **WhatsApp promotional message**, "
#         "handoff to the **WhatsApp Promotional Message Writer Agent**.\n"
#         "3. If both are requested, handle both via the appropriate handoffs.\n\n"
#         "Be explicit in your reasoning when deciding which handoff to use."
#     ),
#     model=llm,
#     tools=[get_message],
#     handoff_description="Checks WhatsApp messages and delegates to content writers."
# )
# facebook_content_wirter: Agent = Agent(
#     name="Facebook Content Writer Agent",
#     instructions="write a facebook promotional content given by whatsapp_message",
#     model=llm,
#     handoffs=[whatsapp_message]
# )
# whatsapp_promotional_wirter: Agent = Agent(
#     name="Whatsapp promotional message Writer Agent",
#     instructions="write a whatsapp promotional message given by whatsapp_message",
#     model=llm,
#     handoffs=[whatsapp_message]
# )

# whatsapp_message.handoffs = [facebook_content_wirter, whatsapp_promotional_wirter]


# # Its upon us to use Orchestrator Agent or do handsoff directly
# # orchestrator_agent: Agent = Agent(
# #     name="Orchestrator Agent",
# #     instructions="You are my assistant",
# #     model=llm,
# #     handoffs=[whatsapp_message, facebook_content_wirter]
# # )




# result = Runner.run_sync(
#     # input="""Salam""",
#     input="""
#     I am making a product named ShoeBurner:
    
#     2. Write a short facebook post content for promotion. and need a whatsapp message too for that.
#     """,
#     starting_agent=whatsapp_message
# )

# print(result.final_output)
# print("\n\n\n",result.last_agent.name)



outline_builder = Agent(
    name="Outline Builder",
    instructions=(
        "Given a particular programming topic, your job is to help come up with a tutorial.You will do that by crafting an outline"
        "After making the outline hand it to the tutorial generator agent."
    )
)
tutorial_generator = Agent(
    name="Tutorial Generator",
    instructions=(
        "Given a programming topic and an outline, your job is to generate code snippets for each section of the outline."
        "format the tutorial in markdown using a mix of text for explanation and code snippets for examples."
        "Where it makes sense, include comments in the code snippets to further explain the code."
    ),
    tools=[]
)