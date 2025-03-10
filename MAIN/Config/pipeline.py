# example file, will have docs so the user knows how to use (after we figure it out first). Try to keep simple.

from typing import List
# each function in the pipeline takes the instruction, and returns what said instruction should have at this stage
# this will require a defined instruction class which isn't defined yet so for now just leave as is

class Pipeline:
    pipeline = [
        "InstructionFetch",
        "InstructionDecode",
        "Execute",
        "Memory Access",
        "Writeback"
    ]


    def __init__(self, instruction):
        ...
    
    def InstructionFetch(self, instruction):
        ...
    
    def InstructionDecode(self, instruction):
        ...
    
    def Execute(self, instruction):
        ...

    def MemoryAccess(self, instruction):
        ...

    def Writeback(self, instruction):
        ...