class add:
    opcode = "add"
    operand_count = 3

    def __init__(self, proc, operands):
        proc.setReg(operands[2], proc.getReg(operands[0]) + proc.getReg(operands[1]))
        proc.incrementPC()
        # proc.dumpState()
    
class ldi:
    opcode = "ldi"
    operand_count = 2

    def __init__(self, proc, operands):
        proc.setReg(operands[0], int(operands[1]))
        proc.incrementPC()

class hlt:
    opcode = "hlt"
    operand_count = 0

    def __init__(self, proc, operands):
        proc.exportState("output.txt")
        proc.stop()
        