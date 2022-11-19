import json

with open('filtered_devEui.json', 'r') as f:
    device_dict = json.load(f)

with open('DeviceList.json', 'r') as f:
    device_list_raw = json.load(f)
# --

def get_type_by_deveui(dev_eui):
    for i in device_dict:
        if dev_eui in device_dict[i]:
            return i
    return None

def append_dev_types():
    for i in device_list_raw['devices']:
        dev_eui = i['devEui']
        dev_type = get_type_by_deveui(dev_eui)
        if dev_type is None or dev_type == 'Unknown':
            i['type'] = 'Unknown'
        else:
            i['type'] = dev_type[0:-1]

if __name__ == '__main__':
    append_dev_types()
    print(device_list_raw)
    with open('DeviceListTEC1.json', 'w') as f:
        json.dump(device_list_raw, f)
