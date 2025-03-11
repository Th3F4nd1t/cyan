from typing import List, Any


# no classes in components.py should have an init function
# they should just contain the operations and the operands which are given to it
class Pipeline: # this is inherited by the pipeline class inside processor
    stages = {
        "InstructionFetch": 0,
        "InstructionDecode": 1,
        "Execute": 2,
        "Memory Access": 3,
        "Writeback": 4
    }


class ALU:
    operands = ["src1","src2"]
    processor_req = []

    def Add(self, num1, num2):
        # add timing stuff
        return num1+num2
    
    def Sub(self,num1,num2):

        return num1-num2
    
    def And(self,num1,num2):
        
        return num1&num2

    def Or(self,num1,num2):

        return num1|num2

    def Xor(self,num1,num2):

        return num1 ^ num2


class PC:
    operands_req = ["flag"]
    proccessor_req = ["flags"]

    def Jmp(self,flag,proc_flags):
        if not proc_flags[flag]:
            return True
        return False

