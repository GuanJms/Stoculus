import json


def read_json_file_to_dict(filename: str):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data
