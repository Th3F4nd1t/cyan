import yaml

# Example: Reading a YAML file
with open("config.yaml", "r") as file:
    data = yaml.safe_load(file)

print(data)  # Prints the parsed YAML data as a Python dictionary
