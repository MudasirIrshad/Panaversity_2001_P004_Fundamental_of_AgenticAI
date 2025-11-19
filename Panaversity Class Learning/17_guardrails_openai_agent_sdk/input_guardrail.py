from dotenv import load_dotenv
import os

from agents import Agent, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, RunConfig, RunContextWrapper, RunResult, Runner, OpenAIChatCompletionsModel, TResponseInputItem, input_guardrail
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


class ProductGuardrailOutput(BaseModel):
    is_not_product_related: bool
    reason: str


# Define guardrail agent
guardrail_agent: Agent = Agent(
    name="Guardrail Agent",
    model=guardrail_llm,
    instructions="check if the user query is not related to ecommerce knowledge, business ideas or any product related information.",
    # instructions="""
    # You evaluate if a user query is any ecommerce product, price, ecommerce, or business ideas.
    # Return:
    # - is_not_product_related = false  → Only if the query is about ecommerce product, price, ecommerce, or business ideas.
    # - is_not_product_related = true → For all other queries.

    # Be strict and literal. Do NOT mark normal questions about history, politics, religion, America, or general topics as related to ecommerce product, price, ecommerce, or business ideas..
    # """,
    output_type=ProductGuardrailOutput,
)


@input_guardrail
async def user_query_guardrail(context: RunContextWrapper[None], agent: Agent,user_input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    result = await Runner.run(
        starting_agent=guardrail_agent,
        input=user_input,
        context=context.context
    )

    if(result.final_output.is_not_product_related):
        print("Guardrail triggered: Query is not product related.")
    

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_not_product_related
    )

# Define agents

customer_support_agent: Agent = Agent(
    name="Customer Support Agent",
    model=llm,
    instructions="You are a helpful customer support agent for our software company.",
    input_guardrails=[user_query_guardrail],
)

# Run a query

try:
    result: RunResult = Runner.run_sync(
        starting_agent=customer_support_agent,
        # input="how to grow a product in ecommerce?",
        input="how to grow a product in ecommerce? Who was the first president of the United States?",

    )

    print(result.final_output)
except InputGuardrailTripwireTriggered as e:
    print("Product related guardrail triggered:", str(e))