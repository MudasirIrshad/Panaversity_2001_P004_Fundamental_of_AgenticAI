from dotenv import load_dotenv
import os
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled
from openai import AsyncOpenAI

from summary_tool import summary_tool
from web_search import web_search

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
    instructions="You are an OCR summarization and web search agent. "
                 "based on the question call the summary_tool to get text from the image or web_search tool for web base searching, "
                 "then give response in format:\n"
                 "for summary_tool = [TEXT]: <extracted text>\n[SUMMARY]: <summary of extracted text>" 
                 "for web_search = [Your Question]: <question of user>\n [Answer]: <answer from web_search tool>",
    model=llm,
    tools=[summary_tool, web_search]
)


response = Runner.run_sync(starting_agent=agent, input=input("What you want?\nSummary of Text extracted from image or simple web searching?\n For image write the image name to summarize it\n and for web searching simply ask your question: \n"))

print(response.final_output)