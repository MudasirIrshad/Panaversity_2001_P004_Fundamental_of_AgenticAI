from dotenv import load_dotenv
import os

from agents import Agent, AgentHooks, RunConfig, RunContextWrapper, RunHooks, RunResult, Runner, OpenAIChatCompletionsModel
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

# Define Hooks

class MyAgentHooks(RunHooks):
    async def on_start(self, context, agent) -> None:
        """Called before the agent is invoked. Called each time the running agent is changed to this
        agent."""
        print(f"\n[RUN HOOK] Starting agent: {agent.name}\n")

    async def on_end(
        self,
        context,
        agent,
        output,
    ) -> None:
        """Called when the agent produces a final output."""
        print(f"\n[RUN HOOK] Ending agent: {agent.name} with output: {output}\n")

    async def on_handoff(
        self,
        context,
        from_agent,
        to_agent,
    ) -> None:
        """Called when the agent is being handed off to. The `source` is the agent that is handing
        off to this agent."""
        print(f"\n[RUN HOOK] Handing off from agent: {from_agent.name} to agent: {to_agent.name}\n")

    async def on_tool_start(
        self,
        context,
        agent,
        tool,
    ) -> None:
        """Called immediately before a local tool is invoked."""
        print(f"\n[RUN HOOK] Agent: {agent.name} is starting tool: {tool.name}\n")

    async def on_tool_end(
        self,
        context,
        agent,
        tool,
        result,
    ) -> None:
        """Called immediately after a local tool is invoked."""
        print(f"\n[RUN HOOK] Agent: {agent.name} has finished tool: {tool.name} with result: {result}\n")

    async def on_llm_start(
        self,
        context,
        agent,
        system_prompt,
        input_items,
    ) -> None:
        """Called immediately before the agent issues an LLM call."""
        print(f"\n[RUN HOOK] Agent: {agent.name} is starting LLM call with prompt: {system_prompt} and inputs: {input_items}\n")

    async def on_llm_end(
        self,
        context,
        agent,
        response,
    ) -> None:
        """Called immediately after the agent receives the LLM response."""
        print(f"\n[RUN HOOK] Agent: {agent.name} has received LLM response: {response}\n")



# Define agents with AGENT Hooks

urdu_agent = Agent(
    name="urdu_agent", 
    instructions="You translate the user input into Urdu and respond the translation in Roman urdu only", 
    model=llm,
)


customer_support_agent = Agent(
    name="customer_support_agent", 
    instructions="Only handoff when user ask to translate to urdu. You determine which agent to use based on user input.", 
    model=llm,
    handoffs=[urdu_agent]
)
# Run a query
result: RunResult = Runner.run_sync(
    starting_agent=customer_support_agent,
    input="Why learn math for AI agents? translate to urdu",
    hooks=MyAgentHooks(),
)

print(result.final_output)