from utils import *
from parts import *

# Define constants
CYAN_VERSION = 1
CONFIG_PATH = ".\configGroup\config.json"

# Get the config from the json file
config = getConfig(CONFIG_PATH)

# Get the processor object
proc = Processor(config)

# Load the program to be ran
proc.loadProgram("./program.txt")

# Run the program
proc.run()
