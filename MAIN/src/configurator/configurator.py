import yaml
#Notes for future use, before running do cd main so that it doesn't throw an error
# Example: Reading a YAML file
CONFIG_PATH = f"Config\config.yaml" 
with open(CONFIG_PATH, "r") as file: 
    data = yaml.safe_load(file)

print(data)  # Prints the parsed YAML data as a Python dictionary
