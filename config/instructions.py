class nop:
    opcode = "nop"
    operand_count = 0

    def __init__(self, proc, operands):
        return
    
class add:
    opcode = "add"
    operand_count = 3

    def __init__(self, proc, operands):
        proc.setReg(operands[2], proc.getReg(operands[0]) + proc.getReg(operands[1]))
        return True
        
"""
class <menomic>:
    opcode = <opcode as a string>
    operand_count = <number of expected operands>

    def __init__(self, proc: Processor, operands: list[int]) -> bool:
        <code>
        return <True if the instruction was executed successfully, False otherwise>
""" 


