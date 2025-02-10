# getting configuration things also process yaml file
import yaml

def get_config(file):
    with open(file, 'r') as f:
        return yaml.safe_load(f)
    
def _validate_config(config):
    ...