from typing import Literal
from langchain_core.language_models.chat_models import BaseChatModel

from langgraph.graph import MessagesState, END
from langgraph.types import Command
from typing_extensions import TypedDict
from templates.supervisor_template import supervisor_system_prompt

class State(MessagesState):
    next: str


def make_supervisor_node(llm: BaseChatModel, members: list[str], master_system_prompt: str = supervisor_system_prompt) -> str:
    options = ["FINISH"] + members
    master_system_prompt = master_system_prompt.format(members)

    class Router(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH."""

        next: Literal[*options]

    def supervisor_node(state: State) -> Command[Literal[*members, "__end__"]]:
        """An LLM-based router."""
        messages = [
            {"role": "system", "content": master_system_prompt},
        ] + state["messages"]
        response = llm.with_structured_output(Router).invoke(messages)
        goto = response["next"]
        if goto == "FINISH":
            goto = END

        return Command(goto=goto, update={"next": goto})

    return supervisor_node