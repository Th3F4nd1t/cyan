# getting configuration things also process yaml file
from .utils import *
from .memory import *
from typing import List, Dict, Any
import yaml

class StaticConfig:
    # stores all static cpu info
    def __init__(self,config):
        self.name:str = config["cpu_name"]
        self.version:str = config["cpu_version"]
        self.description:str = config["cpu_description"]
        self.creator:str = config["creator"]

        self.pipelined:bool = config["pipelined"]
        self.word_size:int = config["word_size"]
        self.simulation_speed:float = config["simulation_speed"]

        self.address_space:int = config["address_space"]
        self.register_count:int = config["register_count"]
        self.rom_size:int = config["rom_size"]
        self.ram_size:int = config["ram_size"]
        

        self.io_type:str = config["io_type"] # pmio or mmio
        self.io_reserved:List[int] = config["io_reserved"] # which mem cells are reserved by mmio


def get_config(file):
    with open(file, 'r') as f:
        return yaml.safe_load(f)
    
def validate_config(config):
    ...

# i have no idea where to put or do with these so they will stay here for now
class Component:
    ...

class Instruction:
    ...
