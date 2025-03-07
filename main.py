from config import *
from processor import *
import sys,os
# Define constants
CYAN_VERSION = 1
CONFIG_PATH = "\configGroup\config.json" 

config = getConfig(f"{os.getcwd()}"+ CONFIG_PATH)

proc = Processor(config)


proc.loadProgram("./program.txt")

proc.run() # Use proc.runSteps() to step through the program
