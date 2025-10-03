from dotenv import load_dotenv
import os
from agents import function_tool
from tavily import TavilyClient
load_dotenv()
api_key = os.getenv('TAVILY_API_KEY')


tavily_client = TavilyClient(api_key=api_key)


@function_tool
def web_search(question: str)-> str:
    """Search the web for answer"""
    print("Searching web tool called")

    result = tavily_client.search(f"{question}")
    
    return f"{result}"
