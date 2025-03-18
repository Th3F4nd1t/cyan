from typing import Dict, Any
from .utils import *
# compiler which turns user-generated program into program which is seen by the processor
# for example functions, loops and other need to be compiled after writing
# take the instruction file and turn it into classes that can be used by the engine

def get_compiled(file: str) -> list:

    with open(file, 'r') as f:
        raw_program = f.readlines()
    
    compiled_program = []

    for index, line in enumerate(raw_program):
        line = line.strip()
        
        while line.startswith(" "):
            line = line[1:]

        # Check for comments or empty lines
        if line.startswith(";") or line == "\n" or line == "":
            line = ""

        if ";" in line:
            line = line.split(";")[0]

        # Insert compiling code for functions, loops, etc here

        compiled_program.append(line)
    
    return compiled_program





# this function compiles the instructions from config.yaml into classes in the instructions.py inside of dynamic_resources

def createDynamicInstructions(config): # add error checking
    log("Starting config adaptation into instruction files", LogLevel.INFO)
    # create file if it doesn't exist or just reset it

    with open("src/cyan/dynamic_resources/instructions.py", "w") as file:
        file.write("# Generated file do not modify\n")

    # starts the creation of the classes
    with open("src/cyan/dynamic_resources/instructions.py", "+a") as file:
        for instruction in config["instruction_set"]:
            
            # basic info
            file.write(f"class {instruction['name'].upper()}:\n")
            file.write(f"   opcode = {instruction['opcode']}\n")
            file.write(f"   latency = {instruction['latency']}\n")


            # operands
            operands_list = ','.join('\''+operand['name']+'\'' for operand in instruction['operands'])
            file.write(f"   operands = [{operands_list}]\n")
            for operand in instruction['operands']:
                file.write(f"   {operand['name']} = " + "{\n")
                file.write(f"       \'type\':\'{operand['type']}\',\n")
                file.write(f"       \'size\':{operand['size']}\n")
                file.write("    }\n")

            # flags
            file.write("   flags_affected = [\n")
            for index,flag in enumerate(instruction["flags_affected"]):
                corrected_flag = "\'" + f"{flag}" + "\'"
                file.write(f"        {corrected_flag}{',' if index != len(instruction['flags_affected'])-1 else ''}\n")
            file.write("    ]\n")

            # pipeline / non pipeline execution info
            if config["pipelined"]:

                pipeline_stages = config["pipeline"]

                file.write("   execution_chain = {\n")
                for stage in instruction["operation"]:
                    corrected_stage = "\'" + f"{stage}" + "\'" + ":" + "\'" + f"{instruction['operation'][stage]}" + "\'"
                    file.write(f"        {corrected_stage}{',' if stage != pipeline_stages[-1] else ''}\n")
                file.write("    }\n")

            else:
                file.write(f"   execution = {instruction['operation']}\n")

            file.write("\n\n\n")

    log("Instruction file creation complete", LogLevel.SUCCESS)