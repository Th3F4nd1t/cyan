from src.cyan.config import *
from src.cyan.engine import *
from src.cyan.compiler import *

config = get_config('Config/config.yaml')
instructions = get_compiled('./program.cyan') # send instruction file to compiler

print(config)
createDynamicInstructions(config)

# not fully implemented
# engine = Engine(instructions,config) 

# not implented
# engine.run()