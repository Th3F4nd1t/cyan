# CYAN
## License
[CC BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## How to Use
### Important Things
- Mnemonics must be 3 characters long. To change, edit `parts.py (ln 98, col 25)`

### Step by Step
#### 1. Download ZIP
This is self explanatory. Download the zip file from GitHub.
#### 2. Extract
Use your favorite extration tool to put the files in any folder location.
#### 4. Edit `config.json`
Follow the instructions below to add your configuration for your processor or import one.
#### 5. Edit `instructions.py`
Create your ISA or import a pre-made one.
#### 6. Write Program
Write your program in program.txt
#### 7. Run
Run `main.py` using `python3 main.py`.


## Config Files
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
|stack_depth|stack depth|idk| no| no
|callstack_depth|callstack depth|idk| no| no
|io_count|number of IO ports|number| no| yes
|io_size| size of IO ports|bits| no| yes

#### How to Define Custom Registers
```json
{
    "metadata" : {},
    "datapoints" : {},
    "custom_regs" : {
        "custom_reg_name_1" : {
            "name" : "name_in_code",
            "size" : 8,
            "should_accumulate" : false,
            "wrapping_behavior" : "<wrap | clamp | error>"
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
            "wrapping_behavior" : "wrap"
        }
    }

}
```

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
        "operand_size" : 5
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
        "io_size" : 8
    }
}
```

## Instruction definitions
```txt
class <mnemonic_uppercase>:
    opcode = <opcode as a string>
    operand_count = <number of expected operands>
    operand_sizes = [<List in bits>]
    signage = [<"u" for unsigned, "s" for signed>]

    def __init__(self, proc: Processor, operands: list[int]) -> None:
        <code>
```

Example for an `add` instruction with signed inputs:
```py
class ADD:
    opcode = "add"
    operand_count = 3
    operand_sizes = [4, 8, 8]
    signage = ["u", "u", "u"]

    def __init__(self, proc, operands):
        proc.setReg(operands[2], proc.getReg(operands[0]) + proc.getReg(operands[1]))
        proc.incrementPC()
```

Note: Incremeting the PC in the instruction is optional. If you dont, the program will automatically do so.

## Programming
; is a comment