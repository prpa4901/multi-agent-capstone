from pydantic import BaseModel
from typing import List

class ParamikoToolInput(BaseModel):
    command: str

class NetmikoToolInput(BaseModel):
    command: str
    commands: List[str]
    device_ip: str
    device_type: str

class NetmikoProbeToolInput(BaseModel):
    commands: List[str]
    device_ip: str
    device_type: str