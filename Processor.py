import os
import sys
import time
from utils import *
from memory import *
from config import *

class Processor:
    def __init__(self, config: dict, stateDict: dict = None) -> None:
        """The class constructor for any processor to be used with CYAN."

        Args:
            config (dict): The configuration dictionary for the processor.
            stateDict (dict, optional): The state to start in, if any. If incorrectly formatted, things may break. Defaults to None.
        """
        # IMPORTANT STUFF
        validateConfig(config, 1)

        self.config = config
        if stateDict is not None:
            self.state = stateDict
        else:
            self.state = []; self.initState()
        self.program = None
        self.instructionFile = None
        self.isRunning = False
        self.parsedProgram = None

    def initState(self) -> dict:
        """Initialize the processor state with default values."""

        self.state = {
            "ram" : [],
            "prom" : [],
            "registers" : [],
            "io" : [],
            "pc" : 0
        }

        for i in range(0, int(self.config["datapoints"]["ram"])):
            self.state["ram"].append(Memory(i, self.config["datapoints"]["word_size"]))

        for i in range(0, int(self.config["datapoints"]["prom"])):
            self.state["prom"].append(Memory(i, self.config["datapoints"]["opcode_size"] + self.config["datapoints"]["operand_count"] * self.config["datapoints"]["operand_size"]))

        for i in range(0, int(self.config["datapoints"]["registers"])): 
            self.state["registers"].append(Memory(i, self.config["datapoints"]["word_size"]))

        try:
            for i in range(0, int(self.config["datapoints"]["io_count"])):
                self.state["io"].append(LockableMemory(i, self.config["datapoints"]["io_size"]))
        except KeyError:
            print("No io defined in config. Skipping.")

        try:
            if self.config["datapoints"]["speed"] is None:
                pass
        except Exception as e:
            log("No speed defined in config. Defaulting to 0.")

        log("Initialized state.")
        return self.state
    
    def run(self):
        log("Starting processor.")
        self.isRunning = True
        while self.isRunning:
            log(f"Executing instruction at {self.state['pc']}")
            temp = self.execute()
            log(f"Instruction executed: {temp}")
            try:
                time.sleep(0.1 * self.config["speed"])
            except: 
                pass

    def Stop(self):
        log("Stopping processor.")
        self.isRunning = False

    def exportState(self, filePath: str, pretty: bool) -> bool:
        log(f"Exporting state to {filePath}")

        # RAM
        ramHeader = str("RAM:\n")
        ramBody = "| "
        for i, ram in enumerate(self.state["ram"]):
            padding = " " * ((len(str(self.config["datapoints"]["ram"])) + 3) - (len(str(self.state["ram"][i].Get())) + len(str(i))))
            ramBody += f"{i}: {padding} {ram.Get()} | "
            if (i + 1) % 10 == 0:
                ramBody += "\n| "

        #PROM
        romHeader = str("\nProgram ROM:\n")
        romBody = "| "
        for i, rom in enumerate(self.state["prom"]):
            padding = " " * ((len(str(self.config["datapoints"]["prom"])) + 3) - (len(str(self.state["prom"][i].Get())) + len(str(i))))
            romBody += f"{i}: {padding} {rom.Get()}  | "
            if (i + 1) % 10 == 0:
                romBody += "\n| "
        

        # REGISTERS
        regHeader = str("\nRegisters:\n")
        regBody = "| "
        for i, reg in enumerate(self.state["registers"]):
            padding = " " * ((len(str(self.config["datapoints"]["registers"])) + 3) - (len(str(self.state["registers"][i].Get())) + len(str(i))))
            regBody += f"{i}: {padding} {reg.Get()}  | "
            if (i + 1) % 3 == 0:
                regBody += "\n| "

        # I/O PORTS
        portsHeader = str("\nI/O Ports:\n")
        portsBody = "| "
        for i, ports in enumerate(self.state["io"]):
            padding = " " * ((len(str(self.config["datapoints"]["io_count"])) + 3) - (len(str(self.state["io"][i].Get())) + len(str(i))))
            portsBody += f"{i}: {padding} {ports.Get()}  | "
            if (i + 1) % 3 == 0:
                portsBody += "\n| "

        try:
            with open(filePath, "w") as f:
                if pretty == False:
                        f.write(str(self.state))
                else:
                    f.write(ramHeader)        
                    f.write(ramBody + "\n")

                    f.write(romHeader)        
                    f.write(romBody + "\n")

                    f.write(regHeader)        
                    f.write(regBody + "\n")

                    f.write(portsHeader)        
                    f.write(portsBody + "\n")
                    
                return True
        except Exception as e:
            print(e)
            return False

    def dumpState(self) -> None:
        log("Dumping state.")
        dumpOutput(dict_of_lists_to_pretty_string(self.state))

    def reset(self):
        self.initState()

    def execute(self) -> bool:
        log("Executing instruction.")
        if self.program is None:
            print("No program loaded.")
            return False
        line = self.program[self.state["pc"]]
        log(f"Executing instruction: {line}")
        
        opcode = line[:3]
        if not (opcode in self.config["metadata"]["operations"]):
            error(f"Unknown opcode: {opcode}")
        log(f"Opcode: {opcode}")
        
        sys.path.append(f"{os.getcwd()}/configGroup") 
        module = __import__("instructions")

        class_ = getattr(module, opcode)
        instr_class = class_
        log(f"Instruction class: {instr_class}")

        operands = line[4:].split(" ")
        if operands == [""]:
            operands = []
        if len(operands) != instr_class.operand_count:
            error(f"Expected {instr_class.operand_count} operands, got {len(operands)}")
    
        for i in range(0, len(operands)):
            try:
                operands[i] = int(operands[i])
            except Exception as e:
                error(f"Invalid operand {operands[i]} at index {i}")

        log(f"Operands: {operands}")


        instr_class(self, operands)
        return True

    def loadProgram(self, programFile: str) -> bool:
        log(f"Loading program from {programFile}")
        try:
            with open(programFile, "r") as f:
                self.program = f.readlines()
                
        except Exception as e:
            print(e)
            return False
        
        for index, line in enumerate(self.program):
            self.program[index] = self.program[index].strip("\n")

    def SetInstructionsFile(self, instructionsFile: str) -> bool:
        log(f"Setting instructions file to {instructionsFile}")
        self.instructionsFile = instructionsFile
        return True

    def SetReg(self, address: int, data: int) -> None:
        log(f"Setting register {address} to {data}")
        self.state["registers"][address].Set(data)
    
    def SetIO(self, address: int, data: int) -> None:
        log(f"Setting IO {address} to {data}")
        self.state["io"][address].Set(data)

    def SetRAM(self, address: int, data: int) -> None:
        log(f"Setting RAM {address} to {data}")
        self.state["ram"][address].Set(data)


    def GetReg(self, address: int) -> int:
        log(f"Getting register {address}")
        return self.state["registers"][address].Get()
    
    def GetIO(self, address: int) -> int:
        log(f"Getting IO {address}")
        return self.state["io"][address].Get()
    
    def GetRAM(self, address: int) -> int:
        log(f"Getting RAM {address}")
        return self.state["ram"][address].Get()
    
    def GetProm(self, address: int) -> int:
        log(f"Getting PROM {address}")
        return self.state["prom"][address].Get()

    def SetIOLock(self, address: int, lockState: bool) -> None:
        log(f"Setting IO {address} lock to {lockState}")
        if lockState:
            self.state["io"][address].Lock()
        else:
            self.state["io"][address].Unlock()
    

    def GetPC(self) -> int:
        log("Getting PC")
        return self.state["pc"]
    
    def SetPC(self, address: int) -> None:
        log(f"Setting PC to {address}")
        self.state["pc"] = address

    def OffsetPC(self, offset: int) -> None:
        log(f"Offsetting PC by {offset}")
        self.state["pc"] += offset

    def IncrementPC(self) -> None:
        log("Incrementing PC")
        self.state["pc"] += 1
