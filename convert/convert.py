import json





if __name__ == '__main__':
    conv = converter(device_list, name_list)
    chirp_json = conv.convert_to_chirpstack_json(chirpstack_inlinometer)
    print()
    print(chirp_json)
    with open('chirp_example_inclinometer.json', 'w') as f:
        json.dump(chirp_json, f)
