from dotenv import load_dotenv
import os
from dataclasses import dataclass
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, RunContextWrapper
from openai import AsyncOpenAI
load_dotenv()


set_tracing_disabled(True)
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

client = AsyncOpenAI(
    api_key= api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)



llm: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client)



@dataclass
class Top_Islamic_Personalities:
    def __init__(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            self.raw_text = f.read()
            self.lines = self.raw_text.splitlines()
    def search_personality(self, name: str)->str:
        """Search for a name and return matching lines"""
        matches = [line for line in self.lines if name.lower() in line.lower()]

        if matches:
            return "\n".join(matches)
        else:
            return f"No information found about {name}"
  



@function_tool
def get_top_islamic_personalities(local_context:RunContextWrapper, name: str)->str:
    print(f"\n\n [TOOL] Getting data for {name}\n\n")


    data_context: Top_Islamic_Personalities = local_context.context
    res = data_context.search_personality(name)
    print(f"\n\n [CONTEXT] Getting data for {name}\n\n")
    return f"This is about {res}."



agent: Agent = Agent(name="Assistant", instructions="You are my Assistant. Use the tool to find details about Islamic personalities. after getting response from the tool try to give output in this way \n[RESULT] <Result from tool> \n[EXPLANATION] <Try to enhance the tool response and give a explained output here >",model=llm, tools=[get_top_islamic_personalities])


data_context = Top_Islamic_Personalities("data.txt")

result = Runner.run_sync(
    starting_agent=agent, 
    input="Tell me about umar",
    context=data_context
    )

print(result.final_output)