# the processor class is just a data structure that holds the state of the processor along with methods to modify the state as well as making sure the state is valid
from typing import List, Dict, Any
from .memory import *
from .config import *
import os, sys

class Processor:
    registers:List[MemoryCell]
    static:StaticConfig

    def __init__(self, config: dict, static:StaticConfig, state = None):
        self.static = static
        if state is None: self.generate_state(config) # Set to a blank state if there is no state provided
        else: self.state = self.upload_state(state)
        
    def generate_state(self, config): #resets and takes all state from config.yaml
        self.state = self.State()

        ## set ports
        if self.static.io_type == "mmio": # insert mmio to memory
            for index, port in enumerate(config["io_ports"]):
                port["accumulates"] = False
                self.state.ram.append( MemoryCell(port,"RAM") )
        else:
            for index, port in enumerate(config["io_ports"]):
                port["accumulates"] = False
                self.state.io.append( MemoryCell(port,"IO") )
        ## set ram
        for address in range(0, self.static.ram_size):
            if address in self.static.io_reserved: continue
            ram_cell = {
                "name": f"RAM cell {address}",
                "description": "RAM",
                "address": address,
                "size": self.static.word_size,
                "accumulates": False,
                "default_value": 0,
                "read_only": False,
                "write_only": False
            }
            self.state.ram.append(MemoryCell(ram_cell,"RAM"))
        
        ## set registers
        # special
        special_register_reserved = []
        for index, reg in enumerate(config["special_registers"]):
            self.state.registers.append( MemoryCell(reg,"Register") )
            special_register_reserved.append(config["special_registers"][index]["address"])

        # normal

        for address in range(0, self.static.register_count):
            if address in special_register_reserved: continue # if taken by special reg
            register_cell = {
                "name": f"Register cell {address}",
                "description": "Register",
                "address": address,
                "size": self.static.word_size,
                "accumulates": False,
                "default_value": 0,
                "read_only": False,
                "write_only": False
            }
            self.state.registers.append( MemoryCell(register_cell, "Register"))


        if self.static.pipelined:
            self.pipeline = self.Pipeline(config["pipeline"])

    def upload_state(self,config) -> dict: # takes state from file export
        ...


    def load_program(self,instructions):
        log(f"Starting program load into processor", LogLevel.INFO)
        # validate each instruction here
        # catch format errors but still will need error handling in mainloop as there are
        # some things that can't be validated
        sys.path.append(f"{os.getcwd()}/src/cyan/dynamic_resources") 
        instructionsFile = "instructions.py"
        module = __import__(str(instructionsFile).strip(".py"))

        for index,line in enumerate(instructions):
            if line == '': 
                self.state.prom.append("")
                continue
            raw_instr = line.split(' ')
            opcode, operands = raw_instr[0], raw_instr[1:]
            class_ = getattr(module, opcode.upper())
            instr_class = class_

            if len(operands) != len(instr_class.operands):
                log(f"Invalid operand match on line {index+1}. {opcode} Required {len(instr_class.operands)} --> Got {len(operands)}", LogLevel.FATAL)
            

            if self.static.pipelined:
                if list(instr_class.execution_chain.keys()) != self.pipeline.stages:
                    log(f"Pipeline stages on instruction {instr_class} don't match pipeline. Check config.yaml for uncaught errors",LogLevel.FATAL)
            
            # add values to the class
            for op_name, value in zip(instr_class.operands,operands):
                instr_class.data[op_name]['value'] = int(value)
            
            self.state.prom.append(instr_class)
        
        log("Program load complete",LogLevel.SUCCESS)
        return






    # processor subclasses

    class State: # handles processor state
        ram: List[MemoryCell]
        registers: List[MemoryCell]
        io: List[MemoryCell]
        prom: List[Any] # replace with List[Instruction] when instruction is defined
        pc: int

        def __init__(self):
            self.ram = []
            self.registers = []
            self.io = []
            self.prom = [] # replace with List[Instruction] when instruction is defined
            self.pc = 0
        
    class Pipeline(): #handles pipeline state

        current: List[Any] # replace with List[Instruction] once that is defined
        def __init__(self,stages):
            self.stages = stages
            self.current = [[] for i in self.stages]
        
        def flush(self):
            self.current = [[] for i in self.stages]
        
        def push(self,instruction):
            self.current.insert(0,instruction) # adds new instruction
            self.current.pop(len(self.pipeline)-1) # removes instruction just on writeback
