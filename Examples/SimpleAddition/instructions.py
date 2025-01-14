class ADD:
    opcode = "add"
    operand_count = 3
    operand_sizes = [4, 4, 4]
    signage = ["u", "u", "u"]

    def __init__(self, proc, operands):
        proc.setReg(operands[2], proc.getReg(operands[0]) + proc.getReg(operands[1]))
    
class LDI:
    opcode = "ldi"
    operand_count = 2
    operand_sizes = [4, 8]
    signage = ["u", "u"]

    def __init__(self, proc, operands):
        proc.setReg(operands[0], int(operands[1]))

class HLT:
    opcode = "hlt"
    operand_count = 0
    operand_sizes = []
    signage = []

    def __init__(self, proc, operands):
        proc.exportState("output.txt", True)
        proc.stop()
        