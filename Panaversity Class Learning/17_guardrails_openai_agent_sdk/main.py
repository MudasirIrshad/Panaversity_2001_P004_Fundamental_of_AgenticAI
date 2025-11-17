from dotenv import load_dotenv
import os

from agents import Agent, GuardrailFunctionOutput, RunConfig, RunContextWrapper, RunResult, Runner, OpenAIChatCompletionsModel, TResponseInputItem, input_guardrail
from openai import AsyncOpenAI

# Load environment variables

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

# Initialize client

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

llm : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)


# Define guardrail agent
guardrail_agent: Agent = Agent(
    name="Guardrail Agent",
    model=llm,
    instructions="You are a guardrail agent that ensures user queries are safe and appropriate. user must not asked about pakistan law and regulations or anything related to that.",
)


@input_guardrail
async def user_query_guardrail(context: RunContextWrapper[None], agent: Agent,user_input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    result = await Runner.run(
        starting_agent=guardrail_agent,
        input=user_input,
        context=context.context
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output != "Input is safe."
    )

# Define agents

customer_support_agent: Agent = Agent(
    name="Customer Support Agent",
    model=llm,
    instructions="You are a helpful customer support agent for our software company.",
)

# Run a query

result: RunResult = Runner.run_sync(
    starting_agent=customer_support_agent,
    input="what is 2+2?",

)

print(result.final_output)