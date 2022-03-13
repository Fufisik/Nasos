import datetime

import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect('localhost', 1883)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe('module:pump')
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    if topic == 'module:pump':
        if payload == "True":
            print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Нехватка воды в баке: включение насоса")
        else:
            print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Бак наполнился: отключение насоса")


while True:
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()