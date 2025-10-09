from dotenv import load_dotenv
import os
from dataclasses import dataclass
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, RunContextWrapper
from openai import AsyncOpenAI
import speech_recognition as sr
import pyttsx3


r = sr.Recognizer()
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

@function_tool
def speech_to_text(audio:str):


    print("\n\nCalling speech to text tool now\n\n")
    with sr.AudioFile(audio) as source:
        audio_data = r.record(source)
        
    try:
        text = r.recognize_google(audio_data) # type: ignore
        print("Transcribed Text:", text)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service")
    return f"{text}"

@function_tool
def text_to_speech(text: str):
    """Convert any text to speech using system voice"""
    print("\n\n[TOOL] Speaking the LLM output...\n\n")
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)   # speed of voice
    engine.setProperty('volume', 0.9) # volume level (0.0 to 1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # type: ignore # choose voice
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    return "Spoken successfully."


agent: Agent = Agent(name="Assistant", instructions="""
You are my intelligent Assistant.
Your purpose is to provide accurate and meaningful information about famous Islamic personalities.

Behavior Rules:

If the user provides an audio file, first use the speech_to_text tool to convert the speech into text.

Once you have the transcribed text, or if the user’s input is already in text form, call the get_top_islamic_personalities tool to find detailed information related to the query.

After receiving the response from the tool, present your final answer in the following format:

[RESULT] <Provide the direct information or key findings here.>

[EXPLANATION] <Give a clear, well-written explanation that expands on the result — include context, history, and any relevant insights to make it educational and engaging.>


After showing your response, automatically call the text_to_speech tool to convert your full answer into spoken audio so it can be listened to easily.

Tone:
Stay respectful, clear, and informative — like a calm, helpful teacher explaining to a student. Avoid unnecessary details and keep responses natural and human-like.
""",
model=llm, 
tools=[speech_to_text,get_top_islamic_personalities, text_to_speech])


data_context = Top_Islamic_Personalities("data.txt")

result = Runner.run_sync(
    starting_agent=agent, 
    input="audio.wav",
    context=data_context
    )

print(result.final_output)