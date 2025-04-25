import streamlit as st
import uuid
from langchain_core.messages import HumanMessage
from workflow_layer.master_supervisor import super_graph
from typing import List, Dict


def run_supergraph(super_graph, input_message: str, message_history: List, config: Dict):
    """Runs LangGraph master supervisor and returns updated message history."""
    state_input = {
        "messages": message_history + [HumanMessage(content=input_message)]
    }
    response = ""
    # print(bot)
    for event in super_graph.stream(state_input, config, stream_mode="values"):
        response = event
    return response


# ---- Streamlit App Layout ----
st.set_page_config(page_title="🧠 Network Master Supervisor", layout="wide")
st.title("🧠 Multi-Agent Network Supervisor")
st.markdown("Ask anything about network config, intent, drift, or monitoring.")

# ---- Session State Setup ----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state["all_messages"] = []

if "context" not in st.session_state:
    st.session_state.context = {}

if st.session_state.get("thread_id") is None:
    st.session_state["thread_id"] = str(uuid.uuid4())
    st.session_state["config"] = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "recursion_limit": 150,
    }

# ---- Show Chat History ----
for message in st.session_state.get("chat_history", []):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



# ---- User Input ----
question = st.chat_input("Ask a question to your network automation system...")

if question:
    # Display user message
    st.chat_message("user").markdown(question)
    st.session_state.chat_history.append({"role": "user", "content": question})

    # Call Supervisor Agent
    with st.spinner("Routing your request to the right agents..."):
        updated_messages = run_supergraph(
            super_graph,
            question,
            st.session_state.chat_history,
            st.session_state.config,
        )
        # print("-- Updated Messages --")
        # print(updated_messages)
        # print("-- End of Updated Messages --")
        st.session_state["all_messages"] = updated_messages["messages"]
        final_response = updated_messages['messages'][-1].content

    # Display Assistant response
    with st.chat_message("assistant"):
        st.markdown(final_response)

    # Update full message history
    st.session_state["chat_history"].append(
        {"role": "assistant", "content": final_response}
    )
