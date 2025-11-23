from dotenv import load_dotenv
import os

from agents import Agent, AgentHooks, RunConfig, RunContextWrapper, RunResult, Runner, OpenAIChatCompletionsModel
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

class MyAgentHooks(AgentHooks):
    async def on_start(self, context, agent) -> None:
        """Called before the agent is invoked. Called each time the running agent is changed to this
        agent."""
        print(f"\n[HOOK]Agent {agent.name} is starting. \n")


    async def on_end(self,
        context,
        agent,
        output
        ) -> None:
        print(f"\n[HOOK]Agent {agent.name} finished \n")

    async def on_handoff(self, context, agent, source) -> None:
        """Called when the agent is being handed off to. The `source` is the agent that is handing
        off to this agent."""
        print(f"\n[HOOK]Handoff from {source.name} to {agent.name}.\n")

    async def on_llm_start(self,
        context,
        agent,
        system_prompt,
        input_items,
    ) -> None:
        """Called immediately before the agent issues an LLM call."""
        print(f"\n[LLM HOOK]Agent {agent.name} is calling LLM.\n")
    
    async def on_llm_end(
        self,
        context,
        agent,
        response,
    ) -> None:
        """Called immediately after the agent receives an LLM response."""
        print(f"\n[LLM HOOK]Agent {agent.name} received LLM response.\n")



# Define agents with AGENT Hooks

urdu_agent = Agent(
    name="urdu_agent", 
    instructions="You translate the user input into Urdu and respond the translation in Roman urdu only", 
    model=llm,
    hooks=MyAgentHooks()
    )


customer_support_agent = Agent(
    name="customer_support_agent", 
    instructions="Only handoff when user ask to translate to urdu. You determine which agent to use based on user input.", 
    model=llm,
    handoffs=[urdu_agent],
    hooks=MyAgentHooks()
    
    )
# Run a query
result: RunResult = Runner.run_sync(
    starting_agent=customer_support_agent,
    input="Why learn math for AI agents? translate to urdu",
    
)

print(result.final_output)