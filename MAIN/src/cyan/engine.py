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
        self.proc.load_program(instructions, config)
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
                class_ = getattr(module, "FLAGS")

                for flag in flags: # evals for each flag needed to be updated
                    self.proc.state.flags[flag] = eval(f"class_.{flag.upper()}({value},{self.static.word_size})")

            case source: 
                log(f"Datatype {source} not valid for engine.\'get\'", LogLevel.WARNING)
                return
    

    def run(self):
        self.clock_run = True

        sys.path.append(f"{os.getcwd()}/Config") 
        instructionsFile = "components.py"
        module = __import__(str(instructionsFile).strip(".py"))

        log("Starting new runtime",LogLevel.INFO)
        if self.static.pipelined:
            log("Pipeline enabled, switching to pipelined runtime", LogLevel.INFO)
            self.run_pipelined(module)
            return
        log("Pipeline disable, using default runtime", LogLevel.INFO)


        for instruction in self.proc.state.prom:
            # start work on this still a hell of a lot of things to iron out on the theory side but it shouldn't b e impossible
            ...


        log("Non pipelined runtime hasn't been implented yet", LogLevel.FATAL)
    

    def halt_clock(self):
        self.clock_run = False




    def run_pipelined(self,module):

        # pipeline already defined
        # make the forwarder

        while True: # only stop once pipeline is fully empty
            

            # will have to deal with hazards, like data, control, multiple things trying to use a single multi-cycle component. Etc
            # main data hazard right now to deal with is alu forwarding

            if self.clock_run: # if no halt yet
                try:
                    self.proc.pipeline.push(self.proc.state.prom[self.proc.state.pc])
                except IndexError:
                    self.proc.pipeline.push('')
                    if all(x == '' for x in self.proc.pipeline.current):
                        log("No halt detected at end of program.", LogLevel.FATAL)
            else:
                self.proc.pipeline.push('')
                if all(x == '' for x in self.proc.pipeline.current): # only checks if there are instructions left that were inserted before the halt instruction
                    break


            forward_incremented = []
            prev_clock = self.proc.state.pc
            print(self.proc.pipeline.current) # debug to see pipeline stages
            for index in range(len(self.proc.pipeline.stages)):
                current = self.proc.pipeline.current[len(self.proc.pipeline.stages) - index - 1]
                if current == '': # skip if empty
                    continue 



                operation = current.execution_chain[self.static.pipeline[len(self.proc.pipeline.stages) - index - 1]]
                
                if operation == "None": continue

                data = {}
                i = 0
                dest = None
                sources = []
                print(current)
                print(current.data)
                for operand in current.data:
                    if current.data[operand]["type"].upper() == "REGISTER.DESTINATION":
                        dest = current.data[operand]["value"]
                    if current.data[operand]["type"].upper() == "REGISTER.VALUE":
                        sources.append(operand)
                    data[operand] = current.data[operand]["value"]
                

                data["flags"] = []
                for flag in current.flags:
                    data["flags"].append(flag)
                
                
                



                name = operation.split('.')[0].upper()
                if self.static.components[name]["forwarded"]:
                    for source in sources:
                        for j, option in enumerate(self.proc.pipeline.forwarder[name]):
                            if option is None: continue
                            if option[0] == data[source]:
                                data[source] = option[1]
                                break



                passed = self.execute(operation,data,module)


                if passed is not None:
                    for j, passed_name in enumerate(passed): # passed output should always be a dict
                        self.proc.pipeline.current[len(self.proc.pipeline.stages) - index - 1].data[passed_name] = {"type":"register.value", "value":passed[passed_name]}
                        if self.static.components[name]["forwarded"]:
                            if j == 0: # on first passed
                                if dest is None: # if there is not a destination an error will throw because forwarders are meant to get things that haven't been put to regs yet
                                    log(f"Instruction {current} missing \'dest\' operand argument required for append to forwarder.", LogLevel.ERROR)
                                self.proc.pipeline.forwarder[name].insert(0,[dest,passed[passed_name]])
                                forward_incremented.append(name)
                            else: # in case more than one passed
                                log(f"Instruction {current} requested passing more than one instruction into a forwarder, which is not supported.", LogLevel.ERROR)
                                self.proc.pipeline.forwarder[name].insert(0,None)
                                forward_incremented.append(name)
                        
                # add new section here to deal with immediates and other instructions which modify the queue




                    print(passed) # for passed objects debug
                else:
                    if self.static.components[name]["forwarded"]:
                        self.proc.pipeline.forwarder[name].insert(0,None)
                        forward_incremented.append(name)
                # checks if forwarder is gone too long
                
            print(self.proc.pipeline.forwarder)
                
            

            for temp in self.proc.pipeline.forwarder: # update all forwards
                if temp not in forward_incremented: # except those which have already been updated this cycle
                    self.proc.pipeline.forwarder[temp].insert(0,None)
                
                if len(self.proc.pipeline.forwarder[temp]) > len(self.proc.pipeline.stages) - self.proc.pipeline.stages.index(self.static.components[temp]["stage"]):
                    self.proc.pipeline.forwarder[temp].pop(-1)

            if prev_clock != self.proc.state.pc:
                ...
            else:
                self.proc.state.pc += 1
            if self.static.simulation_speed == 0:
                time.sleep(0)
            else:
                time.sleep(1000/self.static.simulation_speed)
            input() # just for testing remove once not needed
        
        print(self.proc.state.register[4])
        log("Program Halted, runtime ending", LogLevel.SUCCESS)




    def execute(self, operation, data, module):
        
        instrclass, func = operation.split('.')
        class_ = getattr(module, instrclass.upper())
        passed = eval(f"class_.{func.upper()}(self,{data})")
        return passed