from utils import *

class Memory:
    def __init__(self, address: int | str, wordSize: int) -> None:
        self.address = address
        self.wordSize = wordSize
        self.data = 0

    def __repr__(self):
        return f"Memory(Address={self.address}, Data={self.data})"

    def get(self) -> int:
        return self.data
    
    def set(self, data: int) -> None:
        if data < (2 ** self.wordSize):
            self.data = data
        else:
            log("Data out of range", "ERROR")

class LockableMemory(Memory):
    def __init__(self, address: int | str, wordSize: int) -> None:
        super().__init__(address, wordSize)
        self.locked = False

    def lock(self) -> None:
        self.locked = True
    
    def unlock(self) -> None:
        self.locked = False

class AccumulatedMemory(Memory):
    def __init__(self, address: str, wordSize: int, wrappingBehavior: str) -> None:
        super().__init__(-1, wordSize)
        self.wrappingBehavior = wrappingBehavior
        self.address = address

    def set(self, data: int) -> None:
        overFlow = False
        
        self.data += data

        if self.data > (2 ** self.wordSize) - 1:
            overFlow = True
        
        if overFlow:
            if self.wrappingBehavior == "wrap":
                self.data -= (2 ** self.wordSize) - 1
            elif self.wrappingBehavior == "error":
                log("Data out of range", "ERROR")
            elif self.wrappingBehavior == "clamp":
                self.data = (2 ** self.wordSize) - 1

        