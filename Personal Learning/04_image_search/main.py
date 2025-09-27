from dotenv import load_dotenv
import os
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled
from openai import AsyncOpenAI

from summary_tool import summary_tool

set_tracing_disabled(True)
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

llm : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash", openai_client=client
)

agent = Agent(
    name="OCR Summary Assistant",
    instructions="You are an OCR summarization agent. "
                 "First call the summary_tool to get text from the image, "
                 "then give response in format:\n"
                 "[TEXT]: <extracted text>\n[SUMMARY]: <summary of extracted text>",
    model=llm,
    tools=[summary_tool]
)


response = Runner.run_sync(starting_agent=agent, input=input("What you want?\nSummary of Text extracted from image or simple web searching?\n For image write the image name to summarize it\n"))

print(response.final_output)