# take in instruction classes and modify the state of the processor based on the instructions

from cyan.processor import Processor


class Engine:
    def __init__(self, instructions, config):
        self.proc = Processor(config)
        self.instructions = instructions
        