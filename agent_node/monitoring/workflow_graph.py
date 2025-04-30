
from langgraph.graph import StateGraph, START
from agent_node.monitoring.nodes import (
    config_executor_node,
    show_command_node,
    validator_node,
    clab_topology_agent_node,
    monitoring_agent_node,
    troubleshooting_agent_node,
    monitoring_supervisor_node,
)
from utils.supervisorUtil import State
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

# Define the State type
monitoring_manager_builder = StateGraph(State)
monitoring_manager_builder.add_node("monitoring_supervisor", monitoring_supervisor_node)
monitoring_manager_builder.add_node("monitoring_agent", monitoring_agent_node)
monitoring_manager_builder.add_node("troubleshooting_agent", troubleshooting_agent_node)
monitoring_manager_builder.add_node("config_executor_agent", config_executor_node)
monitoring_manager_builder.add_node("show_command_agent", show_command_node)
monitoring_manager_builder.add_node("validator_agent", validator_node)
monitoring_manager_builder.add_node("clab_topology_agent", clab_topology_agent_node)
monitoring_manager_builder.add_edge(START, "monitoring_supervisor")
monitoring_manager_graph = monitoring_manager_builder.compile(checkpointer=memory)
