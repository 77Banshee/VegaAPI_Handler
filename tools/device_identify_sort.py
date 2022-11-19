import json
import dump_handler

# Fill unhandled list
with open('tools/unhandled.txt', 'r') as u:
    unhandled = []
    for i in u:
        if i not in unhandled:
            unhandled.append(i.removesuffix('\n'))
    # print(len(unhandled))

all_packet_types = []

def validate_device(dev_eui):
    unknown = []
    path = dump_handler.path_dir.as_posix() + '/'
    for i in dump_handler.files:
        with open(path + i, 'r') as f:
            temp_json = json.load(f)
            if temp_json['devEui'] == dev_eui:
                first_byte = temp_json['data'][0:2]
                match first_byte:
                    case '11':
                        if dev_eui not in inclinometers:
                            inclinometers.append(dev_eui)
                        if dev_eui in unknown:
                            unknown.remove(dev_eui)
                    case '05':
                        if dev_eui not in thermometers:
                            thermometers.append(dev_eui)
                        if dev_eui in unknown:
                            unknown.remove(dev_eui)
                    case _:
                        pass
    print()
    print("INCLINOMETERS:")
    print(inclinometers)
    print("THERMOMETERS:")
    print(thermometers)
    print("STILL UNKNOWN:")
    print(unknown)
                

inclinometers = []
thermometers = []

if __name__ == '__main__':
    # correct
    inclinometers = ['07293314051D1721', '07293314051D75ED', '07293314051D6690', '07293314051D22AA', '07293314051D3B71', '07293314051D33CF', '07293314051D7BFC', '07293314051D424C', '07293314051D9DFE', '07293314051D2FAD', '07293314051D5CCA', '07293314051D72F1', '07293314051D8875', '07293314051D2020', '07293314051D5428', '07293314051DCEDE', '07293314051D1287', '07293314051D22F3', '07293314051D0779', '07293314051D219B', '07293314051D21BE', '07293314051DCFFC', '07293314051D08E1', '07293314051D179D', '07293314051D8560', '07293314051D0987', '07293314051D00A5', '07293314051DB188', '07293314051D6C4A', '07293314051DA903', '07293314051D009F', '07293314051D4FD4', '07293314051D1EEF', '07293314051DB5DB', '07293314051D09B6', '07293314051D98A2', '07293314051D0F8C']
    thermometers = ['07293314051E2213', '07293314051E0BDF', '07293314051E3723', '07293314051E6D1B', '07293314051E2EAA', '07293314051E21FF', '07293314051E2398', '07293314051E3F10']
    # uncorrect
    unhandled_after_sort = ['07293314051E6628', '07293314051DD463', '07293314051DC224', '07293314051DBDFE', '07293314051DC7EF', '313330346E307713', '07293314052D18F2', '07293314051E03AD', '07293314051E256F', '07293314051E35B3', '07293314051E278D', '07293314051E1B02', '07293314051E59F2']
    
    valid = {'Inclinometers' : [], 'Thermometers' : [], 'Unknown' : []}
    for i in inclinometers:
        valid['Inclinometers'].append(i)
    for i in thermometers:
        valid['Thermometers'].append(i)
    for i in unhandled_after_sort:
        valid['Unknown'].append(i)
    with open('filtered_devEui.json', 'w') as ff:
        dev_euis = json.dump(valid, ff)
        
        