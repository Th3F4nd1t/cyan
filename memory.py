import math

class Memory:
    def __init__(self, address: int, wordSize: int) -> None:
        self.address = address
        self.wordSize = wordSize
        self.data = 0

    def __repr__(self):
        return f"Memory(Address={self.address}, Data={self.data})"

    def Get(self) -> int:
        return self.data
    
    def Set(self, data: int) -> None:
        if data < math.pow(2, self.wordSize):
            self.data = data
        else:
            raise ValueError("Data out of range")

class LockableMemory(Memory):
    def __init__(self, address: int, wordSize: int) -> None:
        super().__init__(address, wordSize)
        self.locked = False

    def Lock(self) -> None:
        self.locked = True
    
    def Unlock(self) -> None:
        self.locked = False