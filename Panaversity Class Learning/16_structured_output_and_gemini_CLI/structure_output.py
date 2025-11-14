from dotenv import load_dotenv
import os

from agents import Agent, RunConfig, RunContextWrapper, RunResult, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from pydantic import BaseModel


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


class Skill(BaseModel):
    skill_name: str | None
    description: str| None
    level: str| None
    experience: int| None

class Userprofile(BaseModel):
    name: str
    age: int
    email: str
    skill : Skill | list[Skill]

agent = Agent(
    name="My Assistant", 
    model=llm,
    output_type=Userprofile
    )


result: RunResult = Runner.run_sync(
    starting_agent=agent,
    input="I am John Doe, 30 years old, and my email is john@gmail.com",
)

print(result.final_output)
