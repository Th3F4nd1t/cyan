import time
from utils import *

class Processor:
    def __init__(self, config: dict, stateDict: dict = None) -> None:
        """The class constructor for any processor to be used with CYAN."

        Args:
            config (dict): The configuration dictionary for the processor.
            stateDict (dict, optional): The state to start in, if any. If incorrectly formatted, things may break. Defaults to None.
        """
        self.config = config
        if stateDict is not None:
            self.state = stateDict
        else:
            self.state = []; self.initState()
        self.programFile = None
        self.instructionFile = None
        self.isRunning = False
        self.parsedProgram = None

    def initState(self) -> dict:
        """Initialize the processor state with default values."""

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

        return self.state
    
    def step(self):
        ...
        # TODO: Implement processor state transition and instruction execution

    def run(self):
        self.isRunning = True
        while self.isRunning:
            self.step()
            time.sleep(0.1 * self.config["speed"])

    def stop(self):
        self.isRunning = False

    def exportState(self, filePath: str) -> bool:
        try:
            with open(filePath, "w") as f:
                f.write(str(self.state))
                return True
        except Exception as e:
            return False

    def dumpState(self) -> None:
        dumpOutput(self.state)
        

    def reset(self):
        self.initState()

    def execute(self, instruction: str) -> None:
        ...
        # TODO: Implement instruction execution

    def loadProgram(self, programFile: str) -> bool:
        self.programFile = programFile
        ...

    def setInstructionsFile(self, instructionsFile: str) -> bool:
        self.instructionsFile = instructionsFile
        ...

    def parse(self):
        ...

    def setReg(self, address: int, data: list) -> None:
        self.state["registers"][address].set(data)
    
    def setIO(self, address: int, data: list) -> None:
        self.state["io"][address].set(data)

    def setRAM(self, address: int, data: list) -> None:
        self.state["ram"][address].set(data)

    def setDCache(self, address: int, data: list) -> None:
        self.state["dcache"][address].set(data)

    def setICache(self, address: int, data: list) -> None:
        self.state["icache"][address].set(data)


    def getReg(self, address: int) -> list:
        return self.state["registers"][address].get()
    
    def getIO(self, address: int) -> list:
        return self.state["io"][address].get()
    
    def getRAM(self, address: int) -> list:
        return self.state["ram"][address].get()
    
    def getDCache(self, address: int) -> list:
        return self.state["dcache"][address].get()
    
    def getICache(self, address: int) -> list:
        return self.state["icache"][address].get()
    
    def getProm(self, address: int) -> list:
        return self.state["prom"][address].get()
    
    def setRegLock(self, address: int, lockState: bool) -> None:
        if lockState:
            self.state["registers"][address].lock()
        else:
            self.state["registers"][address].unlock()

    def setIOLock(self, address: int, lockState: bool) -> None:
        if lockState:
            self.state["io"][address].lock()
        else:
            self.state["io"][address].unlock()
    

    def getPC(self) -> int:
        return self.state["pc"]
    
    def setPC(self, address: int) -> None:
        self.state["pc"] = address

class ram:
    def __init__(self, address: int, word_size: int) -> None:
        self.address = address
        self.word_size = word_size
        self.data = [0] * self.word_size

    def get(self) -> list:
        return self.data
    
    def set(self, data: list) -> None:
        self.data = data

class dcache:
    def __init__(self, address: int, word_size: int) -> None:
        self.address = address
        self.word_size = word_size
        self.data = [0] * self.word_size

    # TODO

class prom:
    def __init__(self, address: int, word_size: int) -> None:
        self.address = address
        self.word_size = word_size
        self.data = [0] * self.word_size

    def get(self) -> list:
        return self.data

class icache:
    def __init__(self, address: int, word_size: int) -> None:
        self.address = address
        self.word_size = word_size
        self.data = [0] * self.word_size

    # TODO

class register:
    def __init__(self, address: int, word_size: int) -> None:
        self.address = address
        self.word_size = word_size
        self.data = [0] * self.word_size
        self.locked = False

    def get(self) -> list:
        return self.data
    
    def set(self, data: list) -> None:
        self.data = data

    def lock(self) -> None:
        self.locked = True

    def unlock(self) -> None:
        self.locked = False

class io:
    def __init__(self, address: int, size: int) -> None:
        self.address = address
        self.size = size
        self.data = [0] * self.size
        self.locked = False

    def get(self) -> list:
        return self.data
    
    def set(self, data: list) -> None:
        self.data = data

    def lock(self) -> None:
        self.locked = True

    def unlock(self) -> None:
        self.locked = False