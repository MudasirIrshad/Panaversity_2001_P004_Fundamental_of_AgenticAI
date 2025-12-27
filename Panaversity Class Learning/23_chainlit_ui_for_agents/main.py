from dotenv import load_dotenv
import os
import chainlit as cl
from agents import Agent, RunConfig, RunResult, Runner, OpenAIChatCompletionsModel, SQLiteSession, function_tool, trace
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent



# Load environment variables
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

# Initialize client

client = AsyncOpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1"
)

session_storage = SQLiteSession("user_123","conversation_123.db")


llm : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="qwen2.5:7b",
    openai_client=client
)

@function_tool
@cl.step(type="tool")
def get_greeting(name: str) -> str:
    print(f"\n\n[TOOL]: Generating greeting for {name}")
    return f"Hello, {name}! How can I assist you today?"

@function_tool
@cl.step(type="tool")
def essay_writer(topic: str) -> str:
    print(f"\n\n[TOOL]: Writing essay on {topic}")
    return f"Here is an essay on {topic}."


agent : Agent = Agent(
    name="Assistant",
    instructions="You are an AI assistant that helps users with their questions before answering any question you need to check all the tools available and use them appropriately. Always use 'get_greeting' tool to greet users, Use essay_writer tool to write essays.",
    model=llm,
    tools=[get_greeting, essay_writer],
)

@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...

    msg = await cl.Message(content="").send()

    # Run the agent with the user's message
    result = Runner.run_streamed(
        starting_agent=agent,
        input=message.content,
        # session=session_storage,
    )

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            tokens = event.data.delta
            await msg.stream_token(tokens)

    await msg.send()