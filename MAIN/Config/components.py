from typing import List, Any


# no classes in components.py should have an init function
# they should just contain the operations and the operands which are given to it

# instruction req and operand req are not obsolete as we can just put a dict full of everything as data. do error checking in engine.
# each processor req is added to the end of the instruction in order put

# todo: replace all direct proc calls such as state with requests from Engine which acts as mediator
class ALU:
    def ADD(engine, data):
        # add timing stuff
        #read req is defined as (Mem_typem address)
        value = engine.read_req("Register", data["src1"]) + engine.read_req("Register",data["src2"])
        engine.set("flags", value, data["flags"])
        return value
        
    def SUB(engine, data):
        value = engine.read_req("Register", data["src1"]) - engine.read_req("Register",data["src2"])
        engine.set("flags", value, data["flags"])
        return value
    
    def AND(engine, data):
        value = engine.read_req("Register", data["src1"]) & engine.read_req("Register",data["src2"])
        engine.set("flags", value, data["flags"])
        return value

    def OR(engine, data):
        value = engine.read_req("Register", data["src1"]) | engine.read_req("Register",data["src2"])
        engine.set("flags", value, data["flags"])
        return value

    def XOR(engine, data):
        value = engine.read_req("Register", data["src1"]) ^ engine.read_req("Register",data["src2"])
        engine.set("flags", value, data["flags"])
        return value


class PC: # can grab access to proc_flags or state if need be


    def JMP(engine, data):
        if any(engine.get("flags")[data["flags"][flag]] for flag in data["flags"]):
            engine.set("pc",data["dest"])
        return None

class RAM:

    def WRITE(engine, data):
        # write_req should be structured as (mem_type, destination, source data)
        engine.write_req("RAM", engine.read_req("Register", data["dest"]) + data["off"], engine.read_req("Register", data["src1"]))

class REGISTERS:

    def LOD(engine, data): #load from RAM
        engine.write_req("Register", data["dest"], engine.read_req("RAM",engine.read_req("Register", data["src1"]) + data["off"]))

    def WRITE(engine, data):
        engine.write_req("Register", #type
                         data["dest"], #dest
                         data["passed"] #in this case passed is keyword for data that is carried through previous stage in pipeline
                        )

    def LDI(engine, data):
        engine.write_req("Register", #type
                         data["dest"], #dest
                         data["imm"] #since src1 is not comp yet it can act as imm
                        )
# no I/O state because this is a mmio cpu

class CLOCK:

    def HLT(engine,data):
        engine.halt_clock()


class FLAGS: # data will contain word_size
    def ZERO(value,word_size):
        return value == 0
    
    def CARRY(value,word_size):
        bin_format = '{'+f'0:{word_size}'+'}'
        if f'{bin_format}'.format(value)[0] == 1:
            return True
        return False
    
    def OVERFLOW(value,word_size):
        if value < 2**word_size:
            return True
        return False


