from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools.networking_tool import clab_tool, show_netmiko_tool
from tools.gitop_tool import fetch_github_toolkit
from langchain_core.prompts import ChatPromptTemplate
from templates.state_manager_template import (
    intent_template, github_template, clab_topology_manager_template, drift_manager_template
)
import os

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

local_env_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o",
                temperature=0,  # Lower for factual accuracy  # Larger context window
                api_key=local_env_api_key,
)

git_tools = fetch_github_toolkit()

tools_list = git_tools + [clab_tool, show_netmiko_tool]

intent_chat_prompt = ChatPromptTemplate.from_messages([
    ("system", intent_template),
    ("placeholder", "{messages}"),
])

github_chat_prompt = ChatPromptTemplate.from_messages([
    ("system", github_template),
    ("placeholder", "{messages}"),
])

clab_topology_chat_prompt = ChatPromptTemplate.from_messages([
    ("system", clab_topology_manager_template),
    ("placeholder", "{messages}"),
])

drift_manager_chat_prompt = ChatPromptTemplate.from_messages([
    ("system", drift_manager_template),
    ("placeholder", "{messages}"),
])



intent_agent = create_react_agent(
    model=llm,
    tools=tools_list,
    debug=True,
    prompt=intent_chat_prompt,
)

github_agent = create_react_agent(
    model=llm,
    tools=tools_list,
    debug=True,
    prompt=github_chat_prompt,
)

clab_topology_agent = create_react_agent(
    model=llm,
    tools=tools_list,
    debug=True,
    prompt=clab_topology_chat_prompt,
)

drift_manager_agent = create_react_agent(
    model=llm,
    tools=tools_list,
    debug=True,
    prompt=drift_manager_chat_prompt,
)

