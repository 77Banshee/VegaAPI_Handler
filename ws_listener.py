import websockets
import asyncio
import json
import base64
from textwrap import wrap
import queue
import MES_firmware_patch

# Сейчас создав экземпляр класса ws_client и вызвав его метод start_listening() на asyncio.run() мы 
# мы получаем все сообщения которые отправляет веб сокет.

# Необходимо конвертировать приходящие rx сообщения в формат chirpstack и отправить на MQTT брокер, на который мы подписаны 
# в главном потоке.

# - Изучить MES_server и постораться без рефакторинга выключить функции чирпстека или же заменить этим модулем, если
    # это не повредит основной программе.
    # - Релизовать отправку натроек через websocket (Возможно потребуется гуглить как добавить дополнительную задачу в asyncio):
    # Так же можно настроить подписку на топики /command/down
        # -- При получении 03 пакета, а так же при обнаружении смещения времени
        # -- При необходимости изменить переодичность опроса датчиков
    # - Можно реализовать отправку настроек реализацией метода check_time() который будет проверять время устройства прямо на входе,
    # и сразу возвращать ответ при необходимости.
    # Написать дополнительный конвертер для старой версии термокос

#TODO:
    # Поднять MQTT сервер.
    # Добавить 

# Classes

class commands(object):
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
        req["data_list"] = []
        req["data_list"].append(
            {
                "devEui" : dev_eui,
                "data" : data,
                "port" : port,
                "ack" : ack
            }
        )
        return json.dumps(req)

class ws_client(object):
    def __init__(self, device_list, tk_config, ws_address = '172.26.79.10', ws_port = '8082') -> None:
        self.ws_address = ws_address
        self.ws_port = ws_port
        self.uri = f'ws://{self.ws_address}:{self.ws_port}/'
        self.api_dev_list = {}
        self.device_list = device_list
        self.tasks = []
        self.send_queue = queue.Queue()
        self.tk_config = tk_config
        
    def get_tk_quantity(self, dev_eui):
        dev_eui = dev_eui.upper()
        for i in self.tk_config["TK"]:
            if i["devEUI"] == dev_eui:
                return i["Quantity"]
        print(f"[*] ERROR! QUANTITY FOR {dev_eui} NOT FOUND IN TK CONFIG!")
        raise ValueError("Tk not found in tk_config!")
        
    def hex_string_to_b64_bytes(self, hex_string):
        return base64.b64encode(
                bytes.fromhex(hex_string)
            ).decode('ascii')
        
    def get_dev_type(self, dev_eui):
        for i in self.device_list['devices']:
            if i["devEui"] == dev_eui:
                return i["type"]

    def get_dev_name(self, dev_eui): # Web Name
        for i in self.api_dev_list:
            if i["devEui"] == dev_eui:
                return i["devName"]
    
    def convert_to_chirpstack_json(self, vega_json):
        chirpstack_json = {}
        dev_eui = vega_json["devEui"]
        chirpstack_json['devEUI'] = self.hex_string_to_b64_bytes(dev_eui)
        chirpstack_json["applicationName"] = self.get_dev_type(dev_eui)
        chirpstack_json["deviceName"] = self.get_dev_name(dev_eui)
        chirpstack_json['rxInfo']  = []
        chirpstack_json['rxInfo'].append(
            {"rssi": vega_json['rssi'], "loRaSNR": vega_json["snr"]}
        )
        chirpstack_json['txInfo'] = {}
        chirpstack_json['fCnt'] = vega_json["fcnt"]
        chirpstack_json['fPort'] = vega_json["port"]
        chirpstack_json['data'] = self.hex_string_to_b64_bytes(
            vega_json["data"]
        )

        return chirpstack_json
    
    async def TEST_SEND_SETTINGS(self, message):
        # Message example
        # message = commands.send_data_req("07293314051D009F", base64.b64encode(b'\x03').decode('ascii'))
        
        # Add message example
        # self.tasks.append(asyncio.create_task(self.send_test_settings(command)))
        
        con2 = websockets.connect(self.uri)
        async with con2 as ws:
            await ws.send(
                commands.auth_req('root', '123') # auth #TODO: Pass as parameter
            )
            await ws.send(
                message
            )
            print("[*] DEBUG | WS Send settings: MESSAGE SENT!")
            async for message in ws:
               await print("ws: " + message)
            print("[*] Debug | WS Send settings: CONNECTION CLOSED!")
    
    async def event_loop(self):
        connection = websockets.connect(self.uri)
        async with connection as websock:
            await websock.send(
                commands.auth_req('root', '123') # auth #TODO: Pass as parameter
            )
            await websock.send(
                commands.get_device_appdata_req() # Fill vega_api_device_list
            )
            async for message in websock:
                # print(message)
                json_msg = json.loads(message)
                # self.tasks.append(asyncio.create_task(self.printmessage(self.counter)))
                if not self.api_dev_list and json_msg["cmd"] == "get_device_appdata_resp":
                    raw_list = json.loads(message)
                    self.api_dev_list = raw_list["devices_list"]
                    print("api_dev_list has setted!")
                if json_msg["cmd"] == "rx" and json_msg["type"] == "CONF_UP":
                    print(json_msg)
                    payload = json_msg['data']
                    match payload[:2]:
                        case "05":
                            print(f"json_msg['data'] : {payload}")
                            if len(payload) != 46:
                                thermometer_divided = MES_firmware_patch.divide_thermometer_data(payload)
                                print(f"[*] DEBUG: TK Before:\n\t {payload}")
                                print(f"AFTER:")
                                for i in thermometer_divided:
                                    print(f"\t{i}")
                                    self.send_queue.put(i)
                            else:
                                print(f"WTF THERMOMETER DATA NOT OLD VERSION? {payload} | LEN: {len(payload)}")
                        case "11":
                            self.send_queue.put(self.convert_to_chirpstack_json(json_msg))
                        case "03":
                            pass
                    print(self.convert_to_chirpstack_json(json_msg))
                    for i in range(self.send_queue.qsize()):
                        json_to_send =  self.send_queue.get()
                        # PUSH json_to_send TO MQTT
                        # which topic? application/00/device/{vega_json["devEui"].lower()}/event/up

    async def start_listening(self):
        self.tasks.append(asyncio.create_task(self.event_loop()))
        print("[*] Listen websocket...")
        await asyncio.wait(self.tasks)

if __name__ == '__main__':
    with open('cfg/DeviceList.json', 'r') as f:
        device_list = json.load(f)
    
    with open('cfg/TkConfig.json', 'r') as f:
        tk_config = json.load(f)
    
    client = ws_client(device_list, tk_config)
    asyncio.run(client.start_listening())
    