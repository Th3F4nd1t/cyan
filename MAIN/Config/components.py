from typing import List, Any


# no classes in components.py should have an init function
# they should just contain the operations and the operands which are given to it

# instruction req and operand req are not obsolete as we can just put a dict full of everything as data. do error checking in engine.
# each processor req is added to the end of the instruction in order put

# todo: replace all direct proc calls such as state with requests from Engine which acts as mediator
class ALU:
    processor_req = ["flags"]

    def ADD(self, engine, data, proc_flags):
        # add timing stuff
        #read req is defined as (Mem_typem address)
        value = engine.read_req("Register", data["src1"]) + engine.read_req("Register",data["src2"])
        proc_flags.update(value, data["flags_affected"])
        return value
        
    def SUB(self, engine, data, proc_flags):
        value = engine.read_req("Register", data["src1"]) - engine.read_req("Register",data["src2"])
        proc_flags.update(value, data["flags_affected"])
        return value
    
    def AND(self, engine, data, proc_flags):
        value = engine.read_req("Register", data["src1"]) & engine.read_req("Register",data["src2"])
        proc_flags.update(value, data["flags_affected"])
        return value

    def OR(self, engine, data, proc_flags):
        value = engine.read_req("Register", data["src1"]) | engine.read_req("Register",data["src2"])
        proc_flags.update(value, data["flags_affected"])
        return value

    def XOR(self, engine, data, proc_flags):
        value = engine.read_req("Register", data["src1"]) ^ engine.read_req("Register",data["src2"])
        proc_flags.update(value, data["flags_affected"])
        return value


class PC: # can grab access to proc_flags or state if need be

    processor_req = ["flags", "state"]

    def JMP(self, engine, data, proc_flags, state):
        if proc_flags.get(data["flag"]):
            state.pc = data["dest"]
        return None

class RAM:
    processor_req = []

    def WRITE(self, engine, data):
        # write_req should be structured as (mem_type, destination, source data)
        engine.write_req("RAM", engine.read_req("Register", data["dest"]) + data["off"], engine.read_req("Register", data["src1"]))

class Registers:
    processor_req = []

    def LOD(self, engine, data): #load from RAM
        engine.write_req("Register", data["dest"], engine.read_req("RAM",engine.read_req("Register", data["src1"]) + data["off"]))

    def WRITE(self, engine, data):
        engine.write_req("Register", #type
                         data["dest"], #dest
                         data["passed"] #in this case passed is keyword for data that is carried through previous stage in pipeline
                        )

    def LDI(self, engine, data):
        engine.write_req("Register", #type
                         data["dest"], #dest
                         data["imm"] #since src1 is not comp yet it can act as imm
                        )
# no I/O state because this is a mmio cpu