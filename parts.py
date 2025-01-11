import time


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
        ...
        # TODO: Dump the processor state to a file

    def dumpState(self) -> None:
        ...
        # TODO: Dump the processor state as a pretty table
        

    def reset(self):
        ...
        # TODO: Reset the processor state

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