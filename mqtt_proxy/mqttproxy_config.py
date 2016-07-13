import logging

client_cert = '/home/keyvin/kevin certs/1b231e2017-certificate.pem.crt'
awsca_cert = '/home/keyvin/kevin certs/VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem'
private_key = '/home/keyvin/kevin certs/1b231e2017-private.pem.key'
aws_host = "avh00s5j49803.iot.us-west-2.amazonaws.com"
server_pkey ='ca.key'
server_cert = 'ca.crt'
incoming_socket = 443
        

#configure logging for amazon sdk
logger = None
logger = logging.getLogger("AWSIoTPythonSDK.core")  # Python 2
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)
    
