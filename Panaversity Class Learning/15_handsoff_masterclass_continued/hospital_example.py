from dataclasses import dataclass
from dotenv import load_dotenv
import os

from agents import Agent, RunConfig, RunContextWrapper, RunResult, Runner, OpenAIChatCompletionsModel, handoff, trace, trace
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
# Define agents


cardiologist_agent = Agent(
    name="Cardiologist Agent",
    instructions="you are a cardiologist. You will receive patient symptoms and provide a diagnosis and treatment plan. Your job is to handle the patients issues",
    model=llm
    )



class UserProblem(BaseModel):
    problem_description: str

def on_cardiologist_handoff(ctx: RunContextWrapper, input: UserProblem):
    print("\nHandoff to Cardiologist Agent Logged\n")



receptionist_agent = Agent(
    name="Receptionist Agent",
    instructions="you are a hospital receptionist." \
    "You answer general patient questions." \
    "If the patient has a heart issue, handoff to the cardiologist agent.",
    handoff_description="Routes patients to the correct specialist based on their symptoms.",
    model=llm,
    handoffs=[
        handoff(
            agent=cardiologist_agent,
            tool_description_override="handle_cardiology_patient",
            on_handoff = on_cardiologist_handoff,
            input_type = UserProblem
        )
    ]
    )


#Storing conversation history between receptionist and patient


with trace("medical_handoff_conversation"):

    conversation_history = []
    while True:

        user_input = input("Patient: ")
        conversation_history.append({"content": user_input, "role": "user"})
        # Run a query
        result: RunResult = Runner.run_sync(
            starting_agent=receptionist_agent,
            input=conversation_history,
        )
        llm_response = result.final_output
        conversation_history = result.to_input_list() # type: ignore
        print(result.last_agent.name, "\n")
        print(result.final_output)