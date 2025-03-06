# getting configuration things also process yaml file
from typing import List
import yaml

class Config:
    def __init__(self):
        self.name:str = ""
        self.version:str = ""
        self.description:str = ""
        self.creator:str = ""

        self.word_size:int = 0
        self.simulation_speed:float = 0

        self.register_count:int = 0
        self.special_registers:List[SpecialRegister] = []
        
        self.rom_size:int = 0
        self.ram_size:int = 0

        self.io_type:str = "" # pmio or mmio
        self.io_ports:List[IoPort] = []

        self.components:List[Component] = []

        self.instructions:List[Instruction] = []

class SpecialRegister:
    ...

class IoPort:
    ...

class Component:
    ...

class Instruction:
    ...

def get_config(file):
    with open(file, 'r') as f:
        return yaml.safe_load(f)
    
def _validate_config(config):
    ...