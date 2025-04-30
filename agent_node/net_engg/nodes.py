
from typing import Literal, List, Dict, Any, Union
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from agent_node.net_engg.agents import show_command_agent, validator_agent, intent_parser_agent, config_executor_agent, llm
from agent_node.state_manager.agents import github_agent, clab_topology_agent
from utils.supervisorUtil import make_supervisor_node, State
from langgraph.types import Command
from typing_extensions import TypedDict
from templates.supervisor_template import network_supervisor_system_prompt


# Intent Parser Node
def intent_parser_node(state: State) -> Command[Literal["networking_supervisor"]]:
    result = intent_parser_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="intent_parser_agent")
            ],
        },
        # Always report back to the networking_supervisor when done
        goto="networking_supervisor",
    )

# Config Executor Node
def config_executor_node(state: State) -> Command[Literal["networking_supervisor"]]:
    result = config_executor_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="config_executor_agent")
            ],
        },
        # Always report back to the networking_supervisor when done
        goto="networking_supervisor",
    )

# Show Command Node
def show_command_node(state: State) -> Command[Literal["networking_supervisor"]]:
    result = show_command_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="show_command_agent")
            ],
        },
        # Always report back to the networking_supervisor when done
        goto="networking_supervisor",
    )

# Validator Node
def validator_node(state: State) -> Command[Literal["networking_supervisor"]]:
    result = validator_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="validator_agent")
            ],
        },
        # Always report back to the networking_supervisor when done
        goto="networking_supervisor",
    )

# GitHub Agent Node
def github_agent_node(state: State) -> Command[Literal["networking_supervisor"]]:
    result = github_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="github_agent")
            ],
        },
        # Always report back to the networking_supervisor when done
        goto="networking_supervisor",
    )

# CLab Topology Agent Node
def clab_topology_agent_node(state: State) -> Command[Literal["networking_supervisor"]]:
    result = clab_topology_agent.invoke(state)
    return Command(
        update={
            "messages": [
                AIMessage(content=result["messages"][-1].content, name="clab_topology_agent")
            ]
        },
        # Always report back to the networking_supervisor when done
        goto="networking_supervisor",
    )


# Networking Supervisor Node
networking_supervisor_node = make_supervisor_node(llm, [
    "intent_parser_agent",
    "config_executor_agent",
    "show_command_agent", 
    "validator_agent",
    "github_agent",
    "clab_topology_agent"
],
    master_system_prompt=network_supervisor_system_prompt
)

# Add any additional logic or comments here if needed
