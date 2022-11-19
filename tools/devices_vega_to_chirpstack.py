import json


# Get json vega api
with open("device_dump_vega.json", 'r') as f:
    vega_devicelist = json.load(f)
    #\\ Пример запроса одного из девайсов vega_devicelist['devices_list'][0]

# Create raw chirpstack device list and write data into
def chirpstack_raw_dvice_list():
    chirp_device_list = {}
    chirp_device_list['devices'] = []
    for i in vega_devicelist['devices_list']:
        chirp_device_list['devices'].append(
            {
                "devEui": i['devEui'],
                "MqttName": i['devName'],
                "type": "N\A",
                "object_id": "11223344",
                "object_code": "TEC-1",
                "uspd_code": "U1122"
            }
        )
    with open('DeviceList.json', 'w') as d:
        d.write(json.dumps(chirp_device_list))
if __name__ == '__main__':
    chirpstack_raw_dvice_list()