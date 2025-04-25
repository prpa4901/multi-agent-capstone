import netmiko

class NetmikoSSHClient:
    def __init__(self, device_type, host, username, password, port=22):
        self.device_type = device_type
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        """Used for connecting to a network device"""
        device = {
            "device_type": self.device_type,
            "host": self.host,
            "username": self.username,
            "password": self.password,
            "port": self.port
        }
        try:
            self.connection = netmiko.ConnectHandler(**device)
        except Exception as e:
            return f"Error occured while connecting to the device due to {e}"
    
    def run_show_command(self, command):
        try:
            op = self.connection.send_command(command, delay_factor=15)
            return op
        except Exception as e:
            return f"Error occured while fetching the configs from the device due to {e}"


    def configure_commands(self, config_list):
        try:
            op = self.connection.send_config_set(config_list)
            return op
        except Exception as e:
            return f"Error occured while configuration due to {e}"

    def close(self):
        if self.connection:
            self.connection.disconnect()
    
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()