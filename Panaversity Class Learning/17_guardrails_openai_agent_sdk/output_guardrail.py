from dotenv import load_dotenv
import os

from agents import Agent, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered, RunContextWrapper, RunResult, Runner, OpenAIChatCompletionsModel, output_guardrail
from openai import AsyncOpenAI
from pydantic import BaseModel

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
guardrail_llm : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-lite",
    openai_client=client
)


class AIGuardrailOutput(BaseModel):
    is_not_AI_related: bool
    reason: str
class MessageOutput(BaseModel):
    response: str

# Define guardrail agent
guardrail_agent: Agent = Agent(
    name="Guardrail Agent",
    model=guardrail_llm,
    instructions="check if the output is not related to AI or there is no AI base question or solution.",
    output_type=AIGuardrailOutput,
)


@output_guardrail
async def user_query_guardrail(ctx: RunContextWrapper, agent: Agent, output: MessageOutput) -> GuardrailFunctionOutput:
    
    result = await Runner.run(
        starting_agent=guardrail_agent,
        input=output.response,
        context=ctx.context
        )

    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_not_AI_related
    )

# Define agents

assistant_agent: Agent = Agent(
    name="Assistant Agent",
    model=llm,
    instructions="You are a helpful AI base assistant which provides information and answers questions related to AI.",
    output_guardrails=[user_query_guardrail],
    output_type=MessageOutput,
)

# Run a query

try:
    result: RunResult = Runner.run_sync(
        starting_agent=assistant_agent,
        # input="Can you make biryani using AI base suggestions? if yes than give me full hyderabadi biryani recipe.",
        input="hello there, i want to make a car?",

    )

    print("\n",result.final_output)
except OutputGuardrailTripwireTriggered as e:
    print("\nCustomer support related guardrail triggered:\n", str(e))