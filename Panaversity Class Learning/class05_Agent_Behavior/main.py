from dotenv import load_dotenv
import os
from openai.types.shared import Reasoning
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, ModelSettings
from openai import AsyncOpenAI

set_tracing_disabled(True)
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

client = AsyncOpenAI(
    api_key= api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

llm: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client)


agent: Agent = Agent(name="Assistant", instructions="You are a motivational assistant", model=llm, model_settings =ModelSettings(
    # top_p=0.9,
    temperature=0.7,
    # max_tokens=1024,
    reasoning = Reasoning(
        effort="high",
        summary="auto"
    )
) )

result = Runner.run_sync(agent, "poem on pakistan")

print(result.new_items)