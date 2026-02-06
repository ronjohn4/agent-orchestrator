from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain.messages import AIMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI

from app.routes.tools import get_weather, get_datetime, tool_map


class Output(BaseModel):
    input: str = Field(description="The original input")
    content: str = Field(description="The content of the response from the LLM")


# Tools available to the sub-agent (e.g. GetWeather)
TOOLS = [get_weather, get_datetime]


class ToolsSubAgent:
    """Sub-agent that executes tool calls (e.g. GetWeather, GetTime)."""

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.llm_with_tools = self.llm.bind_tools(TOOLS)

    def run(self, task: str) -> str:
        """Execute the task by calling tools as needed. Returns the final answer."""
        messages = [HumanMessage(content=task)]
        max_iterations = 10

        for _ in range(max_iterations):
            response = self.llm_with_tools.invoke(messages)
            messages.append(response)

            if isinstance(response, AIMessage) and response.tool_calls:
                for tool_call in response.tool_calls:
                    tool_name = tool_call["name"]
                    tool_args = tool_call["args"]
                    tool_response = tool_map[tool_name].invoke(tool_args)
                    messages.append(
                        ToolMessage(
                            content=tool_response,
                            tool_call_id=tool_call["id"],
                        )
                    )
            else:
                return response.content

        return "Sub-agent exceeded maximum iterations."


class Orchestrator:
    """Orchestrator that delegates to sub-agents to fulfill user requests."""

    def __init__(self):
        self.tools_agent = ToolsSubAgent()
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        orchestrator_self = self

        @tool
        def delegate_to_tools_agent(task: str) -> str:
            """Delegate to the tools sub-agent. Use when the user needs: weather (GetWeather), current time, or other tool-based information. Pass a clear task description."""
            return orchestrator_self.tools_agent.run(task)

        self.delegate_tool = delegate_to_tools_agent
        self.orchestrator_tools = [self.delegate_tool]
        self.llm_with_tools = self.llm.bind_tools(self.orchestrator_tools)

    def ask(self, prompt_input: str, history: list[tuple[str, str]] | None = None) -> Output:
        messages = []

        if history:
            for user_msg, assistant_msg in history:
                messages.append(HumanMessage(content=user_msg))
                messages.append(AIMessage(content=assistant_msg))

        system = (
            "You are an orchestrator that coordinates sub-agents. "
            "When the user needs weather, current time, or similar data, use delegate_to_tools_agent. "
            "For simple chat, respond directly."
        )
        messages.append(HumanMessage(content=f"{system}\n\nUser: {prompt_input}"))

        max_iterations = 10
        for _ in range(max_iterations):
            response = self.llm_with_tools.invoke(messages)
            messages.append(response)

            if isinstance(response, AIMessage) and response.tool_calls:
                for tool_call in response.tool_calls:
                    if tool_call["name"] == "delegate_to_tools_agent":
                        task = tool_call["args"]["task"]
                        result = self.tools_agent.run(task)
                        messages.append(
                            ToolMessage(
                                content=result,
                                tool_call_id=tool_call["id"],
                            )
                        )
            else:
                content = response.content
                return Output(input=prompt_input, content=content)

        return Output(input=prompt_input, content="Orchestrator exceeded maximum iterations.")
