from utils import *
#this contains any inline function used by the system compiler to replace variables, functions, loops etc.
#such as sysjump, and syscall

#Users you CAN modify and it could provide additional flexibility over the CPU 
# however it is not recommended as it doesn't change program to program
systemFuncs = ["sysjump","syscall"]

class SYSJUMP:
    opcode = "sysjmp"
    operand_count = 1
    operand_sizes = [8]
    signage = ["u","u"]
    

    def __init__(self,proc,operands):
        if not proc.getFlag('zero'):
            proc.setPC(int(operands[0]), False)

class SYSRETURN:
    opcode = "sysreturn"
    operand_count = 0
    operand_sizes = []
    signage = []

    def __init__(self,proc,operands):
        proc.setPC(proc.getCST(),False)