import json

class Commands(object):
    def server_info_req():
        req = {}
        req["cmd"] = "server_info_req"
        return json.dumps(req)
    def auth_req(login, password):
        req = {}
        req["cmd"] = "auth_req"
        req["login"] = login
        req["password"] = password
        return json.dumps(req)
    def ping():
        req = {}
        req["cmd"] = "ping_req"
        return json.dumps(req)
    def get_device_appdata_req():
        req = {}
        req["cmd"] = "get_device_appdata_req"
        return json.dumps(req)
    def get_data_req(dev_eui, enable_options = False, uts_date_from = 0, uts_date_to = 0, direction = "ALL"):
        req = {}
        req["cmd"] = "get_data_req"
        req["devEui"] = dev_eui
        if enable_options:
            req["select"] = {}
            req["select"]["direction"] = direction
            if uts_date_from != 0 < uts_date_to:
                req["select"]["date_from"] = uts_date_from
                req["select"]["date_to"] = uts_date_to
        return json.dumps(req)
    def send_data_req(dev_eui, data, port = 60, ack = False):
        req = {}
        req["cmd"] = "send_data_req"
        # req["data_list"] = {}
        req["data_list"]["devEui"] = dev_eui
        req["data_list"]["data"] = data
        req["data_list"]["port"] = port
        req["data_dist"]["ack"] = ack
        return json.dumps(req)
    
    


# TODO:
    # “get_device_appdata”
    # "get_data"
    # "send_data"
    # "manage_device_appdata"
    # "get_devices"
    # "manage_devices"
    # "get_device_downlink_queue"
    # "manage_device_downlink_queue"
    # "server_info"
    # "tx"

if __name__ == "__main__":
    # asyncio.run(hello())
    auth = Commands.get_device_appdata_req()
    print(auth)








#### WORKS EXAMPLE
        # print("{\"cmd\":\"server_info_req\"}")
