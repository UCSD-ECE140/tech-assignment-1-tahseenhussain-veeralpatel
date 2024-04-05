import time 
import paho.mqtt.client as paho 
from paho import mqtt
import random 
from Mqtt import MQttClient
import matplotlib.pyplot as plt 
  



def update_graph(received_messages, ax1, ax2, y_values_0, y_values_1, last_vals):
    
    # Extract receieved messages
    val_idx_0 = received_messages[0] if len(received_messages) > 0 else None
    val_idx_1 = received_messages[1] if len(received_messages) > 1 else None
    
    # Only updates the graphs if the values have changed - doesnt account for low chance case of no change I know 
    if val_idx_0 is not None and val_idx_0 != last_vals['idx_0']:
        y_values_0.append(int(val_idx_0))
        ax1.clear()
        ax1.plot(y_values_0)
        ax1.set_title('Continuous Values from idx 0')

    if val_idx_1 is not None and val_idx_1 != last_vals['idx_1']:
        y_values_1.append(int(val_idx_1))
        ax2.clear()
        ax2.plot(y_values_1)
        ax2.set_title('Updated Values from idx 1')
        
    last_vals['idx_0'] = val_idx_0
    last_vals['idx_1'] = val_idx_1
    
    plt.pause(0.1)  
    
if __name__ == "__main__":
        
    url = "3983dc79b8c948ff9f164e0f0d0cf8f8.s1.eu.hivemq.cloud"
    
    rcv = MQttClient()
    
    rcv.connect(url)
    rcv.client.loop_start()

    rcv.client.subscribe("james/#", qos=1)
    
    
    # Graphical representation of extracted messages 
    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.suptitle('MQTT Message Values')

    y_values_0 = []
    y_values_1 = []

    last_vals = {'idx_0': None, 'idx_1': None}
    plt.subplots_adjust(hspace=1) 
    while 1:
        #print(f"value: {rcv.received_messages}")
        update_graph(rcv.received_messages, ax1, ax2, y_values_0, y_values_1, last_vals)
        pass