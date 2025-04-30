
from langgraph.graph import StateGraph, START
from agent_node.state_manager.nodes import (
    intent_agent_node,
    github_agent_node,
    clab_topology_agent_node,
    drift_manager_agent_node,
    state_supervisor_node,
    operational_agent_node,
)
from utils.supervisorUtil import State
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

# from langgraph.types import Command
state_manager_builder = StateGraph(State)
state_manager_builder.add_node("state_supervisor", state_supervisor_node)
state_manager_builder.add_node("intent_agent", intent_agent_node)
state_manager_builder.add_node("github_agent", github_agent_node)
state_manager_builder.add_node("clab_topology_agent", clab_topology_agent_node)
state_manager_builder.add_node("operational_agent", operational_agent_node)
# state_manager_builder.add_node("drift_manager_agent", drift_manager_agent_node)

state_manager_builder.add_edge(START, "state_supervisor")

state_manager_graph = state_manager_builder.compile(checkpointer=memory)