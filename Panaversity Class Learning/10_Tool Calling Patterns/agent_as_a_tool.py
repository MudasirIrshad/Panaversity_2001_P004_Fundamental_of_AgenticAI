
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



copywriter: Agent = Agent(name="Copywriter",
                          model=llm,
                          )
contentcreater: Agent = Agent(name="Content Creator",
                          model=llm,
                          )



triage_agent: Agent = Agent(name="Triage Assistant", 
                            model=llm, 
                            tools=[
                                copywriter.as_tool(
                                    tool_name="copywriter_expert",
                                    tool_description="""
                                    Use it for exceptional copywriting tasks.
                                    """
                                ),
                                contentcreater.as_tool(
                                    tool_name="contentcreator_expert",
                                    tool_description="""
                                    Use it for exceptional content writing tasks.
                                    """
                                )
                            ]
                            
                            )

result = Runner.run_sync(starting_agent=triage_agent, input="Write a marvolous content for my linkedin post about quetta in 200 words. and a copywirte for this post")

print(result.final_output)