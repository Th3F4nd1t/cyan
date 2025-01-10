from utils import *
from parts import *

# Define constants
CYAN_VERSION = 1
CONFIG_PATH = ".\config\config.json"
INSTRUCTIONS_PATH = ".\config\instructions.py"


# Get Data
config = getConfig(CONFIG_PATH)
if checkConfig(config, CYAN_VERSION):
    print("Configuration is valid.")
else:
    print("Configuration is invalid.")
    exit(1)

# Create processor object

# Run processor

