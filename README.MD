# FINANCIAL AGENT
---

The goal of this assignment is to understand the fundamental mechanics of LLM Agents without relying on high-level frameworks like LangChain. You will implement a "Financial Assistant" that can answer questions about exchange rates and stock prices. You must implement best coding practices, including Function Maps for routing, Environment Variables for security, and handling Parallel Tool Calls .  

**Agent has separated concerns and boundaries**
- main.py is the launching point for the agent and what should be used to run from terminal
- functions.py contains the functions needed
- schemas.py contains the tool schema given to the model
- agent.py contains the agent orchestration logic
- requirements.txt contains the requiremetns