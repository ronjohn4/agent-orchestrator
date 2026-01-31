from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

class Output(BaseModel):
    input: str = Field(description="The original input")
    response: str = Field(description="The LLM response to the input")


class Orchestrator:
    def __init__(self):
        self.llm = ChatOllama(model="llama3", temperature=0)

    def ask(self, prompt_input: str, history: list[tuple[str, str]] | None = None) -> Output:
        """Invoke the LLM with optional conversation history for context."""
        messages: list[tuple[str, str]] = [
            ("system", "You are a helpful assistant who responds as briefly as possible."),
        ]
        if history:
            messages.extend(history)
        messages.append(("human", "{input}"))

        prompt = ChatPromptTemplate.from_messages(messages)
        pipe = prompt | self.llm.with_structured_output(Output)
        return pipe.invoke({"input": prompt_input})


# test_instance = Orchestrator()
# response = test_instance.ask("What is the capital of France?")
# print(response) # to get the entire response, structured or not
# print(response.content) # with no structured output
# print(response.response) # with structured output, to get just the response text
