import json


config_elements = [
    "ram",
    "dcache",
    "prom",
    "icache",
    "speed",
    "delay",
    "registers",
    "word_size",
    "opcode_size",
    "operand_count",
    "operand_size",
    "immediate_size",
    "stack_depth",
    "callstack_depth",
    "io_count",
    "io_size",
]


def isConfigValid(configDict: dict, version) -> bool:
    """This method checks the configuration of the configuration for a CYAN emulator.

    Args:
        configDict (dict): The configuration dictionary to be checked.

    Returns:
        bool: True if the configuration is valid, False otherwise.
    """
    # Metadata required fields
    metadata_required = ["name", "cyan_version"]
    
    # Datapoints required fields
    datapoints_required = [
        "prom", "registers", "word_size", "opcode_size", "operand_count",
        "operand_size"
    ]

    # Check required metadata
    for field in metadata_required:
        if field not in configDict.get("metadata", {}):
            print(f"Missing required metadata field: {field}")
            return False

    # Check required datapoints
    for field in datapoints_required:
        if field not in configDict.get("datapoints", {}):
            print(f"Missing required datapoints field: {field}")
            return False
        
    if configDict.get("metadata", {}).get("cyan_version") > version:
        print(f"Config is too new. Expected {configDict.get('metadata', {}).get('cyan_version')}, got {version}")
        return False

    return True

def checkConfig(config, version):
    if checkConfig(config, version):
        print("Configuration is valid.")
    else:
        print("Configuration is invalid.")
        raise Exception("Configuration is invalid.")

def getConfig(configPath: str) -> dict:
    """Returns a dict of the configuration from the given json file.

    Args:
        configPath (str): The absolute or relative path of the configuration file.

    Returns:
        dict: The dict of the config.
    """

    with open(configPath, "r") as f:
        return json.load(f)

def dumpOutput(stateDict: dict):
    """
    Dumps the output of the CYAN emulator as a pretty table.

    Args:
        stateDict (dict): The state dictionary of the CYAN emulator. Note that the input should be Processor.StateDict.get() or any other raw dictionary.
    
    Raises:
        TypeError: If stateDict is not a dictionary.
    """
    if not isinstance(stateDict, dict):
        raise TypeError()

    key_width = max(len(str(key)) for key in stateDict.keys()) if stateDict else 3
    value_width = max(len(str(value)) for value in stateDict.values()) if stateDict else 5
    
    key_width = max(key_width, len("Key"))
    value_width = max(value_width, len("Value"))
    
    border = f"+{'-' * (key_width + 2)}+{'-' * (value_width + 2)}+"
    header = f"| {'Key'.ljust(key_width)} | {'Value'.ljust(value_width)} |"
    
    print(border)
    print(header)
    print(border)
    for key, value in stateDict.items():
        print(f"| {str(key).ljust(key_width)} | {str(value).ljust(value_width)} |")
    print(border)
