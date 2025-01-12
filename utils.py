import json
import importlib

logValue = True

def log(message: str) -> None:
    if logValue:
        print(message)

def error(message: str) -> None:
    print(f"Error: {message}")
    print("Exiting the program.")
    exit(1)
    

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

def import_class(class_path):
    module_name, class_name = class_path.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)

def dict_of_lists_to_pretty_string(data):
    result = []
    for key, class_list in data.items():
        class_strings = [repr(cls) for cls in class_list]
        result.append(f"{key}: [{', '.join(class_strings)}]")
    return "{\n  " + ",\n  ".join(result) + "\n}"