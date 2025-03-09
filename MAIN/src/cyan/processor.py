# the processor class is just a data structure that holds the state of the processor along with methods to modify the state as well as making sure the state is valid
from typing import List, Dict, Any
from memory import *
from config import *


class Processor:
    state:Dict[str,Any]
    registers:List[MemoryCell]
    static:StaticConfig

    def __init__(self, config: dict, static:StaticConfig, state: dict = None):
        self.static = static
        if state is None: self.generate_state(config) # Set to a blank state if there is no state provided
        else: self.state = self.upload_state(state) 



    def generate_state(self, config): #resets and takes all state from config.yaml
        self.state = {
            "ram": [],
            "prom": [],
            "registers": [],
            "io": [],
            "pc": 0,
        }
        ## set ports
        if self.static.io_type == "mmio": # insert mmio to memory
            for index, port in enumerate(config["io_ports"]):
                port["accumulates"] = False
                self.state["ram"].append( MemoryCell(port,"RAM") )
        else:
            for index, port in enumerate(config["io_ports"]):
                port["accumulates"] = False
                self.state["io"].append( MemoryCell(port,"IO") )
        
        ## set ram
        for address in range(0, self.static.ram_size):
            if address in self.static.io_reserved: continue
            ram_cell = {
                "name": f"RAM cell {i}",
                "description": "RAM",
                "address": address,
                "size": self.static.word_size,
                "accumulates": False,
                "default_value": 0,
                "read_only": False,
                "write_only": False
            }
            self.state["ram"].append(MemoryCell(ram_cell,"ram"))
        
        ## set registers
        # special
        special_register_reserved = []
        for index, reg in enumerate(config["special_registers"]):
            self.state["registers"].append( MemoryCell(reg,"Register") )
            special_register_reserved.append(config["special_registers"]["address"])

        # normal

        for address in range(0, self.static.register_count):
            if address in special_register_reserved: continue # if taken by special reg
            register_cell = {
                "name": f"Register cell {i}",
                "description": "Register",
                "address": address,
                "size": self.static.word_size,
                "accumulates": False,
                "default_value": 0,
                "read_only": False,
                "write_only": False
            }
            self.state["registers"].append( MemoryCell(register_cell, "Register"))




    def upload_state(self,config) -> dict: #takes state from file export
        ...
