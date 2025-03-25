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

            print()
            pipeline_iterator = zip(list(reversed(self.proc.pipeline.current)),list(reversed(self.proc.pipeline.stages)))
            for instruction, stage in pipeline_iterator:
                if instruction == '': 
                    for component in list(self.proc.pipeline.forwarder.keys()):
                        self.proc.pipeline.forwarder[component][self.proc.pipeline.stages.index(stage)] = None
                    continue

                stage_index = self.proc.pipeline.stages.index(stage)
                operation = instruction.execution_chain[stage]
                name = operation.split('.')[0].upper()

                data = {}
                destination = None

                data["flags"] = []
                for flag in instruction.flags:
                    data["flags"].append(flag)


                sources = []
                sources_opcode = []
                for opcode in instruction.data:

                    if instruction.data[opcode]["type"].upper() == "REGISTER.DESTINATION":
                        destination = instruction.data[opcode]["value"]

                    elif instruction.data[opcode]["type"].upper() == "REGISTER.SOURCE":
                        sources_opcode.append(instruction.data[opcode]["value"])
                        sources.append(opcode)

                    data[opcode] = instruction.data[opcode]["value"]

                
                
                # its looping twice but due to the way operands are handled it has to be to avoid missing stuff
                for component in list(self.proc.pipeline.forwarder.keys()):
                    self.proc.pipeline.forwarder[component][stage_index] = None
                    # sets default value to none to overwrite that of previous cycle
                    if destination is None: continue
            
                    # 
                    for opcode in list(reversed(instruction.data)):
                        if opcode in self.static.components[component]["forward_operands"]:
                            self.proc.pipeline.forwarder[component][stage_index] = [destination,data[opcode]]
                            break
                
                if operation.upper() == "NONE": continue # important that tis is after the forwarding creation to not break other instructions
                



                # grab and filter item transfer info from config


                # now checks for things that need to be forwarded to itself
                if self.static.components[name]["forwarded"]:
                    for opcode in sources:
                        for j, temp in enumerate(self.proc.pipeline.forwarder[name][stage_index+1:]):

                            
                            # I need a way to link register.value types and register.source types
                            if temp is None: continue
                            dest_fw, value_fw = temp
                            transfer_hm = self.static.components[name]["transfer"]

                            if instruction.data[opcode]["value"] == dest_fw:
                                if opcode in transfer_hm:
                                    data[transfer_hm[opcode]] = value_fw
                                else:
                                    data[opcode] = value_fw
                                break
            
                # now actually execute instruction

                passed = self.execute(operation,data,module)
                if passed is not None:
                    for passed_name in passed:
                        self.proc.pipeline.current[stage_index].data[passed_name] = {"type":"Register.Value","value":passed[passed_name]}





            self.proc.state.pc += 1
            
            if self.static.simulation_speed == 0:
                time.sleep(0)
            else:
                time.sleep(1000/self.static.simulation_speed)
            input() # just for testing remove once not needed
        
        # print(self.proc.state.register[4]) to test my program
        log("Program Halted, runtime ending", LogLevel.SUCCESS)




    def execute(self, operation, data, module):
        
        instrclass, func = operation.split('.')
        class_ = getattr(module, instrclass.upper())
        passed = eval(f"class_.{func.upper()}(self,{data})")
        return passed