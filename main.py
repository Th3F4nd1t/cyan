from utils import *
from parts import *

# Define constants
CYAN_VERSION = 1
CONFIG_PATH = ".\config\config.json"
INSTRUCTIONS_PATH = ".\config\instructions.py"


# Get Data
config = getConfig(CONFIG_PATH)

proc = Processor(config)

# Run processor

print(proc.state)