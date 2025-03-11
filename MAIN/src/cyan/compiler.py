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