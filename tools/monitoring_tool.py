from langchain.tools import tool
import requests

@tool
def prometheus_query_tool() -> str:
    """
    Fetch all SNMP-exported metrics for the core router using the cisco_device module.
    No input needed. Returns raw metric text.
    """
    try:
        url = "http://172.18.117.152:9116/snmp?module=cisco_device&target=172.20.20.2"
        response = requests.get(url, timeout=5)  # Removed params={"query": query}
        if response.status_code == 200:
            # Assuming the response is JSON and contains a "data" field
            data = response.text
            if not data:
                return "No data returned for query."
            return str(data)
        else:
            return f"Query failed with status code: {response.status_code}"
    except Exception as e:
        return f"Error querying Prometheus: {str(e)}"