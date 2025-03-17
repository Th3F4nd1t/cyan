from .utils import *
from typing import Dict, Any
# all types of memory live here


class MemoryCell:
    # MemoryCell is the basis of all memory types.
    # it requires a cell_info dict which contains the intial state of the register
    # todo add signs
    def __init__(self, cell_info: Dict[str, Any], memory_class: str): 

        self.mem_class:str = memory_class
        self.name:str = cell_info["name"]
        self.description:str = cell_info["description"]
        self.address:int = cell_info["address"]
        self.read_only:bool = cell_info["read_only"]
        self.write_only:bool = cell_info["write_only"]
        self.accumulates:bool = cell_info["accumulates"]
        self.word_size:int = cell_info["size"]
        self.value:int = cell_info["default_value"]
    
    def __repr__(self):
        return f"Memory {self.mem_class}: Address={self.address}, Value={self.value}"

    def read(self):
        if self.write_only:
            log(f"Write-only error: Reading from {self.mem_class} {self.address} failed","WARNING")
            return
        return self.value
    

    def write(self, value):
        # add size checking
        if self.read_only:
            log(f"Read-only error: Writing to {self.mem_class} {self.address} failed","WARNING")
            return
        
        if self.accumulates: # check for accumulator reg
            self.value += value
        else:
            self.value = value
        
        if self.value > (2**self.word_size): #size checking
            log("Data out of range, overflowing", "WARNING")
            # for signed that warning becomes an error
            # also for signed overflow to negative
            self.value = self.value % (2 ** self.wordSize)





