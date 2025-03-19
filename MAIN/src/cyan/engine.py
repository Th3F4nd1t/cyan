# take in instruction classes and modify the state of the processor based on the instructions

from .processor import Processor
from .config import *

class Engine:
    static: StaticConfig
    proc: Processor
    
    def __init__(self, instructions, config):
        self.static = StaticConfig(config) # contains base info about cpu which could be useful
        self.proc = Processor(config, self.static)
        self.proc.load_program(instructions)
        self.instructions = instructions
    

    def write_req(self, mem_type, destination, data):
        # this func acts as an intermediary before modifying processor. A smoothing over
        mem_type = mem_type.lower()

        if mem_type not in ("register", "ram", "io"):
            log(f"Addressed to non-existent memory type {mem_type}", LogLevel.WARNING)
            return
        if 0 < destination < eval(f"len(self.proc.state.{mem_type})"):
        # this eval statement is not safe at all, but since it is a downloaded source project its fine
        # user can only hack themselves with this
            return eval(f"self.proc.state.{mem_type}[{destination}].write({data})")

        # if outside of range
        log(f"Addressed memory out of range", LogLevel.WARNING)
        return

    def read_req(self, mem_type, location):
        mem_type = mem_type.lower()

        # checking if the mem type was written correctly
        if mem_type not in ("register", "ram", "io"):
            log(f"Read from non-existent memory type {mem_type}", LogLevel.WARNING)
            return

        if 0 < location < eval(f"len(self.proc.state.{mem_type})"): # checks for addressing within bounds of memory
        # this eval statement is not safe at all, but since it is a downloaded source project its fine
            return eval(f"self.proc.state.{mem_type}[{location}].read()")

        # if outside of mem range
        log(f"Addressed memory out of range", LogLevel.WARNING)
        return




    def get(self,source):
        source = source.lower()

        match source:
            case "pc": return self.proc.state.pc
            case "pipeline": return self.proc.pipeline.current
            case "flags": return self.proc.state.flags

            case source: 
                log(f"Datatype {source} not valid for engine.\'get\'", LogLevel.WARNING)
                return
    