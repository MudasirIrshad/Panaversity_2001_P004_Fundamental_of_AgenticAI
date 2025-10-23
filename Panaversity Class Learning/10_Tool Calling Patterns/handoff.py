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


# 2 DIFFERENT AGENT EXAMPLE
# tutorial_generator = Agent(
#     name="Tutorial Generator",
#     instructions=(
#         "Given a programming topic and an outline, your job is to generate code snippets for each section of the outline."
#         "format the tutorial in markdown using a mix of text for explanation and code snippets for examples."
#         "Where it makes sense, include comments in the code snippets to further explain the code."
#         "After making the tutorial hand it to the outline builder agent."
#     ),
#     tools=[],
#     model=llm
# )


# outline_builder = Agent(
#     name="Outline Builder",
#     instructions=(
#         "Given a particular programming topic, your job is to help come up with a tutorial.You will do that by crafting an outline"
#         "After making the outline hand it to the tutorial generator agent."
#         "After handing to the tutorial generator, the tutorial generator give back its response to you and you have to craft ending outline for that."
#         "After receiving the tutorial back, summarize it briefly as a final conclusion and return that as the final output."
#     ),
#     handoffs=[tutorial_generator],
#     model=llm
# )

# tutorial_generator.handoffs = [outline_builder]

# runner = Runner.run_sync(
#     starting_agent=outline_builder, 
#     input="Loops in Java"
# )

# print(runner.final_output)
# print(runner.last_agent.name)


# 3 DIFFERENT AGENTS EXAMPLE

@function_tool
def get_message()->str:
    """Check and returns unread whastapp messages and share them"""
    return "You have 1 message: 'Create a promotional facebook post and whatsapp message for my brand EatMySnack this is a food court' "

whatsapp_monitoring_agent: Agent = Agent(
    name="Whatsapp Monitoring Agent",
    instructions=(
        "Use the 'get_message' tool to check for unread WhatsApp messages.\n\n"
        "If the message requests both Facebook and WhatsApp content:\n"
        "1 First, handoff to the **Social Media Agent**.\n"
        "2 After getting that result, handoff to the **WhatsApp Messaging Agent**.\n"
        "3 When both responses are received, combine them into a clear final answer and return it.\n\n"
        "If only one type is requested, just handoff to that single agent."
    ),
    tools=[get_message],
    model=llm
)

whatsapp_messaging_agent: Agent =Agent(
    name="Whatsapp Messaging Agent",
    instructions= (
        "Write a short, catchy promotional WhatsApp message for the given topic or brand.\n"
        "Keep it friendly and concise.\n"
        "After writing, return the message as your final output whatsapp montoring agent (do not hand off)."
   
    ),
    handoff_description="Used for generating whatsapp message base on the topic",
    model=llm
)

social_media_agent : Agent = Agent(
    name="Social media agent",
    handoff_description="Used to generate social media content based on topic",
    instructions=(
        "Write a promotional Facebook or social media post for the given brand or topic.\n"
        "Make it creative and engaging.\n"
        "After writing, return the post as your final output to whatsapp montoring agent (do not hand off)."
        "NOTE: You cant produce whatsapp related content for that handoff your output to whatsapp montoring agent and it will handoff to whatsapp message agent"
    ),
    model=llm
)

whatsapp_monitoring_agent.handoffs= [social_media_agent, whatsapp_messaging_agent]
social_media_agent.handoffs = [whatsapp_monitoring_agent]
whatsapp_messaging_agent.handoffs = [whatsapp_monitoring_agent]

runner  = Runner.run_sync(
    starting_agent=whatsapp_monitoring_agent,
    input=""
)

print(runner.final_output)
print(runner.last_agent.name)
