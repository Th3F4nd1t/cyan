from config import *
from parts import *
from Processor import *

# Define constants
CYAN_VERSION = 1
CONFIG_PATH = ".\configGroup\config.json"

config = GetConfig(CONFIG_PATH)

proc = Processor(config)

proc.loadProgram("./program.txt")

proc.run()
