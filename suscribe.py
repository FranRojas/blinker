import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))

mqttBroker ="mqtt.eclipseprojects.io"

client = mqtt.Client("Smartphone")
client.connect(mqttBroker) 

client.loop_start()

client.subscribe("PARPADEO")
client.on_message=on_message 

time.sleep(1)
client.loop_stop()  
