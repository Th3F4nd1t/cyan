from src.cyan.config import *
from src.cyan.engine import *
from src.cyan.compiler import *

config = get_config('./config.yaml')
instructions = get_compiled('./instructions.cyan') # send instruction file to compiler

engine = Engine(instructions,config) 

engine.run() #engine.run is not implemented yet