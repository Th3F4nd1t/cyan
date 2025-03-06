from config import *
from processor import *

# Define constants
CYAN_VERSION = 1
CONFIG_PATH = "./configGroup/config.json" 
#changed to forward slash in future should add linux/windows checking for compat

config = getConfig(CONFIG_PATH)

proc = Processor(config)


proc.loadProgram("./program.txt")

proc.runSteps() # Use proc.runSteps() to step through the program
