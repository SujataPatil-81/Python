import json

def read_config(file_path):
    """
    Reads a JSON configuration file and returns its contents as a dictionary.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file '{file_path}' not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Configuration file '{file_path}' contains invalid JSON.")