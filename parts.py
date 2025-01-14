import os
import sys
import time
from utils import *

class Processor:
    def __init__(self, config: dict, stateDict: dict = None) -> None:
        """The class constructor for any processor to be used with CYAN."

        Args:
            config (dict): The configuration dictionary for the processor.
            stateDict (dict, optional): The state to start in, if any. If incorrectly formatted, things may break. Defaults to None.
        """
        # IMPORTANT STUFF
        self.logValue = True # CSP EXAM. This is a variable that determines if the log function should print the messages to the console. It's boolean, either True or False.

        self.config = config

        # CSP EXAM. stateDict is an argument variable passed. It defaults to None when there isn't a dictionary passed and this small if statement checks if it needs to run the initState() function to create a state dictionary.
        if stateDict is not None:
            self.state = stateDict
        else:
            self.state = []; self.initState()

        
        self.program = None
        self.instructionFile = None
        self.isRunning = False
        self.parsedProgram = None

    def log(self, message: str) -> None:
        if self.logValue:
            print(message)


    def initState(self) -> dict:
        """Initialize the processor state with default values."""

        # CSP EXAM. self.state is a dictionary that stores various lists and integers that represent the current data stored across the processor.
        self.state = {
            "ram" : [],
            "dcache" : [],
            "prom" : [],
            "icache" : [],
            "registers" : [],
            "io" : [],
            "pc" : 0
        }

        for i in range(0, int(self.config["datapoints"]["ram"])):
            self.state["ram"].append(ram(i, self.config["datapoints"]["word_size"]))

        try:
            for i in range(0, int(self.config["datapoints"]["dcache"])):
                self.state["dcache"].append(dcache(0, self.config["datapoints"]["word_size"]))
        except KeyError:
            print("No dcache defined in config. Skipping.")

        for i in range(0, int(self.config["datapoints"]["prom"])):
            self.state["prom"].append(prom(i, self.config["datapoints"]["opcode_size"] + self.config["datapoints"]["operand_count"] * self.config["datapoints"]["operand_size"]))

        try:
            for i in range(0, int(self.config["datapoints"]["icache"])):
                self.state["icache"].append(icache(i, self.config["datapoints"]["opcode_size"] + self.config["datapoints"]["operand_count"] * self.config["datapoints"]["operand_size"]))
        except KeyError:
            print("No icache defined in config. Skipping.")

        for i in range(0, int(self.config["datapoints"]["registers"])): 
            self.state["registers"].append(register(i, self.config["datapoints"]["word_size"]))

        try:
            for i in range(0, int(self.config["datapoints"]["io_count"])):
                self.state["io"].append(io(i, self.config["datapoints"]["io_size"]))
        except KeyError:
            print("No io defined in config. Skipping.")

        self.log("Initialized state.")
        return self.state

    def run(self):
        self.log("Starting processor.")
        self.isRunning = True
        while self.isRunning: # CSP EXAM. This loop is the main loop that goes through all the lines in the program file and parses and executes them with the self.execute() function.
            self.log(f"Executing instruction at {self.state['pc']}")
            temp = self.execute()
            self.log(f"Instruction executed: {temp}")
            try:
                time.sleep(0.1 * self.config["speed"])
            except KeyError:
                self.log("No speed defined in config. Defaulting to 0.")

    def stop(self):
        self.log("Stopping processor.")
        self.isRunning = False

    def exportState(self, filePath: str) -> bool:
        self.log(f"Exporting state to {filePath}")
        try:
            with open(filePath, "w") as f:
                f.write(str(self.state))
                return True
        except Exception as e:
            print(e)
            return False

    def dumpState(self) -> None:
        self.log("Dumping state.")
        dumpOutput(dict_of_lists_to_pretty_string(self.state))

    def reset(self):
        self.initState()

    def execute(self) -> bool:
        self.log("Executing instruction.")
        if self.program is None:
            print("No program loaded.")
            return False
        line = self.program[self.state["pc"]]
        self.log(f"Executing instruction: {line}")
        
        opcode = line[:3]
        if not (opcode in self.config["metadata"]["operations"]):
            print(f"Unknown opcode: {opcode}")
            return False
        self.log(f"Opcode: {opcode}")
        
        sys.path.append(f"{os.getcwd()}/configGroup") 
        module = __import__("instructions")

        class_ = getattr(module, opcode)
        instr_class = class_
        self.log(f"Instruction class: {instr_class}")
        
        # The operands list is used to pass the arguments of each instruction into the instruction class for the execution. There is some cleaning of it as well as some length checking. It also get's turned into integers.
        operands = line[4:].split(" ")
        if operands == [""]:
            operands = []
        if len(operands) != instr_class.operand_count:
            print(f"Expected {instr_class.operand_count} operands, got {len(operands)}")
            return False
    
        for i in range(0, len(operands)):
            operands[i] = int(operands[i])

        self.log(f"Operands: {operands}")


        instr_class(self, operands)
        return True

    def loadProgram(self, programFile: str) -> bool:
        self.log(f"Loading program from {programFile}")
        try:
            with open(programFile, "r") as f:
                self.program = f.readlines()
                
        except Exception as e:
            print(e)
            return False
        
        for index, line in enumerate(self.program): # CSP EXAM. This for loop goes through all the lines in the program file and turn them into a list and remove the newline character as a first round of cleaning.
            self.program[index] = self.program[index].strip("\n")

    def setInstructionsFile(self, instructionsFile: str) -> bool:
        self.log(f"Setting instructions file to {instructionsFile}")
        self.instructionsFile = instructionsFile
        return True

    def setReg(self, address: int, data: int) -> None:
        self.log(f"Setting register {address} to {data}")
        self.state["registers"][address].set(data)
    
    def setIO(self, address: int, data: int) -> None:
        self.log(f"Setting IO {address} to {data}")
        self.state["io"][address].set(data)

    def setRAM(self, address: int, data: int) -> None:
        self.log(f"Setting RAM {address} to {data}")
        self.state["ram"][address].set(data)


    def getReg(self, address: int) -> int:
        self.log(f"Getting register {address}")
        return self.state["registers"][address].get()
    
    def getIO(self, address: int) -> int:
        self.log(f"Getting IO {address}")
        return self.state["io"][address].get()
    
    def getRAM(self, address: int) -> int:
        self.log(f"Getting RAM {address}")
        return self.state["ram"][address].get()
    
    def getProm(self, address: int) -> int:
        self.log(f"Getting PROM {address}")
        return self.state["prom"][address].get()
    
    def setRegLock(self, address: int, lockState: bool) -> None:
        self.log(f"Setting register {address} lock to {lockState}")
        if lockState:
            self.state["registers"][address].lock()
        else:
            self.state["registers"][address].unlock()

    def setIOLock(self, address: int, lockState: bool) -> None:
        self.log(f"Setting IO {address} lock to {lockState}")
        if lockState:
            self.state["io"][address].lock()
        else:
            self.state["io"][address].unlock()
    

    def getPC(self) -> int:
        self.log("Getting PC")
        return self.state["pc"]
    
    def setPC(self, address: int) -> None:
        self.log(f"Setting PC to {address}")
        self.state["pc"] = address

    def offSetPC(self, offset: int) -> None:
        self.log(f"Offsetting PC by {offset}")
        self.state["pc"] += offset

    def incrementPC(self) -> None:
        self.log("Incrementing PC")
        self.state["pc"] += 1


    def getDCache(self, address: int) -> int:
        return self.state["dcache"][address].get()
    
    def getICache(self, address: int) -> int:
        return self.state["icache"][address].get()
    
    def setDCache(self, address: int, data: int) -> None:
        self.state["dcache"][address].set(data)

    def setICache(self, address: int, data: int) -> None:
        self.state["icache"][address].set(data)


