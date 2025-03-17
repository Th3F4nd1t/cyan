from typing import List, Any


# no classes in components.py should have an init function
# they should just contain the operations and the operands which are given to it

# instruction_req and operand req are put in a single dict with respective names and values
# each processor req is added to the end of the instruction in order put

# todo: replace all direct proc calls such as state witha request from Engine which acts as mediator
class ALU:
    operand_req = ["src1","src2"]
    instruction_req = ["flags_affected"]
    processor_req = ["flags"]

    def Add(self, data, proc_flags):
        # add timing stuff
        value = data["src1"]+data["src2"]
        proc_flags.update(value, data["flags_affected"])
        return value
        
    def Sub(self, data, proc_flags):
        value = data["src1"]-data["src2"]
        proc_flags.update(value, data["flags_affected"])
        return value
    
    def And(self, data, proc_flags):
        value = data["src1"]&data["src2"]
        proc_flags.update(value, data["flags_affected"])
        return value

    def Or(self, data, proc_flags):
        value = data["src1"]|data["src2"]
        proc_flags.update(value, data["flags_affected"])
        return value

    def Xor(self, data, proc_flags):
        value = data["src1"]^data["src2"]
        proc_flags.update(value, data["flags_affected"])
        return value


class PC: # can grab access to proc_flags or state if need be
    operand_req = ["dest","flag"]
    instruction_req = []
    processor_req = ["flags", "state"]

    def Jmp(self, data, proc_flags, state):
        if proc_flags.get(data["flag"]):
            state.pc = data["dest"]
        return None

class RAM:
    operand_req = ["dest","src1", "src2"]
    instruction_req = []
    processor_req = ["state"]

    def CST(self, data, state):
        state.ram[data["dest"]+data["src2"]].write(state.registers[data["src1"]].read())
    
    def CLD(self, data, state):
        state.registers[data["dest"]+data["src2"]].write(state.ram[data["src1"]].read())

class Registers:
    operand_req = ["dest","imm"]
    instruction_req = []
    processor_req = ["state"]

    def LDI(self, data, state):
        state.registers[data["dest"].write(data["imm"])]

# no I/O state because this is a mmio cpu