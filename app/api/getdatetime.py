from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from datetime import datetime
from langchain.agents import create_agent


MODEL = "llama3.2"

#-------------------------------------------------------------------
# get_datetime tool
#-------------------------------------------------------------------
class DatetimeResult(BaseModel):
    """Structured result for date, time, timezone, day of week."""
    date: str = Field(description="Current date in YYYY-MM-DD format")
    time: str = Field(description="Current time in HH:MM:SS format")
    timezone: str = Field(description="Local timezone name or offset")
    day_of_week: str = Field(description="Full day name (e.g. Monday)")


@tool
def get_datetime() -> DatetimeResult:
    """Get the date and time. Use when the user asks about:
    - current time, what time it is, what's the time
    - today's date, what date is it, what day is today
    - day of week, weekday, or similar time/date questions,
    - time zone, what time zone am I in, what is my time zone.
    Returns the date, time, timezone and day of week as structured JSON."""
    now = datetime.now().astimezone()
    result = DatetimeResult(
        date=now.strftime("%Y-%m-%d"),
        time=now.strftime("%H:%M:%S"),
        timezone=now.tzname() or str(now.tzinfo) if now.tzinfo else "local",
        day_of_week=now.strftime("%A"),
    )
    return result.model_dump_json()


#-------------------------------------------------------------------
# get_datetime sub-agent
#-------------------------------------------------------------------
model = ChatOllama(model=MODEL)

subagent_runnable = create_agent(
    model=model,
    tools=[get_datetime],
    system_prompt=(
        "You are a specialized date and time agent. "
        "Always use the get_datetime tool to get accurate information. "
        "Return the shortest possible response that answers the question—no extra "
        "context, no preamble, just the answer."
    )
)


@tool("get_datetime_subagent", description="Used to find date and time related information.")
def get_datetime_subagent(query: str) -> str:
    """This sub-agent can determine the date, time, timezone, day of week"""
    result = subagent_runnable.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content
