import os
from pydantic import BaseModel 
from dotenv import load_dotenv
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper
import re
from langchain_core.tools import Tool

load_dotenv()

# Load environment variables from .env file
GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")
GITHUB_REPO = "prpa4901/network-intent-capstone"

with open("github_app.pem", "r") as f:
    GITHUB_APP_PRIVATE_KEY = f.read()

def clean_tool_name(tool_name: str) -> str:
    clean_name = re.sub(r"[^\w\-]", "_", tool_name.lower())  # Replace invalid chars
    return clean_name

def fetch_github_toolkit():
    """
    Fetches the GitHub toolkit using the GitHub API wrapper.
    """
    # Initialize the GitHub API wrapper
    github = GitHubAPIWrapper(github_app_id=GITHUB_APP_ID,
                                github_app_private_key=GITHUB_APP_PRIVATE_KEY,
                                github_repository=GITHUB_REPO,
                                )
    # Initialize the GitHub toolkit
    toolkit = GitHubToolkit.from_github_api_wrapper(github)

    tools = toolkit.get_tools()

    for tool in tools:
        tool.name = clean_tool_name(tool.name)


    return tools
