
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools.networking_tool import apply_netmiko_config_tool, show_netmiko_tool, supported_command_probe_tool
from tools.gitop_tool import fetch_github_toolkit

from langchain_core.prompts import ChatPromptTemplate
from templates.netengg_template import network_config_prompt, validator_prompt, show_command_prompt, config_executor_prompt, intent_parser_prompt
import os

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

local_env_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o",
                temperature=0,  # Lower for factual accuracy  # Larger context window
                api_key=local_env_api_key,
)

git_tools = fetch_github_toolkit()

tools_list = git_tools + [apply_netmiko_config_tool, show_netmiko_tool, supported_command_probe_tool]



networking_chat_prompt = ChatPromptTemplate.from_messages([
    ("system", network_config_prompt),
    ("placeholder", "{messages}"),
])

intent_chat_prompt = ChatPromptTemplate.from_messages([
    ("system", intent_parser_prompt),
    ("placeholder", "{messages}"),
])

config_chat_prompt = ChatPromptTemplate.from_messages([
    ("system", config_executor_prompt),
    ("placeholder", "{messages}"),
])

validator_chat_prompt = ChatPromptTemplate.from_messages([
    ("system", validator_prompt),
    ("placeholder", "{messages}"),
])

show_command_chat_prompt = ChatPromptTemplate.from_messages([
    ("system", show_command_prompt),
    ("placeholder", "{messages}"),
])


intent_parser_agent = create_react_agent( 
    model=llm,
    tools=tools_list,
    debug=True,
    prompt=networking_chat_prompt,
)

config_executor_agent = create_react_agent(
    model=llm,
    tools=tools_list,
    debug=True,
    prompt=networking_chat_prompt,
)

show_command_agent = create_react_agent(
    model=llm,
    tools=tools_list,
    debug=True,
    prompt=networking_chat_prompt,
)

validator_agent = create_react_agent(
    model=llm,
    tools=tools_list,
    debug=True,
    prompt=networking_chat_prompt,
)

