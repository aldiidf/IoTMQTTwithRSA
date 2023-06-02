import json
import random
import time
import datetime
from paho.mqtt import client as mqtt_client
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
import secrets
import RPi.GPIO as GPIO

broker = 'broker.hivemq.com'
port = 1883
topic = "data/enkripsi/RSA"
topic2 = "data/enkripsi/RSAKEY"

def connect_mqtt():
 def on_connect(client, userdata, flags, rc):
    if rc == 0:
      print("Connected to MQTT Broker!")
    else:
      print("Failed to connect, return code %d\n", rc)
 
 client = mqtt_client.Client()
 client.on_connect = on_connect
 client.connect(broker, port)
 
 return client

def publish(client, dataRSA):
    time.sleep(1)

objData = {
'dataEnkripsiRSA' : dataRSA,
}

dataJson = json.dumps(objData)
result = client.publish(topic, dataJson)

# result: [0, 1]
status = result[0]

if status == 0:
    print(f"Send `{dataJson}` to topic `{topic}`")
else:
    print(f"Failed to send message to topic {topic}")
def publish2(client):
    
    time.sleep(1)

objData = {
'privateKeyRSA' : str(privateKey),
}
dataJson = json.dumps(objData)
result = client.publish(topic2, dataJson)

# result: [0, 1]
status = result[0]
if status == 0:
    print(f"Send `{dataJson}` to topic `{topic2}`")
else:
    print(f"Failed to send message to topic {topic2}")

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 3
GPIO_ECHO = 2

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
 GPIO.output(GPIO_TRIGGER, True)
 time.sleep(0.00001)

 GPIO.output(GPIO_TRIGGER, False)

 StartTime = time.time()
 StopTime = time.time()
 while GPIO.input(GPIO_ECHO) == 0:
    StartTime = time.time()

 while GPIO.input(GPIO_ECHO) == 1:
    StopTime = time.time()

 TimeElapsed = StopTime - StartTime
 distance = (TimeElapsed*34300) / 2
 
 return distance    

if __name__ =='__main__':
    try:
        while True:
            dist = distance()
            print ("Distance = %.1f cm" %dist)
            distInStr = str(dist)
            msg = print ("Data Sensor= ", distInStr + " cm")
            timens = time.time_ns()
            print("time before= ", timens)
 
            msg = str.encode(distInStr)
 
            key = RSA.generate(1024)

            privateKey = key.exportKey('PEM')
            
            publicKey = key.publickey().exportKey('PEM')
        
        #Enkripsi RSA
            RSApublicKey = RSA.importKey(publicKey)
            OAEP_cipher = PKCS1_OAEP.new(RSApublicKey)
            encryptedMsg1 = OAEP_cipher.encrypt(msg)
            print("RSA encrypt:", encryptedMsg1)
            privKey = secrets.randbelow(curve.field.n)
            pubKey = privKey * curve.g
 
            timens = time.time_ns()          
            print("time after= ", timens)
            f = open ('encryptionRSA.txt', 'w')
            f.write(str(encryptedMsg1))
            
            f.close()
            f = open ('encryptionRSA.txt', 'r')
            messageRSA = f.read()
        
            client = connect_mqtt()
            publish(client, messageRSA)

            time.sleep(2)
            
    except KeyboardInterrupt:
        print ("Measurement stopped")
        
        GPIO.cleanup()

