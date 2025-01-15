from utils import *

class Memory:
    def __init__(self, address: int | str, wordSize: int, error: bool = False) -> None:
        self.address = address
        self.wordSize = wordSize
        self.data = 0
        self.error = error

    def __repr__(self):
        return f"Memory(Address={self.address}, Data={self.data})"

    def get(self) -> int:
        return self.data
    
    def set(self, data: int) -> None:
        if data < (2 ** self.wordSize):
            self.data = data
        elif not self.error:
            self.data = data % (2 ** self.wordSize)
        else:
            log("Data out of range", "ERROR")

class LockableMemory(Memory):
    def __init__(self, address: int | str, wordSize: int, error: bool) -> None:
        super().__init__(address, wordSize, error)
        self.locked = False

    def lock(self) -> None:
        self.locked = True
    
    def unlock(self) -> None:
        self.locked = False

class AccumulatedMemory(Memory):
    def __init__(self, address: str, wordSize: int, error: bool) -> None:
        super().__init__(-1, wordSize)
        self.error = error
        self.address = address

    def set(self, data: int) -> None:
        overFlow = False
        
        self.data += data

        if self.data > (2 ** self.wordSize) - 1:
            overFlow = True
        
        if overFlow:
            if not self.error:
                self.data -= (2 ** self.wordSize) - 1
            else:
                log("Data out of range", "ERROR")

        