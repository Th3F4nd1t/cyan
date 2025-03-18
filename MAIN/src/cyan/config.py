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
    
    log("Starting configuration validation", LogLevel.INFO)
    # contains all required fields and dependencies

    # required field contains either "none", which skips to the next instruction, "main", which takes the list at index 1 and checks if it is in the outer layer of the config file
    # or "nest", which checks each nested instance of the original field for all items (nest is explicity used for things with multiple repeated fields, make a new one for other stuff)
    required_fields = {
        "cpu_name": ["none"],
        "creator": ["none"],
        "pipelined": ["main",["pipeline"]],
        "address_space": ["none"],
        "word_size": ["none"],
        "simulation_speed": ["none"],
        "register_count": ["none"],
        "special_registers": ["nest",["name","description","address","read_only","write_only","default_value","size","accumulates"]],
        "rom_size": ["none"],
        "ram_size": ["none"],
        "io_type": ["main",["io_reserved"]],
        "io_ports": ["nest",["name","description","address","read_only","write_only","default_value","size"]],
        "components": ["nest",["class","description","operations_handled"]],
        "opcode_length": ["none"],
        "instruction_set": ["nest",["name","opcode","operation","description","operands","latency","flags_affected"]],
    }



    for field in list(required_fields.keys()):
        if field not in config.keys():
            log(f"{field} not found in config. Aborting", LogLevel.FATAL)
        if required_fields[field][0] == "none":
            continue
        
        if required_fields[field][0] == "nest":
            for dependency in required_fields[field][1]:
                for index, subitem in enumerate(config[field]):
                    if dependency not in subitem.keys():
                        log(f"Dependency \'{dependency}\' of \'{field}\' not found in config. Aborting", LogLevel.FATAL)
        else:
            for dependency in required_fields[field][1]:
                if dependency not in config.keys():
                    log(f"Dependency \'{dependency}\' of \'{field}\' not found in config. Aborting", LogLevel.FATAL)
                

    log("Configuration validation complete", LogLevel.SUCCESS)