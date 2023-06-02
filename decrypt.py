import json
import random
import time
from paho.mqtt import client as mqtt_client
import mysql.connector
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
import binascii
import ast
import secrets
import hashlib, secrets, binascii

broker = 'broker.hivemq.com'
port = 1883
topic = "data/enkripsi/RSA"
topic2 = "data/enkripsi/RSAKEY"
mydb = mysql.connector.connect(
host="localhost",
user="root",
password="12345",
database="datata"
)
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

dataRSA = []

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        data = json.loads(msg.payload.decode())
        dataRSA.append(data)

    if(len(dataRSA) == 2):
        print(dataRSA)
        
        dekripsiRSA(dataRSA[0]['dataEnkripsiRSA'], dataRSA[1]['privateKeyRSA'])

        dataRSA.clear()

    client.subscribe([(topic,0),(topic2,0)])
    client.on_message = on_message

    def dekripsiRSA(dataEnkripsi, key):
        RSAprivateKey = RSA.importKey(ast.literal_eval(key))
        OAEP_cipher = PKCS1_OAEP.new(RSAprivateKey)
        decryptedMsg1 = OAEP_cipher.decrypt(ast.literal_eval(dataEnkripsi))
        
        print('Decryption RSA:', decryptedMsg1.decode('utf-8')) 
        print("time decrypt= ", timens)

        print(type(dataEnkripsi))
        print(type(decryptedMsg1.decode('utf-8')))
        inserData(dataEnkripsi,decryptedMsg1.decode('utf-8'))
        def inserData(encryptData, decryptData):
            sql = "INSERT INTO rsadata (encryptData, decryptData) VALUES (%s, %s)"
            val = (encryptData, decryptData)
            mycursor = mydb.cursor()
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        def run():
            client = connect_mqtt()
            subscribe(client)
            client.loop_forever()

        if __name__ == '__main__':
            run()

