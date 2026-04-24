from pydantic import BaseModel, Field
from langchain.messages import AIMessage, HumanMessage
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from sympy import content
from app.api.getdatetime import get_datetime_subagent
from app.api.getweather import get_weather_subagent
from app.api.generalknowledge import get_general_knowledge
from app.config import Config

MODEL = Config.ORCHESTRATOR_MODEL
MAX_HISTORY_TURNS = Config.MAX_HISTORY_TURNS


class Output(BaseModel):
    input: str = Field(description="The original input")
    content: str = Field(description="The content of the response from the LLM")


class Orchestrator:
    """Orchestrator that delegates to sub-agents to fulfill user requests."""

    def __init__(self):
        self.session = []
        self.model = ChatOllama(model=MODEL, temperature=0)
        # self.tool_map = {
        #     "get_weather_subagent": get_weather_subagent, 
        #     "get_datetime_subagent": get_datetime_subagent,
        #     "get_general_knowledge": get_general_knowledge,
        # }
        self.tools = [get_weather_subagent, get_datetime_subagent, get_general_knowledge]
        self.orchestrator = create_agent(
            self.model, 
            tools=self.tools,  
            system_prompt="You are a manager. Delegate research to the researcher tools."
        )

    def _get_history(self) -> list[tuple[str, str]]:
        """Get conversation history from session as [(role, content), ...] for LangChain."""
        # raw = self.session.get("chat_history", [])
        return [(h["role"], h["content"]) for h in self.session]


    def _append_to_history(self, user_msg: str, assistant_msg: str) -> None:
        """Append a turn to session history and trim if needed."""
        # history = self.session.get("chat_history", [])
        history = self.session
        history.extend([
            {"role": "human", "content": user_msg},
            {"role": "ai", "content": assistant_msg},
        ])
        self.session = history[-(MAX_HISTORY_TURNS * 2) :]

    # def ask(self, prompt_input: str) -> Output:
    def ask(self, prompt_input: str) -> str:
        history = self._get_history()
        messages = []
        system = (
            "Categorize user requests as one of the following: "
            "1. Weather related "
            "2. Date or Time related "
            "3. General "
            "If the category is General, answer the question using the get_general_knowledge tool. "
            "Otherwise, delegate to the appropriate sub-agent and return only the sub-agent's response. "
            # "Do not return any extra commentary or information, just the sub-agent's answer."
            "Return the category in the response."
        )

        messages.append({"role": "system", "content": system})

        if history:
            for user_msg, assistant_msg in history:
                messages.append({"role": "user", "content": user_msg})
                messages.append({"role": "assistant", "content": assistant_msg})

        messages.append({"role": "user", "content": prompt_input})
        result = self.orchestrator.invoke({"messages": messages})

        # guard for varying result formats
        if isinstance(result, dict) and "messages" in result and len(result["messages"]) > 0:
             content = result["messages"][-1].content
        else:
            # fallback for lower-level return values
            content = str(result)

        self._append_to_history(prompt_input, content)

        # return Output(input=prompt_input, content=content)
        return content
        