class Processor:
    def __init__(self, config: dict, stateDict: dict = None) -> None:
        """The class constructor for any processor to be used with CYAN."

        Args:
            config (dict): The configuration dictionary for the processor.
            stateDict (dict, optional): The state to start in, if any. If incorrectly formatted, things may break. Defaults to None.
        """
        self.config = config
        self.state = stateDict if stateDict else self.initState()

    def initState(self) -> dict:
        """Initialize the processor state with default values."""
        
        state = {}

        