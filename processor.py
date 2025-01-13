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
        resetLogger()
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
            log("No speed defined in config. Defaulting to 0.", "WARNING")

        log("Initialized state.", "INFO")
        return self.state
    
    def run(self):
        log("Starting processor.", "INFO")
        self.isRunning = True
        while self.isRunning:
            # Remove whitespace before the line
            line = self.program[self.state["pc"]]
            while line.startswith(" "):
                line = line[1:]

            # Check for comments or empty lines
            if line.startswith(";") or line.startswith("\n") or line.startswith(""):
                self.state["pc"] += 1

            if line.includes(";"):
                line = line.split(";")[0]
            
            else:
                log(f"Executing instruction at {self.state['pc']}", "INFO")
                rpc = self.state["pc"]
                temp = self.execute()
                if self.state["pc"] == rpc:
                    self.state["pc"] += 1
                log(f"Instruction executed: {temp}", "INFO")

                try:
                    time.sleep(0.1 * self.config["speed"])
                except: 
                    pass

    def stop(self):
        log("Stopping processor.", "INFO")
        self.isRunning = False

    def exportState(self, filePath: str, pretty: bool) -> bool:
        log(f"Exporting state to {filePath}", "INFO")

        # RAM
        ramHeader = str("RAM:\n")
        ramBody = "| "
        for i, ram in enumerate(self.state["ram"]):
            padding = " " * ((len(str(self.config["datapoints"]["ram"])) + 3) - (len(str(self.state["ram"][i].get())) + len(str(i))))
            ramBody += f"{i}: {padding} {ram.get()} | "
            if (i + 1) % 10 == 0:
                ramBody += "\n| "

        #PROM
        romHeader = str("\nProgram ROM:\n")
        romBody = "| "
        for i, rom in enumerate(self.state["prom"]):
            padding = " " * ((len(str(self.config["datapoints"]["prom"])) + 3) - (len(str(self.state["prom"][i].get())) + len(str(i))))
            romBody += f"{i}: {padding} {rom.get()}  | "
            if (i + 1) % 10 == 0:
                romBody += "\n| "
        

        # REGISTERS
        regHeader = str("\nRegisters:\n")
        regBody = "| "
        for i, reg in enumerate(self.state["registers"]):
            padding = " " * ((len(str(self.config["datapoints"]["registers"])) + 3) - (len(str(self.state["registers"][i].get())) + len(str(i))))
            regBody += f"{i}: {padding} {reg.get()}  | "
            if (i + 1) % 3 == 0:
                regBody += "\n| "

        # I/O PORTS
        portsHeader = str("\nI/O Ports:\n")
        portsBody = "| "
        for i, ports in enumerate(self.state["io"]):
            padding = " " * ((len(str(self.config["datapoints"]["io_count"])) + 3) - (len(str(self.state["io"][i].get())) + len(str(i))))
            portsBody += f"{i}: {padding} {ports.get()}  | "
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
        log("Dumping state.", "INFO")
        dumpOutput(dict_of_lists_to_pretty_string(self.state))

    def reset(self):
        self.initState()

    def execute(self) -> bool:
        log("Executing instruction.", "INFO")
        if self.program is None:
            print("No program loaded.", "WARNING")
            return False
        line = self.program[self.state["pc"]]
        log(f"Executing instruction: {line}", "INFO")
        
        line = line.split(" ")
        opcode = line[0]
        if not (opcode in self.config["metadata"]["operations"]):
            log(f"Unknown opcode: {opcode}", "ERROR")
        log(f"Opcode: {opcode}", "INFO")
        
        sys.path.append(f"{os.getcwd()}/configGroup") 
        module = __import__("instructions")

        class_ = getattr(module, opcode.upper())
        instr_class = class_
        log(f"Instruction class: {instr_class}", "INFO")

        operands = line[1:]
        for operand in operands:
            if operand == "":
                operands.remove(operand)

        if isSizedCorrectly(instr_class.operand_sizes, operands) == False:
            log("Operand size mismatch.", "ERROR")
        else:
            log("Operand size match.", "INFO")

        if len(operands) != instr_class.operand_count:
            log(f"Expected {instr_class.operand_count} operands, got {len(operands)}", "ERROR")
    
        for i in range(0, len(operands)):
            try:
                operands[i] = int(operands[i])
            except Exception as e:
                log(f"Invalid operand {operands[i]} at index {i}", "ERROR")

        log(f"Operands: {operands}", "INFO")


        instr_class(self, operands)
        return True

    def loadProgram(self, programFile: str) -> bool:
        log(f"Loading program from {programFile}", "INFO")
        try:
            with open(programFile, "r") as f:
                self.program = f.readlines()
                
        except Exception as e:
            print(e)
            return False
        
        for index, line in enumerate(self.program):
            self.program[index] = self.program[index].strip("\n")

    def setInstructionsFile(self, instructionsFile: str) -> bool:
        log(f"Setting instructions file to {instructionsFile}", "INFO")
        self.instructionsFile = instructionsFile
        return True

    def setReg(self, address: int, data: int) -> None:
        log(f"Setting register {address} to {data}", "INFO")
        self.state["registers"][address].set(data)
    
    def setIO(self, address: int, data: int) -> None:
        log(f"Setting IO {address} to {data}", "INFO")
        self.state["io"][address].set(data)

    def setRAM(self, address: int, data: int) -> None:
        log(f"Setting RAM {address} to {data}", "INFO")
        self.state["ram"][address].set(data)


    def getReg(self, address: int) -> int:
        log(f"Getting register {address}", "INFO")
        return self.state["registers"][address].get()
    
    def getIO(self, address: int) -> int:
        log(f"Getting IO {address}", "INFO")
        return self.state["io"][address].get()
    
    def getRAM(self, address: int) -> int:
        log(f"Getting RAM {address}", "INFO")
        return self.state["ram"][address].get()
    
    def getProm(self, address: int) -> int:
        log(f"Getting PROM {address}", "INFO")
        return self.state["prom"][address].get()

    def setIOLock(self, address: int, lockState: bool) -> None:
        log(f"Setting IO {address} lock to {lockState}", "INFO")
        if lockState:
            self.state["io"][address].lock()
        else:
            self.state["io"][address].unlock()
    

    def getPC(self) -> int:
        log("Getting PC", "INFO")
        return self.state["pc"]
    
    def setPC(self, address: int) -> None:
        log(f"Setting PC to {address}", "INFO")
        self.state["pc"] = address

    def offsetPC(self, offset: int) -> None:
        log(f"Offsetting PC by {offset}", "INFO")
        self.state["pc"] += offset

    def incrementPC(self) -> None:
        log("Incrementing PC", "INFO")
        self.state["pc"] += 1
