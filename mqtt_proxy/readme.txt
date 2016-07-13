This is a very basic proxy server to forward requests from embedded devices to AWS IoT when they have trouble connecting. Though the full text is not here, it is inteded to be GPLv2.

1. Install the AWS IoT python SDK

2. The root CA is used to validate the certificate. The proxies private key is ca.key. The public cert is ca.crt (poorly named)

3. Mqttproxy_config.py should be configured to point to your instance with your certificates.

   DO Not put them in the same directory you will be checking in.

4. In proxy.py, there is a read write loop with a hard coded publish.  

CONNECTING

in /etc/hosts set ma.sdf.org to 127.0.0.1 - you can regenerate a certificate with a different name

openssl s_client -connect ma.sdf.org:8883 -CAfile /path_to_root_cert (root cert in repo)

Anything typed into this terminal will be proxied to the mqtt topic '$aws/things/thing/shadow/update'. This topic is hard coded and is found at line 40 of proxy.py

There are currently no callbacks configured in proxy - this is how you would send the reply from amazon back to the device.

Amazon AWS IoT - you need a thing with an attatched certificate, and a connected policy that allows access. The AWS IoT python sdk is documented at:

https://github.com/aws/aws-iot-device-sdk-python/blob/master/README.rst

The code in the samples sub directory is useful. Source code is very easy to read if you need to figure out an odd error.

Wrapping things with try/catch will make it much more robust. Connected proxy objects exist in their own threads. Mqtt objects exist in their own threads. Removes the need for using select and multiplexing sockets. To handle responses to subscriptions, you should define your own callbacks (see api documentation).


