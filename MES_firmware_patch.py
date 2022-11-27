import textwrap

# 46 symbols in packet.
# 23 bytpacket

# 32 symbols in data
# 16 bytes in data

def str_sum_hex_dec(hex_str, num):
    res = hex(int(hex_str, 16) + num)[2:] # Отсекаем у результата "0x" в начале
    if len(res) == 1:
            res = "0" + res
    return res

def divide_thermometer_data(str_hex_data, quantity):
    # Metadata
    packet_id = str_hex_data[0:2]
    first_sensor = str_hex_data[2:4]
    last_sensor = str_hex_data[4:6]
    time = str_hex_data[6:14]
    # Measures
    raw_str_hex_measures = str_hex_data[14:]
    divided_measures = textwrap.wrap(raw_str_hex_measures, 4 * 8) # Разрезаем данные на несколько пакетов (до 8ми значений с датчиков на пакет)
    # Convert process
    # Берем первый пакет.
            # Конвертируем из str -> int_hex -> int_dec
            # прибавляем 7 и получаем current_last_sensor
            # Конвертируем в int_hex -> str
            #
    handled_packets = []
    current_first_sensor = "01"
    for i in divided_measures:
        current_last_sensor = str_sum_hex_dec(current_first_sensor, 7) # Прибавляем 7 к текущему первому сенсору, чтобы получить предположительный последний сенсор.
        if current_last_sensor > last_sensor:
            current_last_sensor = last_sensor
        if len(current_last_sensor) == 1:
            current_last_sensor = "0" + current_last_sensor # Если в значении одна цифра нужно добавить 0 перед ней, для правильного парсинга.
        if len(i) < 32:
            for _ in range(32 - len(i)):
                i += "0"        
        packet_part = packet_id + current_first_sensor + current_last_sensor + time + i
        handled_packets.append(packet_part)
        # Меняем первый сенсор для следующего пакета
        # divided_measures.
        current_first_sensor = str_sum_hex_dec(current_last_sensor, 1)
    return handled_packets

class thermo_data_for_tests():
    def __init__(self, byte_array_data, quantity) -> None:
        self.quantity = quantity #18
        # Metadata
        self.byte_array_data = byte_array_data
        self.id = byte_array_data[0:1]
        self.first_sensor = byte_array_data[1:2]
        self.last_sensor = byte_array_data[2:3]
        self.time = byte_array_data[3:7]
        # Divide sensor data
        self.data = byte_array_data[7:]
        # b_sensor_data_list = textwrap.wrap(self.data, 4)
        print(len(self.data) / self.quantity)
        # self.sensor_data = textwrap.wrap(self.data, 4)
        
    def convert(self):
        for i in range(0, int(len(self.data) / 2)):
            print(f"{i+1}")
            barr = bytearray()
            barr.append(self.data[0])
            barr.append(self.data[1])
            self.data = self.data[2:]
            print(barr)
            res = int.from_bytes(barr, 'big', signed=True) / 100
            print(res)
    def __str__(self) -> str:
        return (
            f"ID: {self.id.hex()}\n" +
            f"First sensor: {self.first_sensor.hex()}\n" +
            f"Last sensor: {self.last_sensor.hex()}\n" +
            f"DATA:\n\t {self.data.hex()} \n\t\n"
        )

if __name__ == "__main__":
    raw = "050112636f6f8df67afa7aff1effe8fff6ffc6ff8fff55ff3bff24fef6fec7feb0fea5fea2fea1feb4feb3"
    # raw = "05 01 12 636f6f8d f67a fa7a ff1e ffe8 fff6 ffc6 ff8f ff55 ff3b ff24 fef6 fec7 feb0 fea5 fea2 fea1 feb4 feb3"
    handled_packets = divide_thermometer_data(raw, 18)
    print(handled_packets)