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

### Flags
- `getFlag(name: str) -> bool`

#### Input/Output
- `setIO(address: int, data: int) -> none`
- `getIO(address: int) -> int`
- `setIOLock(address: int, lockState: bool) -> none`

#### Program Counter
- `getPC() -> int`
- `setPC(address: int) -> none`
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