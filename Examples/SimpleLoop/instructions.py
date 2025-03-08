class SUB: #subtracts a - b
    opcode = "sub"
    operand_count = 3
    operand_sizes = [4, 4, 4]
    signage = ["u", "u", "u"] 

    def __init__(self, proc, operands):
        proc.setReg(operands[0], proc.getReg(operands[1]) - proc.getReg(operands[2]),True)
    
class LDI:
    opcode = "ldi"
    operand_count = 2
    operand_sizes = [4, 8]
    signage = ["u", "u"]

    def __init__(self, proc, operands):
        proc.setReg(operands[0], int(operands[1]),False)

class HLT:
    opcode = "hlt"
    operand_count = 0
    operand_sizes = []
    signage = []

    def __init__(self, proc, operands):
        proc.exportState("output.txt", True)
        proc.stop()

class JMP:
    opcode = "jmp"
    operand_count = 3
    operand_sizes = [8,2,2]
    signage = ["u","u","u"]
    

    def __init__(self,proc,operands): 
        if not proc.getFlag(proc.config["datapoints"]["flags"][operands[1]]):  #can choose which flag to use for jump
            proc.setPC(int(operands[0]), True if operands[2] > 0 else False)



#flags
class zero:
    def get(value) -> bool:
        return value == 0