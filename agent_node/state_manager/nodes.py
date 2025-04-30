
from typing import Literal, List, Dict, Any, Union
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from agent_node.state_manager.agents import intent_agent, github_agent, clab_topology_agent, drift_manager_agent, llm, operational_agent
from utils.supervisorUtil import make_supervisor_node, State
from langgraph.types import Command
from typing_extensions import TypedDict
from templates.supervisor_template import state_supervisor_system_prompt



# Intent Agent Node
def intent_agent_node(state: State) -> Command[Literal["state_supervisor"]]:
    result = intent_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="intent_agent")
            ],
        },
        # Always report back to the state_supervisor when done
        goto="state_supervisor",
    )

# GitHub Agent Node
def github_agent_node(state: State) -> Command[Literal["state_supervisor"]]:
    result = github_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="github_agent")
            ],
        },
        # Always report back to the state_supervisor when done
        goto="state_supervisor",
    )

# CLab Topology Agent Node
def clab_topology_agent_node(state: State) -> Command[Literal["state_supervisor"]]:
    result = clab_topology_agent.invoke(state)
    return Command(
        update={
            "messages": [
                AIMessage(content=result["messages"][-1].content, name="clab_topology_agent")
            ]
        },
        # Always report back to the state_supervisor when done
        goto="state_supervisor",
    )

# Drift Manager Agent Node
def drift_manager_agent_node(state: State) -> Command[Literal["state_supervisor"]]:
    result = drift_manager_agent.invoke(state)
    return Command(
        update={
            "messages": [
                AIMessage(content=result["messages"][-1].content, name="drift_manager_agent")
            ],
        },
        # Always report back to the supervisor when done
        goto="state_supervisor",
    )

def operational_agent_node(state: State) -> Command[Literal["state_supervisor"]]:
    result = operational_agent.invoke(state)
    return Command(
        update={
            "messages": [
                AIMessage(content=result["messages"][-1].content, name="operational_agent")
            ],
        },
        # Always report back to the state_supervisor when done
        goto="state_supervisor",
    )



state_supervisor_node = make_supervisor_node(llm,
                                             ["intent_agent", "github_agent", "clab_topology_agent", "operational_agent"],
                                             master_system_prompt=state_supervisor_system_prompt)
