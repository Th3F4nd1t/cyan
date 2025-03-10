from src.cyan.config import *
from src.cyan.engine import *
from src.cyan.compiler import *

config = get_config('Config/config.yaml')
instructions = get_compiled('./program.cyan') # send instruction file to compiler

engine = Engine(instructions,config) 

engine.run() #engine.run is not implemented yet