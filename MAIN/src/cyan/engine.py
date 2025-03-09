# take in instruction classes and modify the state of the processor based on the instructions

from cyan.processor import Processor
from config import *

class Engine:
    def __init__(self, instructions, config):
        validate_config(config) # validate config not set up yet
        self.static = StaticConfig(config) # contains base info about cpu which could be useful
        self.proc = Processor(config, self.static)
        self.instructions = instructions
        