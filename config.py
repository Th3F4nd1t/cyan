import json
from utils import *

config_elements = [
    "ram",
    "prom",
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
    "reg_error",
    "ram_error",
    "io_error"
]


def validateConfig(configDict: dict, version) -> bool:
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
        "prom", "registers", "word_size", "opcode_size", "operand_count", "operand_size", "reg_error", "ram_error", "io_error", "flags"
    ]

    # Check required metadata
    for field in metadata_required:
        if field not in configDict.get("metadata", {}):
            log(f"Missing required metadata field: {field}", "FATAL")

    # Check required datapoints
    for field in datapoints_required:
        if field not in configDict.get("datapoints", {}):
            log(f"Missing required datapoints field: {field}", "FATAL")
        
    if configDict.get("metadata", {}).get("cyan_version") > version:
        log(f"Config is too new. Expected {version}, got {configDict.get('metadata', {}).get('cyan_version')}", "ERROR")

    log("Configuration is valid.", "INFO")
    return True

def getConfig(configPath: str) -> dict:
    """Returns a dict of the configuration from the given json file.

    Args:
        configPath (str): The absolute or relative path of the configuration file.

    Returns:
        dict: The dict of the config.
    """

    with open(configPath, "r") as f:
        return json.load(f)
