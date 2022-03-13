import datetime
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect('localhost', 1883)

class Pump:
    def __init__(self, state):
        self.state = state

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state


pump = Pump(False)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe('sensors/#')
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    if topic == 'sensors/sensor_low' and payload == "True":
        print(str(datetime.datetime.now().time().strftime("%H:%M:%S")) + " Достигнут минимальный порог."
                                                                        " ***Включение насоса***")
        pump.set_state(True)
        client.publish("module:pump", pump.get_state())
    elif topic == 'sensors/sensor_high' and payload == "True":
        print(str(datetime.datetime.now().time().strftime("%H:%M:%S")) + " Достигнут максимальный порог."
                                                                        " ***Выключение насоса***")
        pump.set_state(False)
        client.publish("module:pump", pump.get_state())

while True:
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()