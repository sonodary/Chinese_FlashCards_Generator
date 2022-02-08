import os
import json
current_directory = os.path.dirname(__file__)


# The function converts the json file into a python dictionary
def convert():
    try:
        with open(f'{current_directory}/Words_to_remember.json') as json_data:
            data = json.load(json_data)
            return data
    except:
        with open(f'{current_directory}/Chinese_dict.json') as json_data:
            data = json.load(json_data)
            return data


