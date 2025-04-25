from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from utils.supervisorUtil import make_supervisor_node, State
from typing import Literal, TypedDict, List, Dict, Any, Union
from agent_node.state_manager.workflow_graph import state_manager_graph
from agent_node.net_engg.workflow_graph import network_manager_graph
from langgraph.graph import StateGraph, START
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver

llm = ChatOpenAI(model="gpt-4o")


# master_supervisor_node = make_supervisor_node(llm, ["state_supervisor", "network_supervisor"])

master_supervisor_node = make_supervisor_node(llm, ["state_supervisor"])

def call_state_team(state: State) -> Command[Literal["master_supervisor"]]:
    response = state_manager_graph.invoke({"messages": state["messages"][-1]})
    return Command(
        update={
            "messages": [
                AIMessage(
                    content=response["messages"][-1].content, name="state_supervisor"
                )
            ],
        },
        goto="master_supervisor",
    )

def call_network_team(state: State) -> Command[Literal["master_supervisor"]]:
    response = network_manager_graph.invoke({"messages": state["messages"][-1]})
    return Command(
        update={
            "messages": [
                AIMessage(
                    content=response["messages"][-1].content, name="network_supervisor"
                )
            ],
        },
        goto="master_supervisor",
    )

memory = MemorySaver()

super_builder = StateGraph(State)
super_builder.add_node("master_supervisor", master_supervisor_node)
super_builder.add_node("state_supervisor", call_state_team)
# super_builder.add_node("network_supervisor", call_network_team)

super_builder.add_edge(START, "master_supervisor")
super_graph = super_builder.compile(checkpointer=memory)