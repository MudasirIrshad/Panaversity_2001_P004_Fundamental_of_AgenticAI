# 🏃 Runner.run_streamed in OpenAI Agent SDK

When running an **agent** using `Runner.run_streamed`, the output is not delivered at once.  
Instead, the agent streams tokens **as they are generated** by the LLM, and three main types of **stream events** are triggered.

---

## 📡 Stream Events

### 1. `AgentUpdatedStreamEvent`
- Triggered whenever the **state of the agent** is updated during the run.
- For example, when the agent switches tools, changes steps, or updates its reasoning trace.

### 2. `RawResponseEvent`
- Contains the **raw, low-level tokens** as they are received from the LLM.
- Useful if you want to build **real-time typing effects** (like ChatGPT) or debug token streams.

### 3. `RunItemStreamEvent`
- Emits **structured items** that are produced during the run (e.g., messages, tool calls, or intermediate steps).
- Higher-level than raw tokens, more semantic and agent-friendly.

---

## ⚡ How It Works
- Instead of waiting for the **entire completion**, you subscribe to these events.
- Each event will fire **as soon as a new token or step is available**.
- This is useful for building:
  - 🖥️ Real-time dashboards  
  - 💬 Chat UIs with typing effect  
  - 🔎 Debugging traces of agent reasoning  

---