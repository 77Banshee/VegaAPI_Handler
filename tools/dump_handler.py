import sys, os, pathlib
import json

# path_dir = pathlib.Path().absolute()
path_dir = pathlib.Path('C:/SMZ\Websocket/dumps/message_dumps/').absolute()

files = os.listdir(path_dir)


def clear():
    for i in files:
        to_remove = None
        if i.endswith('.json'):
            file = path_dir.as_posix() + '/' + i
            with open(file, 'r') as f:
                json_text = json.load(f)    
                if json_text['cmd'] == 'console':
                    to_remove = i
                    print("to remove appended")
        if to_remove != None:
            os.remove(file)
            to_remove = None
            print("removed")

def distinct_value_dict(value):
    distinct_values = []
    for i in files:
        with open(path_dir.as_posix() + '/' + i, 'r') as f:
            json_text = json.load(f)    
            if value in json_text:
                if json_text[value] not in distinct_values:
                    distinct_values.append(json_text[value])
    print(len(distinct_values))
    return distinct_values


def get_data(dev_eui):
    for i in files:
        with open(path_dir.as_posix() + '/' + i, 'r') as f:
            json_text = json.load(f)
            if json_text['devEui'] == dev_eui:
                print(json_text['data'])                         


if __name__ == "__main__":
    get_data('07293314051E3F10')