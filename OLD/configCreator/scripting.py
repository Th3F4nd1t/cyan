def convertToPythonInstruction(input: str) -> str:
    """
    instr INSTRUCTION_NAME
    
    // comment
    
    py start
    some python code
    py end

    setreg: addr, data optional_setflags



    """

# #### Memory
# - `setReg(address: int, data: int, bool setFlags) -> none`
# - `setRAM(address: int, data: int, bool setFlags) -> none`
# - `setCustomReg(name: str, data: int, bool setFlags) -> none`
# - `getReg(address: int) -> int`
# - `getRAM(address: int) -> int`
# - `getProm(address: int) -> int`
# - `getCustomReg(address: int) -> int`

# ### Flags
# - `getFlag(name: str) -> bool`

# #### Input/Output
# - `setIO(address: int, data: int) -> none`
# - `getIO(address: int) -> int`
# - `setIOLock(address: int, lockState: bool) -> none`

# #### Program Counter
# - `getPC() -> int`
# - `setPC(address: int) -> none`
# - `offsetPC(offset: int) -> none`
# - `incrementPC() -> none`

# #### Internal Methods (DO NOT USE)
# - `initState() -> none`
# - `initFlags() -> none`
# - `updateFlags() -> none`
# - `executeLine() -> none`
# - `execute() -> bool`