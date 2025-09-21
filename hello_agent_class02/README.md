# 📖 Theory: Why and How This Code Works

This project shows how to use the **OpenAI Agent SDK** with **Google Gemini models**. Let’s break down why we need each piece:

1. **dotenv** → We use `from dotenv import load_dotenv` to load environment variables (like API keys) from a `.env` file instead of hardcoding them in code. This keeps credentials secure and makes the project portable.  
2. **os** → We import `os` to fetch the API key after dotenv loads it, using `os.getenv("GOOGLE_API_KEY")`.  
3. **agents (Agent, Runner, OpenAIChatCompletionsModel)** → These are part of the **Agent SDK**.  
   - **Agent**: Defines the assistant (its name, personality, and role). Without this, the model would just return text, not act like an "agent".  
   - **Runner**: Executes the agent and manages the full run (input → reasoning → output). It’s like the engine that drives the agent.  
   - **OpenAIChatCompletionsModel**: This wraps any OpenAI-compatible chat model (in this case Gemini) so it works inside the Agent SDK.  
4. **openai.AsyncOpenAI** → This is the **client** that connects to an OpenAI-style API endpoint. Since Google Gemini exposes an OpenAI-compatible API, we set `base_url="https://generativelanguage.googleapis.com/v1beta/openai/"`. The `api_key` is also passed here. Without the client, the agent would have no way to communicate with the model.  
5. **Putting it all together** →  
   - Load API key securely with dotenv.  
   - Create the `AsyncOpenAI` client to talk to Gemini’s API.  
   - Wrap the model with `OpenAIChatCompletionsModel` to make it usable inside the SDK.  
   - Define the `Agent` with role + instructions.  
   - Use `Runner.run_sync` to execute the agent on a given task (e.g., “why learn math for AI Agents?”).  
   - Print `result.final_output` to see the agent’s clean response.  

In short:  
- **dotenv + os** → Securely manage API keys.  
- **AsyncOpenAI** → The bridge to Gemini’s API.  
- **Model Wrapper** → Makes Gemini usable by the SDK.  
- **Agent** → The brain with personality.  
- **Runner** → The executor of tasks.  

This workflow ensures you can **easily swap models**, **keep your code clean**, and **leverage agentic behavior** without manual wiring of chains or prompts.
