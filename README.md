# CYAN
## License
[CC BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/)
## Features
- Will write this list at the end

## How to Use

### Step by Step
#### 1. Download ZIP
This is self explanatory. Download the zip file from GitHub.
#### 2. Extract
Use your favorite extration tool to put the files in any folder location.
#### 4. Create [Config File](#config-file)
Follow the instructions below to add your configuration for your processor or import one.
#### 5. Create [Instruction File](#instruction-file)
Create your ISA or import a pre-made one.
#### 6. [Write Program](#programming)
Write your program in program.txt
#### 7. Run
Run `main.py` using `python3 main.py`.


## Config File
### Metadata
| ID | Description | Required |
|:--:| :---------: | :------: |
|name| The name of the processor| yes
|cyan_version| The version of the emulator to use| yes
|creator| The creator of the processor| no
|date| The date the processor was created| no
|description| The description of the processor| no
|operations| List of operations that are created in the instructions file (note: the name should be the same as the function name)| yes


### Datapoints
| ID |   Description   | Units | Required | Recommended |
| :------: | :-------------: | :----------: | :-:| :-:|
|ram|amount of ram|bytes| no | yes
|dcache|amount of dcache|bytes| no| no
|dcache_banks|how many banks|number| no | no
|icache|amount of icache|bytes| no| no
|icache_banks|how many banks|number| no | no
|prom|amount of prom|bytes| yes| yes
|speed|rate that the processor can take |redstone ticks|no| yes
|delay|amount of time it takes from input to output|redstone ticks|no| yes
|registers|number of registers|number| yes| yes
|word_size|word size|number| yes| yes
|opcode_size|opcode size in bits|number| yes |yes
|operand_count|operands|number| yes | yes
|operand_size|number of operands|number| yes| yes
|immediate_size|immediate size|bits| no| no
|io_count|number of IO ports|number| no| yes
|io_size| size of IO ports|bits| no| yes
|reg_error| error on overflow| yes| yes
|ram_error| error on overflow| yes| yes
|io_error| error on overflow| if i/o| yes

### Examples
#### Required
```json
{
    "metadata" : {
        "name" : "foobar",
        "cyan_version" : 1,
        "operations" : ["add", "sub", "xor", "not", "and"]

    }, "datapoints" : {
        "prom" : 64,
        "registers" : 8,  
        "word_size" : 8,
        "opcode_size" : 6, 
        "operand_count" : 2, 
        "operand_size" : 5,
        "reg_error" : false,
        "ram_error" : false,
        "io_error" : false,
        "flags" : ["zero, carry, overflow"],
        "zero_register": true
    }
}
```

#### Recommended
```json
{
    "metadata" : {
        "name" : "foobar",
        "operations" : ["add", "sub", "xor", "not", "and"],
        "cyan_version" : 1,
        "creator" : "Jon Doe"

    }, "datapoints" : {
        "prom" : 64,
        "registers" : 8,  
        "word_size" : 8,
        "opcode_size" : 6, 
        "operand_count" : 2, 
        "operand_size" : 5,
        "ram" : 64,
        "speed" : 4,
        "delay" : 6,
        "io_count" : 4, 
        "io_size" : 8,
        "reg_error" : false,
        "ram_error" : false,
        "io_error" : false,
        "flags" : ["zero, carry, overflow"],
        "zero_register": true
    }
}
```

### How to define flags
After setting the flag list in the config.json file (Example: "flags" : ["zero, carry, overflow"]), you must define what each flag does in the instructions.py file.
```python
class flag_name:
    def get(value) -> bool:
```
Example for a zero flag:
config.json:
```json
{
    "metadata" : {
        "name" : "foobar",
        "cyan_version" : 1,
        "operations" : ["add", "sub", "xor", "not", "and"]

    }, "datapoints" : {
        "prom" : 64,
        "registers" : 8,  
        "word_size" : 8,
        "opcode_size" : 6, 
        "operand_count" : 2, 
        "operand_size" : 5,
        "reg_error" : false,
        "ram_error" : false,
        "io_error" : false,
        "flags" : ["zero"],
        "zero_register": true
    }
}
```
instructions.py:
Note that the class name MUST match the flag name that was defined in config.json.
```python
class zero:
    def get(value) -> bool:
        return value == 0
```

### How to Define Custom Registers
Note that error is error on overflow.
```json
{
    "metadata" : {},
    "datapoints" : {},
    "custom_regs" : {
        "custom_reg_name_1" : {
            "name" : "name_in_code",
            "size" : 8,
            "should_accumulate" : false,
            "error" : false
        }
    }

}
```
Example for an accumulator:
```json
{
    "metadata" : {},
    "datapoints" : {},
    "custom_regs" : {
        "acc" : {
            "name" : "acc",
            "size" : 8,
            "should_accumulate" : true,
            "error" : false
        }
    }

}
```


## Instruction File
Must be a Python file inside of the folder `configGroup`. Note that if you don't change the PC in the instruction, the engine will automatically proceed to the next line in the program.
### Structure
```txt
class <mnemonic_uppercase>:
    opcode = <opcode as a string>
    operand_count = <number of expected operands>
    operand_sizes = [<List in bits>]
    signage = [<"u" for unsigned, "s" for signed>]

    def __init__(self, proc: Processor, operands: list[int]) -> None:
        <code>
```

