# the processor class is just a data structure that holds the state of the processor along with methods to modify the state as well as making sure the state is valid

class Processor:
    def __init__(self, config: dict, state: dict = None):
        if state is None: self.reset() # Set to a blank state if there is no state provided
        else: self.state = self.generate_state() 

    def generate_state(self) -> dict:
        
