import json

with open('cfg/DeviceList.json', 'r') as f:
    device_list = json.load(f)
    
incCounter = 1
thermoCounter = 1

for i in device_list['devices']:
    if i["type"] == "Inclinometer":
        i["MqttName"] = f"i50.{incCounter}"
        incCounter += 1
    if i["type"] == "Thermometer":
        i["MqttName"] = f"BH5000{thermoCounter}"
        thermoCounter += 1

with open('NewDeviceList.json', 'w') as f:
    json.dump(device_list, f)