
import paho.mqtt.client as paho 
from paho import mqtt

class MQttClient: 
    def __init__(self, client_id="", userdata=None, protocol=paho.MQTTv5):
        """
        Initializes the MQTT Client with necessary callbacks and settings.
        """
        self.client = paho.Client(callback_api_version=paho.CallbackAPIVersion.VERSION1, client_id=client_id, userdata=userdata, protocol=protocol)
        self.setup_callbacks()
        self.received_messages = []
    def setup_callbacks(self):
        """
        Sets up the callback methods for the MQTT client.
        """
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        
    # setting callbacks for different events to see if it works, print the message etc.
    def on_connect(self, client, userdata, flags, rc, properties=None):
        """
            Prints the result of the connection with a reasoncode to stdout ( used as callback for connect )
            :param client: the client itself
            :param userdata: userdata is set when initiating the client, here it is userdata=None
            :param flags: these are response flags sent by the broker
            :param rc: stands for reasonCode, which is a code for the connection result
            :param properties: can be used in MQTTv5, but is optional
        """
        print("\n\nCONNACK received with code %s." % rc)


    # with this callback you can see if your publish was successful
    def on_publish(self, client, userdata, mid, properties=None):
        """
            Prints mid to stdout to reassure a successful publish ( used as callback for publish )
            :param client: the client itself
            :param userdata: userdata is set when initiating the client, here it is userdata=None
            :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
            :param properties: can be used in MQTTv5, but is optional
        """
        print("Publish success - mid: " + str(mid))

    # print which topic was subscribed to
    def on_subscribe(self,client, userdata, mid, granted_qos, properties=None):
        """
            Prints a reassurance for successfully subscribing
            :param client: the client itself
            :param userdata: userdata is set when initiating the client, here it is userdata=None
            :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
            :param granted_qos: this is the qos that you declare when subscribing, use the same one for publishing
            :param properties: can be used in MQTTv5, but is optional
        """
        print("Subscribed: " + str(mid) + " " + str(granted_qos))
        print("Sub result: " + str(userdata))


    # print message
    def on_message(self, client, userdata, msg):
        """
            Prints a mqtt message to stdout ( used as callback for subscribe )
            :param client: the client itself
            :param userdata: userdata is set when initiating the client, here it is userdata=None
            :param msg: the message with topic and payload
        """
        print(f"\n\nReceived message '{msg.payload.decode()}' on topic '{msg.topic}'")
        
        # Circular list (ECE16 ftw!!! :O)
        while len(self.received_messages) < 2:
            self.received_messages.append(None)
        self.received_messages = [msg.payload.decode(), self.received_messages[0]]
        
    def msg(self, msg):
        '''
        Accesses msg sent to client 
        '''
        return msg 
         
    def connect(self, url, port=8883):
        """
        Connects the client to the MQTT broker.
        """
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(username="ECE140B", password="potato123P")
        self.client.connect(url, port)


    def start_loop(self):
        """
        Starts the network loop to process network events, including dispatching callbacks.
        """
        self.client.loop_start()
        