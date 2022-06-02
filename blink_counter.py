
from email.message import Message
from pydoc import Helper
import blinker
import cv2
from matplotlib.pyplot import draw_if_interactive;
import mediapipe as mp;
import numpy as np;
from datetime import datetime
from paho.mqtt import client as mqtt_client
import random
from random import randrange, uniform
import time

broker = 'broker.emqx.io'
port = 1883
topic = "PARPADEO"
client_id = f'python-mqtt-{random.randint(0, 1000)}' 
username = 'Francisco'
password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client







def eye_aspect_ratio(coordinates):
    d_A = np.linalg.norm(np.array(coordinates[1])-np.array(coordinates[5]))
    d_B = np.linalg.norm(np.array(coordinates[2])-np.array(coordinates[4]))
    d_C = np.linalg.norm(np.array(coordinates[0])-np.array(coordinates[3]))

    return (d_A + d_B) / (2 * d_C)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)


mp_face_mesh =mp.solutions.face_mesh
index_left_eye = [33, 160, 158, 133, 153, 144]
index_right_eye = [362, 385, 387, 263, 373, 380]
EAR_THRESH = 0.20
NUM_FRAMES = 1
aux_counter = 0
blink_counter=0 
t1 = 0
t2 = 0
t3=0
def send_message (t3,t1,t2):
    if t3<0:
       t3= t3*-1

    if t3< 1.2:
        message = "AYUDA"
        print (message)
        client.publish("PARPADEO", message)
        print("Just published " + message + " to topic PARPADEO")
      
        t3 =0
    elif t3< 2.2:
        message ="QUIERO HABLAR"
        print (message)
        client.publish("PARPADEO", message)
        print("Just published " + message + " to topic PARPADEO")
        
        t1=0
        t2=0
       
    else:
        print("todo Ok")
        blink_counter = 0 
        t1=0
        t2=0


with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1) as face_mesh:

    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)

        coordinates_left_eye = []
        coordinates_right_eye = []


        if results.multi_face_landmarks is not None:
            for face_landmarks in results.multi_face_landmarks:
                for index in index_left_eye:
                    x = int(face_landmarks.landmark[index].x * width)
                    y = int(face_landmarks.landmark[index].y * height)
                    coordinates_left_eye.append([x,y])

                    cv2.circle(frame, (x,y),2,(0,255,255),1)
                    cv2.circle(frame, (x,y),1,(128,0,255),1)
                for index in index_right_eye:
                    x = int(face_landmarks.landmark[index].x * width)
                    y = int(face_landmarks.landmark[index].y * height)
                    coordinates_right_eye.append([x,y])
                    cv2.circle(frame, (x,y),2,(128,0,255),1)
                    cv2.circle(frame, (x,y),1,(0,255,255),1)

                ear_left_eye =  eye_aspect_ratio(coordinates_left_eye) 
                ear_right_eye =  eye_aspect_ratio(coordinates_right_eye)
                ear = (ear_left_eye+ear_right_eye)/2
                #print("ear_left_eye:", ear_left_eye, " ear_right_eye:", ear_right_eye)
                print(ear)


                if ear < EAR_THRESH:
                    aux_counter +=1
                    

                else:
                    if aux_counter >= NUM_FRAMES:
                        aux_counter= 0
                        blink_counter+=1 
                        print (blink_counter)
                        if blink_counter ==1:
                            t1 = datetime.now()
                            print("primer parpadeo")
                        if blink_counter==3:
                            t2 = datetime.now()
                            t3 = t2.second-t1.second
                            send_message(t3,t1,t2)
                            print("van ", t3)
                            blink_counter=0
                            t3=0


        cv2.imshow("Frame", frame)
        k=cv2.waitKey(1) & 0xFF
        if k == 27:
            break

cap.release()
cv2.destroyAllWindows()
