import paramiko

class ParamikoSSHClient:
    def __init__(self, host, username, password, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        try:
            print("Connecting to the device")
            self.client.connect(self.host, self.port, self.username, self.password)
        except Exception as e:
            print(f"Error occured while connecting to the device due to {e}")
    
    def exec_command(self, command):
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            op = stdout.read().decode('utf-8')
            return op
        except Exception as e:
            print(f"Error occured while executing the command due to {e}")
    
    def close(self):
        self.client.close()
    
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()