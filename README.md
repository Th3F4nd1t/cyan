# CYAN
## License
[CC BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## How to Use
### Important Things
- Mnemonics must be 3 characters long. To change, edit `parts.py (ln 98, col 25)`

### Step by Step
#### 1. Download ZIP
#### 2. Extract
#### 4. Edit `config.json`
#### 5. Edit `instructions.py`
#### 6. Run

## Things I have to do
- [ ] Execution Function


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
class <menomic>:
    opcode = <opcode as a string>
    operand_lengths = <list of operand lengths as integers. the engine will push the operands as integers>

    def __init__(self, operands: List[int]) -> bool:
        <code>
        return <True if the instruction was executed successfully, False otherwise>
```

Example for an `add` instruction:
```py
class add:
    opcode = "0001"
    operand_lengths = [3, 3, 3]

    def __init__(self, operands: List[int]) -> bool:
        if setRegister(operands[2], (getRegister(operands[0]) + getRegister(operands[1]))):
            return True
        else:
            return False
```