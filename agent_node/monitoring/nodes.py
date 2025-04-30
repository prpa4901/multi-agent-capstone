
from typing import Literal, List, Dict, Any, Union
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from agent_node.net_engg.agents import show_command_agent, validator_agent, config_executor_agent, llm
from agent_node.monitoring.agents import monitoring_agent, troubleshooting_agent
from agent_node.state_manager.agents import clab_topology_agent
from utils.supervisorUtil import make_supervisor_node, State
from langgraph.types import Command
from typing_extensions import TypedDict
from templates.supervisor_template import monitoring_supervisor_system_prompt



# Config Executor Node
def config_executor_node(state: State) -> Command[Literal["monitoring_supervisor"]]:
    result = config_executor_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="config_executor_agent")
            ],
        },
        # Always report back to the monitoring_supervisor when done
        goto="monitoring_supervisor",
    )

# Show Command Node
def show_command_node(state: State) -> Command[Literal["monitoring_supervisor"]]:
    result = show_command_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="show_command_agent")
            ],
        },
        # Always report back to the monitoring_supervisor when done
        goto="monitoring_supervisor",
    )

# Validator Node
def validator_node(state: State) -> Command[Literal["monitoring_supervisor"]]:
    result = validator_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="validator_agent")
            ],
        },
        # Always report back to the monitoring_supervisor when done
        goto="monitoring_supervisor",
    )


# CLab Topology Agent Node
def clab_topology_agent_node(state: State) -> Command[Literal["monitoring_supervisor"]]:
    result = clab_topology_agent.invoke(state)
    return Command(
        update={
            "messages": [
                AIMessage(content=result["messages"][-1].content, name="clab_topology_agent")
            ]
        },
        # Always report back to the monitoring_supervisor when done
        goto="monitoring_supervisor",
    )

# Monitoring Agent Node
def monitoring_agent_node(state: State) -> Command[Literal["monitoring_supervisor"]]:
    result = monitoring_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="monitoring_agent")
            ]
        },
        # Always report back to the monitoring_supervisor when done
        goto="monitoring_supervisor",
    )

# Troubleshooting Agent Node
def troubleshooting_agent_node(state: State) -> Command[Literal["monitoring_supervisor"]]:
    result = troubleshooting_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="troubleshooting_agent")
            ]
        },
        # Always report back to the monitoring_supervisor when done
        goto="monitoring_supervisor",
    )




# Monitoring Supervisor Node
monitoring_supervisor_node = make_supervisor_node(llm, [
    "config_executor_agent",
    "show_command_agent", 
    "validator_agent",
    "clab_topology_agent",
    "monitoring_agent",
    "troubleshooting_agent"
],
    master_system_prompt=monitoring_supervisor_system_prompt
)

# Add any additional logic or comments here if needed
