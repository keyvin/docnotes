#!/usr/bin/python

import socket
import ssl
import select
import urlparse
import gzip
import zlib
import json
import re
import logging
import threading



#import configuration and logging
from mqttproxy_config import *

#import proxy_class
from proxy import *
#this class accepts a socket, determines which key to use, initiates an aws connection, and sends the data and response from a different python thread.




        
class ProxyServer():
    address_family = socket.AF_INET6
    server_ssl_key = ''
    server_ssl_cert = ''

    port = 8883
    server_address = ('', port)
    #Accept requests on incoming port. Log originating IP
    def __init__(self):
        #this can be a list. 
        self.proxy = []
        self.listen_begin()

    def handle_request(self, socket):
        request, client_address = socket.accept()
        request = ssl.wrap_socket(request, keyfile=server_pkey, certfile=server_cert,
                                  server_side=True)
        self.log(client_address)
        prox = Proxy()
        prox.connect(request)
        self.proxy.append(prox)


    #redefine as necessary
    def log(self, text):
        print text

    def listen_begin(self):
        serversocket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        #bind the socket to a public host,
        # and a well-known port
        serversocket.bind(self.server_address)
        #become a server socket
        serversocket.listen(5)
        while True:
            self.handle_request(serversocket)

if __name__ == '__main__':
    s = ProxyServer()
    s.connect(None)


#This script has the following flow:

#receive connection on LISTEN port

#receive MQTT message from LISTEN port

#rewrite MQTT info as needed

#establish connection to host on SEND port w/ the correct key, cert, and private file

#send MQTT. Capture Reply and send back to original device.




