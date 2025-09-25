from dotenv import load_dotenv
import os
import asyncio
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, ModelSettings
from openai.types.responses import ResponseTextDeltaEvent
from openai import AsyncOpenAI

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

client = AsyncOpenAI(
    api_key= api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

async def main():

    llm: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
        openai_client=client,
        model="gemini-2.5-flash"
    )

    agent: Agent = Agent(name="AI Assistant", instructions="You are an AI Teacher which give solutions to any question.", model=llm)

    run_cfg = RunConfig(

        model_settings=ModelSettings(temperature=0.3)
    )

    res = Runner.run_streamed(agent, input("What you want to ask? "), run_config=run_cfg)

    async for event in res.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="\n", flush=True)


asyncio.run(main())