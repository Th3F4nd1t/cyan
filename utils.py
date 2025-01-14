import json
import importlib
import datetime

printLogs = True

def log(message: str, level: str) -> None:
    with open("./log.txt", "a") as f:
        f.write(f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}] {level.upper()}: {message}\n")

    if level == "INFO" or level == "WARNING":
        if printLogs:
            print(f"{level.upper()}: {message}")
    elif level == "ERROR" or level == "FATAL":
        print(f"{level.upper()}: {message}")
        print("Exiting the program...")
        with open("./log.txt", "a") as f:
            f.write(str(f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}] {level.upper()}: Exiting the program...\n"))
        exit(1)
    
def resetLogger():
    with open("./log.txt", "w") as f:
        f.write("")

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

def isSizedCorrectly(sizes: list, data: list, signage: list) -> bool:
    """ Check if the number in the data list is within the corrospondin number of bits specified in the sizes list. It also uses the signage list to check if the number is signed or unsigned and if it's signed, then it limits the values to be within the 2s complement size."""
    for i, size in enumerate(sizes):
        if signage[i] == "u":
            if data[i] < 0 or data[i] >= 2 ** size:
                return False
        elif signage[i] == "s":
            if data[i] < -(2 ** (size - 1)) or data[i] >= 2 ** (size - 1) - 1:
                return False
            
    return True