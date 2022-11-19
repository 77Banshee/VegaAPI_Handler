import websockets
import asyncio
import json

# Сейчас создав экземпляр класса ws_client и вызвав его метод start_listening() на asyncio.run() мы 
# мы получаем все сообщения которые отправляет веб сокет.

# Необходимо конвертировать приходящие rx сообщения в формат chirpstack и отправить на MQTT брокер, на который мы подписаны 
# в главном потоке.

#TODO:
    # - Изучить MES_server и постораться без рефакторинга выключить функции чирпстека или же заменить этим модулем, если
    # это не повредит основной программе.
    # - Релизовать отправку натроек через websocket (Возможно потребуется гуглить как добавить дополнительную задачу в asyncio):
        # -- При получении 03 пакета, а так же при обнаружении смещения времени
        # -- При необходимости изменить переодичность опроса датчиков

## Debug instances
with open('dump_1668240808.json', 'r') as f:
    chirpstack_inlinometer = json.load(f)
    
with open('cfg/NameList.json', 'r') as f:
    name_list = json.load(f)

with open('cfg/DeviceList.json', 'r') as f:
    device_list = json.load(f)

# Classes
class converter(object):
    def __init__(self, device_list, name_list) -> None:
        self.device_list = device_list
        self.name_list = name_list

    def get_dev_type(self, dev_eui):
        for i in self.device_list['devices']:
            if i["devEui"] == dev_eui:
                return i["type"]

    def get_dev_name(self, dev_eui): # Web Name
        for i in self.name_list['devices']:
            if i["devEui"] == dev_eui:
                return i["deviceName"]

    def convert_to_chirpstack_json(self, vega_json):
        chirpstack_json = {}
        dev_eui = vega_json["devEui"]
        chirpstack_json['devEUI'] = dev_eui
        chirpstack_json["applicationName"] = self.get_dev_type(dev_eui)
        chirpstack_json["deviceName"] = self.get_dev_name(dev_eui)
        chirpstack_json['rxInfo']  = []
        chirpstack_json['rxInfo'].append(
            {"rssi": vega_json['rssi'], "loRaSNR": vega_json["snr"]}
        )
        chirpstack_json['txInfo'] = {}
        chirpstack_json['fCnt'] = vega_json["fcnt"]
        chirpstack_json['fPort'] = vega_json["port"]
        chirpstack_json['data'] = vega_json["data"]

        return chirpstack_json

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
        # req["data_list"] = {}
        req["data_list"]["devEui"] = dev_eui
        req["data_list"]["data"] = data
        req["data_list"]["port"] = port
        req["data_dist"]["ack"] = ack
        return json.dumps(req)

class ws_client(object):
    def __init__(self, ws_address = '172.26.79.10', ws_port = '8082') -> None:
        self.ws_address = ws_address
        self.ws_port = ws_port
    async def event_loop(self):
        uri = f'ws://{self.ws_address}:{self.ws_port}/'
        connection = websockets.connect(uri)
        async with connection as websock:
            await websock.send(
                commands.auth_req('root', '123')
            )
            async for message in websock:
                print(message)
                json_msg = json.loads(message)
                if json_msg["cmd"] == "rx":
                    pass
            await websock.close()

    async def start_listening(self):
        tasks = asyncio.create_task(self.event_loop())
        print("[*] Listen websocket...")
        await tasks

if __name__ == '__main__':
    client = ws_client()
    asyncio.run(client.start_listening())
    