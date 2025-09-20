from dotenv import load_dotenv
import os

from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, RunResult # type: ignore


load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

external_client: AsyncOpenAI = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=api_key
)

llm : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

agent: Agent = Agent(name="Assistant", instructions="You are a motivational assistant", model=llm)

result: RunResult = Runner.run_sync(agent, "why learn math for AI Agents?")

print(result.final_output)