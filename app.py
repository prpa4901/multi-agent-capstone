import streamlit as st
import uuid
from langchain_core.messages import HumanMessage
# from agent_node.state_manager.agents import 
from agent_node.state_manager.workflow_graph import state_manager_graph
from agent_node.net_engg.workflow_graph import network_manager_graph
from agent_node.monitoring.workflow_graph import monitoring_manager_graph
# from workflow_layer.monitoring.workflow_graph import monitoring_supervisor_graph  # if exists
from typing import List, Dict


def run_graph(graph_executor, input_message: str, message_history: List, config: Dict):
    """Runs selected graph and returns updated message history."""
    state_input = {
        "messages": message_history + [HumanMessage(content=input_message)]
    }
    response = ""
    for event in graph_executor.stream(state_input, config, stream_mode="values"):
        if event["messages"]:
            latest_message = event["messages"][-1]
            with st.expander(f"🔍 Debug Step - {latest_message.type}"):
                st.markdown(latest_message.content)
            response = event
    return response


# ---- Streamlit App Layout ----
st.set_page_config(page_title="🧠 Modular Network Automation", layout="wide")
st.title("🧠 Modular Multi-Agent Supervisor")
st.markdown("Choose the specialized agent for network tasks.")

# ---- Session State Setup ----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = "Intent Agent"

if st.session_state.get("thread_id") is None:
    st.session_state["thread_id"] = str(uuid.uuid4())
    st.session_state["config"] = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "recursion_limit": 150,
    }

# ---- Sidebar Agent Selector ----
st.sidebar.header("Select Active Agent")
if st.sidebar.button("Intent Agent"):
    st.session_state.selected_agent = "Intent Agent"
if st.sidebar.button("Network Config Agent"):
    st.session_state.selected_agent = "Network Config Agent"
if st.sidebar.button("Monitoring Agent"):
    st.session_state.selected_agent = "Monitoring Agent"

# ---- Show Chat History ----
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---- User Input ----
question = st.chat_input(f"Ask something for {st.session_state.selected_agent}...")

if question:
    # Display user input
    st.chat_message("user").markdown(question)
    st.session_state.chat_history.append({"role": "user", "content": question})

    # Choose the appropriate agent graph
    selected_graph = None
    if st.session_state.selected_agent == "Intent Agent":
        selected_graph = state_manager_graph
    elif st.session_state.selected_agent == "Network Config Agent":
        selected_graph = network_manager_graph
    elif st.session_state.selected_agent == "Monitoring Agent":
       selected_graph = monitoring_manager_graph
    else:
        st.error("Unknown agent selected.")
        selected_graph = None

    if selected_graph:
        with st.spinner(f"Running {st.session_state.selected_agent}..."):
            updated_messages = run_graph(
                selected_graph,
                question,
                st.session_state.chat_history,
                st.session_state.config,
            )
            final_response = updated_messages['messages'][-1].content

        with st.chat_message("assistant"):
            st.markdown(final_response)

        # Save Assistant Response
        st.session_state.chat_history.append(
            {"role": "assistant", "content": final_response}
        )
