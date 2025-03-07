from utils import *
#this contains any inline function used by the system compiler needed to provide the compiler's features
#such as sysjump, and syscall

#Users you CAN modify and it could provide additional flexibility over the CPU
# however it is not recommended as it doesn't change program to program
systemFuncs = ["sysjump","syscall"]

class SYSJUMP:
    opcode = "sysjump"
    operand_count = 3
    operand_sizes = [8,2,2]
    signage = ["u","u","u"]
    

    def __init__(self,proc,operands): 
        if not proc.getFlag(proc.config["datapoints"]["flags"][operands[1]]): #can choose which flag to use for jump
            proc.setPC(int(operands[0]), True if operands[2] > 0 else False)

class SYSRETURN:
    opcode = "sysreturn"
    operand_count = 0
    operand_sizes = []
    signage = []

    def __init__(self,proc,operands):
        proc.setPC(proc.getCST(),False)