### Processor Methods
#### Control
- `run() -> none`
- `runSteps() -> none`
- `pause(time: int) -> none`
- `stop() -> none`
- `exportState(filePath: str, pretty: bool) -> bool`
- `dumpState() -> none`
- `reset() -> none`
- `loadProgram(programFile: str) -> bool`
- `setInstructionsFile(instructionsFile: str) -> bool`

#### Memory
- `setReg(address: int, data: int, bool setFlags) -> none`
- `setRAM(address: int, data: int, bool setFlags) -> none`
- `setCustomReg(name: str, data: int, bool setFlags) -> none`
- `getReg(address: int) -> int`
- `getRAM(address: int) -> int`
- `getProm(address: int) -> int`
- `getCustomReg(address: int) -> int`
- `getCST() -> int`

### Flags
- `getFlag(name: str) -> bool`

#### Input/Output
- `setIO(address: int, data: int) -> none`
- `getIO(address: int) -> int`
- `setIOLock(address: int, lockState: bool) -> none`

#### Program Counter
- `getPC() -> int`
- `setPC(address: int, cstackpush: bool) -> none`
- `offsetPC(offset: int) -> none`
- `incrementPC() -> none`

#### Internal Methods (DO NOT USE)
- `initState() -> none`
- `initFlags() -> none`
- `updateFlags() -> none`
- `executeLine() -> none`
- `execute() -> bool`

### Example
Example for an `add` instruction with signed inputs:
```py
class ADD:
    opcode = "add"
    operand_count = 3
    operand_sizes = [4, 8, 8]
    signage = ["u", "u", "u"]

    def __init__(self, proc, operands):
        proc.setReg(operands[2], proc.getReg(operands[0]) + proc.getReg(operands[1]))
```

Note: Incremeting the PC in the instruction is optional. If you dont, the program will automatically do so.

## Programming
### Notes
- Comments can be on their own line or in-line (`;` signifies the start of a comment)

### Format
The default format for CYAN instruction inputs is: `<mnemonic> <operand> <operand> <etc>`

The mnemonic can be lowercase, uppercase, or a mix. This is the same letters as whatever it's defined as in the isntructions file.

The operands should be numbers of any base. For bases other than 10, they must use any of the common notations (0x, 0b, 0o, and decimal). Negative numbers aren't supported and must be dealt with by describing the operand as signed in the instruction class.

### Functions
The compiler supports limited functions, which allow for dynamic reusing of code and loops.

A function can be initialized using `.func <name>` and must be ended using `.`
The code within is reusable, however when the PC reaches a function it will ignore the lines starting with . and run the code normally.

Example of a basic function:
```py
.func minus
    sub 0b0001 0b0001 0b0010 #data
.
minus 0b00 0b00
```
The function above subtracts register 2 from register 1 and stores it in register 1 as the PC passes through it, then it gets called and runs again by `minus 0b00 0b00`.

This code gets compiled into:
```py
NOP
sub 0b0001 0b0001 0b0010
NOP
sysjump 1 0b00 0b00
```
`.func minus` gets turned into a NOP, and `minus` is turned into a hook where whenever `minus` is called, it is replaced by `sysjump` and respective operands. 
`sysjump` contains three operands, one of which is filled in at compile, therefore function calls contain two operands: `flag` and `cstackpush`, which define the flag to use for the jump and whether or not to push to the call stack, respectively.

This can be used to make a loop like this
```py
.func minus
    sub 0b0001 0b0001 0b0010 #data
    minus 0b00 0b00
.
```

The period closing the function also has a functionality. Replacing it with a `.return` will pop from the callstack and jump to that number
Example:
```py
.func minus
    sub 0b0001 0b0001 0b0010 #data
    minus 0b00 0b00
.return
```

Compiled:
```py
NOP
sub 0b0001 0b0001 0b0010
sysjump 1 0b00 0b00
sysreturn
```
`sysreturn` contains no operands, and requires the call stack to have at least one item not throw an error.

### System Methods

The system methods used by the functions to operate are defined in `sysfunctions.py`.
The two default methods are defined as such:
```py

class SYSJUMP:
    opcode = "sysjump"
    operand_count = 3
    operand_sizes = [8,2,2]
    signage = ["u","u","u"]
    
    def __init__(self,proc,operands): 
        if not proc.getFlag(proc.config["datapoints"]["flags"][operands[1]]):
            proc.setPC(int(operands[0]), True if operands[2] > 0 else False)

class SYSRETURN:
    opcode = "sysreturn"
    operand_count = 0
    operand_sizes = []
    signage = []

    def __init__(self,proc,operands):
        proc.setPC(proc.getCST()+1,False)
```

These functions are not recommended to be touched by the user, and can easily be replaced using custom `jmp` and `return` functions.
For example, when using a custom `jmp` instead of writing just `<funcName>` it is best to write `jmp <funcName>`. `<funcName>` then compiles to an index. 
When using a custom `return`, it is best to leave the last period blank and use it on its own line.

Example using custom functions:
```py
.func minus
    sub 0b0001 0b0001 0b0010 #data
    jmp minus 0b00 0b00
    ret
.
```
