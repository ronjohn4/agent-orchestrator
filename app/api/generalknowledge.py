from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from datetime import datetime
from langchain.agents import create_agent


MODEL = "llama3.2"

#-------------------------------------------------------------------
# get_general_knowledge sub-agent
#-------------------------------------------------------------------
model = ChatOllama(model=MODEL)

subagent_runnable = create_agent(
    model=model,
    system_prompt=(
        "You are a general knowledge agent. "
        "Return the shortest possible response that answers the question—no extra "
        "context, no preamble, just the answer."
    )
)


@tool("general_knowledge", description="Used for general questions that are not domain specific.")
def get_general_knowledge(query: str) -> str:
    """This sub-agent can answer general knowledge questions that are not weather or date/time related."""
    result = subagent_runnable.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content
