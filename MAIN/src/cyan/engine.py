# take in instruction classes and modify the state of the processor based on the instructions
# instruction operations need a dict "data" which can contain any number of things differently per instruction
# will need to make a function which contructs it and everything it needs

from .processor import Processor
from .config import *
import os,sys, time

class Engine:
    static: StaticConfig
    proc: Processor
    
    def __init__(self, instructions, config):
        self.static = StaticConfig(config) # contains base info about cpu which could be useful
        self.proc = Processor(config, self.static)
        self.proc.load_program(instructions)
        self.instructions = instructions
        self.clock_run = False

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
        # match case for easier expansion
        match source:
            case "pc": return self.proc.state.pc
            case "pipeline": return self.proc.pipeline.current
            case "flags": return self.proc.state.flags

            case source: # case where nothing else was found
                log(f"Datatype {source} not valid for engine.\'get\'", LogLevel.WARNING)
                return
    

    def set(self, source, value:int, flags:List[str] = None):
        source = source.lower()
        
        match source:
            case "pc": # checks for overflow first
                if len(self.proc.state.prom) > value:
                    log(f"Jump to {value} caused PC overflow to {value-len(self.proc.state.prom)}",LogLevel.WARNING)
                    self.proc.state.pc = value-len(self.proc.state.prom)
                self.proc.state.pc = value
                return

            case "flags":
                # check for flags updating
                if flags is None: #checks to make sure instruction was given
                    log(f"Searched flags not present in instruction", LogLevel.WARNING)
                    return
                # finds flags class from components.py
                sys.path.append(f"{os.getcwd()}/Config") 
                instructionsFile = "components.py"
                module = __import__(str(instructionsFile).strip(".py"))
                class_ = getattr(module, "flags".upper())

                for flag in flags: # evals for each flag needed to be updated
                    self.proc.state.flags[flag] = eval(f"class_.{flag}({value},{self.static.word_size})")

            case source: 
                log(f"Datatype {source} not valid for engine.\'get\'", LogLevel.WARNING)
                return
    

    def run(self):
        self.clock_run = True

        log("Starting new runtime",LogLevel.INFO)
        if self.static.pipelined:
            log("Pipeline enabled, switching to pipelined runtime", LogLevel.INFO)
            self.run_pipelined()
            return
        log("Pipeline disable, using default runtime", LogLevel.INFO)


        for instruction in self.proc.state.prom:
            # start work on this still a hell of a lot of things to iron out on the theory side but it shouldn't b e impossible
            ...


        log("Non pipelined runtime hasn't been implented yet", LogLevel.FATAL)
    

    def stop_clock(self):
        self.clock_run == False




    def run_pipelined(self):

        while self.clock_run and self.proc.pipeline.current: # only stop once pipeline is fully empty

            # will have to deal with hazards, like data, control, multiple things trying to use a single multi-cycle component. Etc
            if self.static.simulation_speed == 0:
                time.sleep(0)
            else:
                time.sleep(1000/self.static.simulation_speed)
            break # just for testing remove once not needed
        
        log("Pipeliend runtime hasn't been implemented yet", LogLevel.FATAL)