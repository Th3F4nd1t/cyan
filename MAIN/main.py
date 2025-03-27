from src.cyan.config import *
from src.cyan.engine import *
from src.cyan.compiler import *
from src.cyan.utils import *
import sys
log("Booting CPU", LogLevel.INFO)
config = get_config('Config/config.yaml')

validate_config(config)
createDynamicInstructions(config)


instructions = get_compiled('./program.cyan') # finish compiler


engine = Engine(instructions,config) 

# not implented
engine.run()