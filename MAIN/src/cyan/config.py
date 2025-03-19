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

        self.flags: List[str] = config["flags"]

def get_config(file):
    with open(file, 'r') as f:
        return yaml.safe_load(f)
    



def validate_config(config):
    
    log("Starting configuration validation", LogLevel.INFO)
    # contains all required fields and dependencies

    # required field contains either "none", which skips to the next instruction, "main", which takes the list at index 1 and checks if it is in the outer layer of the config file
    # or "nest", which checks each nested instance of the original field for all items (nest is explicity used for things with multiple repeated fields, make a new one for other stuff)
    # after nest or main instead of a list you can put a "cond", followed by a dict with each value and its possible dependencies
    # however due to how stupid the code is it is needed that you put [None,[<dependencies here>]] as the format.
    required_fields = {
        "cpu_name": ["none"],
        "creator": ["none"],
        "pipelined": ["main","cond",{True:[None,["pipeline"]], False:[None,["none"]]}], # fix this because it always checks for pipeline facepalm
        "address_space": ["none"],
        "word_size": ["none"],
        "simulation_speed": ["none"],
        "register_count": ["none"],
        "special_registers": ["nest",["name","description","address","read_only","write_only","default_value","size","accumulates"]],
        "rom_size": ["none"],
        "ram_size": ["none"],
        "io_type": ["main","cond",{"mmio":[None,["io_reserved"]],"pmio":[None,["none"]]}],
        "io_ports": ["nest",["name","description","address","read_only","write_only","default_value","size"]],
        "components": ["nest",["class","description","operations_handled"]],
        "opcode_length": ["none"],
        "instruction_set": ["nest",["name","opcode","operation","description","operands","latency","flags_affected"]],
    }

    # make nested nests for when it comes to instruction sets
    # about this section below here. Uhh. So I coded it and it works i guess but i have no clue how i tried to line comment here and there but it is still confusing
    def nest_search(field,domain):
        try:
            for dependency in domain[field][1]:
                if dependency == "none": continue
                for index, subitem in enumerate(config[field]):
                    if dependency not in subitem.keys(): # checks nested instances of domain given
                        log(f"Dependency \'{dependency}\' of \'{field}\' not found in config.", LogLevel.FATAL)
        except KeyError:
            log(f"Dependency \'{field}\' not in possible configurations", LogLevel.FATAL)

    def main_search(field,domain):
        try:
            for dependency in domain[field][1]:
                if dependency == "none": continue
                if dependency not in config.keys(): # checks surface layer of config
                    log(f"Dependency \'{dependency}\' of \'{field}\' not found in config.", LogLevel.FATAL)
        except KeyError:
            log(f"Dependency \'{field}\' not in possible configurations", LogLevel.FATAL)
    
    # start iterating
    for field in list(required_fields.keys()):
        if field not in config.keys():
            log(f"{field} not found in config.", LogLevel.FATAL)
        
        # allows for people to skip sections using None keyword which would otherwise be flagged (more customisablity)
        if required_fields[field][0] == "none" or config[field] == "None":
            continue
        
        #checking for nested or main
        if required_fields[field][0] == "nest":
            # checking for conditional
            if required_fields[field][1] == "cond":
                # if true changes the domain that the nest_search will be looking for to a more local one
                nest_search(config[field],required_fields[field][2])
                continue
            nest_search(field,required_fields)
        else:
            # same as nest_search but for main
            if required_fields[field][1] == "cond":
                main_search(config[field],required_fields[field][2])
                continue
            main_search(field)
                

    log("Configuration validation complete", LogLevel.SUCCESS)