#KNP - 07/13/2016 - Threaded class. Handles I/O between one socket and another
#rewrites information as necessary

import threading
from mqttproxy_config import *
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient



class Proxy(threading.Thread):
    def __init__(self):
        #There should be some mechanism to look up these credentials for each device
        #currently stored in 
        threading.Thread.__init__(self, target=self.main_loop)
        self.client_cert = client_cert
        self.awsca_cert = awsca_cert
        self.private_key = private_key
        self.aws_host = aws_host
        self.incoming_socket = None
        self.myShadowClient = None
    def connect(self, incoming_socket):

        self.incoming_socket = incoming_socket
        self.myShadowClient = AWSIoTMQTTShadowClient("impulse")       
        print(self.aws_host)
        self.myShadowClient.configureEndpoint(self.aws_host, 8883)
        self.myShadowClient.configureCredentials(self.awsca_cert, self.private_key, self.client_cert)       
        self.myShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myShadowClient.configureMQTTOperationTimeout(5)  # 5 sec
        res = self.myShadowClient.connect()
        self.run()

        
    #function just passes data back and forth. Use callbacks for mqqt sending
    def main_loop(self):
        #define callbacks to return information to socket
        while True:
            data = self.incoming_socket.recv(2048)
            print data
            data = self.incoming_socket.write("Received")
    def callback(self):
        pass

    
