import time 
import paho.mqtt.client as paho 
from paho import mqtt
import random 
from Mqtt import MQttClient

  
if __name__ == "__main__":
        
    url = "8ae73aecca8b42aba3a5f1c678529a93.s1.eu.hivemq.cloud"
    
    cl1 = MQttClient()
    cl2 = MQttClient()
    
    cl1.connect(url)


    cl2.connect(url)
    
    
    while True:
        rand1 = random.randint(-100, -1)
        rand2 = random.randint(1, 9999)
        cl1.client.publish("james/toyota", payload=rand1, qos=1)
        cl2.client.publish("james/ford", payload=rand2, qos=1)
        print("Pubslihed..")

        time.sleep(3)




