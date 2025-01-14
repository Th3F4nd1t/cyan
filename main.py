from config import *
from parts import *
from processor import *

# Define constants
CYAN_VERSION = 1
CONFIG_PATH = ".\configGroup\config.json"

config = getConfig(CONFIG_PATH)

proc = Processor(config)

proc.loadProgram("./program.txt")

proc.runSteps()
