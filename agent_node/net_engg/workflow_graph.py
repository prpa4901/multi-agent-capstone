
from langgraph.graph import StateGraph, START
from agent_node.net_engg.nodes import (
    intent_parser_node,
    config_executor_node,
    show_command_node,
    validator_node,
    networking_supervisor_node,
    github_agent_node,
    clab_topology_agent_node,
)
from utils.supervisorUtil import State
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

# Define the State type
networking_manager_builder = StateGraph(State)
networking_manager_builder.add_node("networking_supervisor", networking_supervisor_node)
networking_manager_builder.add_node("intent_parser_agent", intent_parser_node)
networking_manager_builder.add_node("config_executor_agent", config_executor_node)
networking_manager_builder.add_node("show_command_agent", show_command_node)
networking_manager_builder.add_node("validator_agent", validator_node)
networking_manager_builder.add_node("github_agent", github_agent_node)
networking_manager_builder.add_node("clab_topology_agent", clab_topology_agent_node)
networking_manager_builder.add_edge(START, "networking_supervisor")
network_manager_graph = networking_manager_builder.compile(checkpointer=memory)
