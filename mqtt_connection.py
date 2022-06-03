
import paho.mqtt.client as mqtt
import time

broker_address= "40923ae94e934107b11ee48351971009.s2.eu.hivemq.cloud"
port = 8883
user = "francis"
password = "Igna1695"
topic = "Parpadeo/aviso/prueba"
message="Ayuda"
def publish(topic, message):
    print(message)
    client.publish(topic, message)
 
def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
            #Signal connection 
 
    else:
 
        print("Connection failed")
def on_message(client, userdata,msg):
    print("Received message: " +msg.topic + " "+ msg.payload.decode("utf-8") )



 
client = mqtt.Client()               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message = on_message
client.connect(broker_address, 8883)          #connect to broker
client.tls_set(tls_version= mqtt.ssl.PROTOCOL_TLS)
 
client.loop_start()        #start the loop
 


 

 