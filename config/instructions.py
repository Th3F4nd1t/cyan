from instructionLib import getRegister, setRegister, List

class nop:
    opcode = "0000" # opcode in decimal
    operand_lengths = [0] # Lengths

    def __init__(self, operands):
        return
    
class add:
    opcode = "0001"
    operand_lengths = [3, 3, 3]

    def __init__(self, operands: List[int]) -> bool:
        if setRegister(operands[2], (getRegister(operands[0]) + getRegister(operands[1]))):
            return True
        else:
            return False
        
"""
class <menomic>:
    opcode = <opcode as a string>
    operand_lengths = <list of operand lengths as integers. the engine will push the operands as integers>

    def __init__(self, operands: List[int]) -> bool:
        <code>
        return <True if the instruction was executed successfully, False otherwise>
""" 


