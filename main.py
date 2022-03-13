import datetime
import time

import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect('localhost', 1883)


class Sensor:
    def __init__(self, name, state, value):
        self.name = name
        self.state = state
        self.value = value

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state


sensor_high = Sensor('sensor_high', False, 50)
sensor_low = Sensor('sensor_low', False, 1)


def increase_water(volume):
    time.sleep(3)
    return volume + 1


while True:

    sensor_high.value = int(input('Введите максимальный порог воды для отключения насоса (не выше 100): '))
    sensor_low.value = int(input('Введите минимальный порог воды для включения насоса (не ниже 1): '))
    if sensor_high.value > sensor_low.value:
        if sensor_high.value <= 100 and sensor_low.value >= 1:
            print("Значения установлены на датчики. Двигаемся дальше...")
        else:
            print("Значение должны соответстовать условиям!")
            continue
    else:
        print("Значение максимального порога должно быть строго больше минимального!")
        continue

    while True:
        now_volume = int(input('Введите объем воды, который находится в баке '
                               '(не выше максимального порога и не ниже 0): '))

        if 0 <= now_volume <= sensor_high.value:
            print("Текущий объем воды условно определен.")
            break
        else:
            print("Значение объема воды должно быть не выше максимального порога! Либо значение не корректно!")
            pass
    break


while True:

    if now_volume <= sensor_low.value:
        sensor_low.set_state(True)
        print("Воды недостаточно")
        client.publish("sensors/sensor_low", sensor_low.get_state())
        print(str(datetime.datetime.now().time().strftime("%H:%M:%S")) + " Заполнение бака")
        sensor_low.set_state(False)
        while True:
            if now_volume < sensor_high.value:
                now_volume = increase_water(now_volume)
            else:
                sensor_high.set_state(True)
                client.publish("sensors/sensor_high", sensor_high.get_state())
                break
    elif now_volume == sensor_high.value:
        print(str(datetime.datetime.now().time().strftime("%H:%M:%S")) + " *Бак полный*")
        while True:
            rs = input("Вода начала расходоваться? да/нет: ")
            if rs == 'да':
                sensor_high.set_state(False)
                client.publish("sensors/sensor_high", sensor_high.get_state())
                # Эмуляция для срабатывания нижнего датчика при расходовании воды внешними факторами {
                while True:
                    st = input("Уровень в баке достиг минимального порога? да/нет: ")
                    #   }
                    if st == 'да':
                        now_volume = sensor_low.value
                        break
                    elif st == 'нет':
                        pass
                    else:
                        print("Введены неверные данные!")
                        pass
                break
            elif rs == 'нет':
                pass
            else:
                print("Введены неверные данные!")
                pass
    else:
        print("*Воды в баке достаточно*")
        while True:
            st = input("Уровень в баке достиг минимального порога? да/нет: ")
            if st == 'да':
                now_volume = sensor_low.value
                break
            elif st == 'нет':
                pass
            else:
                print("Введены неверные данные!")
                pass
    continue