# Hardware classes
class dcache:
    def __init__(self, address: int, word_size: int) -> None:
        self.address = address
        self.word_size = word_size
        self.data = 0

    def __repr__(self):
        return f"Dcache(address={self.address}, data={self.data})"

    def get(self) -> int:
        return self.data
    
    def set(self, data: int) -> None:
        self.data = data

class icache:
    def __init__(self, address: int, word_size: int) -> None:
        self.address = address
        self.word_size = word_size
        self.data = 0

    def __repr__(self):
        return f"Icache(address={self.address}, data={self.data})"
    
    def get(self) -> int:
        return self.data
    
    def set(self, data: int) -> None:
        self.data = data

class ram:
    def __init__(self, address: int, word_size: int) -> None:
        self.address = address
        self.word_size = word_size
        self.data = 0

    def __repr__(self):
        return f"Ram(address={self.address}, data={self.data})"

    def get(self) -> int:
        return self.data
    
    def set(self, data: int) -> None:
        self.data = data

class prom:
    def __init__(self, address: int, word_size: int) -> None:
        self.address = address
        self.word_size = word_size
        self.data = 0

    def __repr__(self):
        return f"Prom(address={self.address}, data={self.data})"

    def get(self) -> int:
        return self.data
    

class register:
    def __init__(self, address: int, word_size: int) -> None:
        self.address = address
        self.word_size = word_size
        self.data = 0
        self.locked = False

    def __repr__(self):
        return f"Register(address={self.address}, data={self.data}, locked={self.locked})"

    def get(self) -> int:
        return self.data
    
    def set(self, data: int) -> None:
        self.data = data

    def lock(self) -> None:
        self.locked = True

    def unlock(self) -> None:
        self.locked = False

class io:
    def __init__(self, address: int, size: int) -> None:
        self.address = address
        self.size = size
        self.data = 0
        self.locked = False

    def __repr__(self):
        return f"IO(address={self.address}, data={self.data}, locked={self.locked})"

    def get(self) -> int:
        return self.data
    
    def set(self, data: int) -> None:
        self.data = data

    def lock(self) -> None:
        self.locked = True

    def unlock(self) -> None:
        self.locked = False
