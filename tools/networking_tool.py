from langchain_core.tools import tool, render_text_description
from model_schema.net_tool_models import ParamikoToolInput, NetmikoToolInput, NetmikoProbeToolInput
from utils.netmikoSSHClient import NetmikoSSHClient
from utils.paramikoSSHClient import ParamikoSSHClient
from typing import List
from rapidfuzz import process
import os

REMOTE_TOPOLOGY_DIRECTORY = os.getenv("REMOTE_TOPOLOGY_DIRECTORY")
REMOTE_VM_HOST = os.getenv("REMOTE_HOST")
REMOTE_VM_USERNAME = os.getenv("REMOTE_USERNAME")
REMOTE_VM_PASSWORD = os.getenv("REMOTE_PASSWORD")
REMOTE_VM_PORT = os.getenv("REMOTE_PORT")
NETWORK_DEVICE_USER = os.getenv("NETWORK_DEVICE_USER")
NETWORK_DEVICE_PASSWORD = os.getenv("NETWORK_DEVICE_PASSWORD")


@tool(return_direct=True, args_schema=ParamikoToolInput)
def clab_tool(command: str):
    """Tool used for SSH into VM device with VM_ip and run various command over SSH, mainly for inspecting containerlab topology"""
    try:
        # vals = ai_analzed_string.split(",")
        if not command:
            return "Either command or device ip is missing, please provide correct command and device ip"
        command = command.split('=')[-1].strip().strip("'").strip('"')
        # device_ip = vm_ip.split('=')[-1].strip().strip("'").strip('"')
        # print(device_ip)
        print(command)
        ssh_client = ParamikoSSHClient(REMOTE_VM_HOST,
                                       REMOTE_VM_USERNAME,
                                       REMOTE_VM_PASSWORD,
                                       22)
        ssh_client.connect()
        parsed_output = ssh_client.exec_command(command)
        print(parsed_output)
        ssh_client.close()
        return parsed_output
    except Exception as e:
        return f"Error occured while configuration due to {e}, you can retry if needed"

@tool(return_direct=True, args_schema=NetmikoToolInput)
def show_netmiko_tool(command: str, device_ip: str, device_type: str, commands=[]):
    """Tool used for getting or fetching network configuration from a network device"""
    try:

        # command, device_ip, device_type = ai_action_command.split(",")
        # print(device_type)
        # print(device_ip)
        # print(command)
        command = command.split('=')[-1].strip().strip("'").strip('"')
        device_ip = device_ip.split('=')[-1].strip().strip("'").strip('"')
        device_type = device_type.split('=')[-1].strip().strip("'").strip('"')
        ssh_client = NetmikoSSHClient(device_type,
                                      device_ip,
                                      username=NETWORK_DEVICE_USER,
                                      password=NETWORK_DEVICE_PASSWORD,
                                      port=22)
        ssh_client.connect()
        parsed_output = ssh_client.run_show_command(command)
        ssh_client.close()
        return parsed_output
    except Exception as e:
        return f"Error occured while configuration due to {e}, you can retry if needed"


@tool(args_schema=NetmikoToolInput)
def apply_netmiko_config_tool(commands: List[str], device_ip: str, device_type: str, command=""):
    """Tool used for writing and applying network configuration on a network device in config mode"""
    try:
        ssh_client = NetmikoSSHClient(device_type,
                                      device_ip,
                                      username=NETWORK_DEVICE_USER,
                                      password=NETWORK_DEVICE_PASSWORD,
                                      port=22)
        ssh_client.connect()
        op = ssh_client.configure_commands(commands)
        ssh_client.close()
        return op
    except Exception as e:
        return f"Error occured while configuration due to {e}, you can retry if needed"


@tool(args_schema=NetmikoProbeToolInput)
def supported_command_probe_tool(commands: List[str], device_ip: str, device_type: str):
    """
    Given a list of intended commands, this tool probes the CLI of the specified network device
    to find the nearest valid supported commands using fuzzy matching.
    """
    try:
        ssh_client = NetmikoSSHClient(
            device_type=device_type,
            host=device_ip,
            username="your_username",
            password="your_password"
        )
        ssh_client.connect()

        help_output = ssh_client.run_show_command("?")

        available_cmds = [
            line.strip().split()[0]
            for line in help_output.splitlines()
            if line.strip()
        ]

        suggestions = {}
        for cmd in commands:
            matches = process.extract(cmd, available_cmds, limit=3)
            suggestions[cmd] = [m[0] for m in matches]

        ssh_client.close()
        return suggestions

    except Exception as e:
        return {"error": str(e)}

