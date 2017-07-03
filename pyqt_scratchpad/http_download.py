import http.client
import time


conn = http.client.HTTPConnection("gensho.ftp.acc.umu.se")
print (conn)
conn.request('GET', '/debian-cd/current/amd64/iso-dvd/debian-9.0.0-amd64-DVD-1.iso')

r = conn.getresponse()
print(r.status, r.reason)
print (r)

file = open("output.iso", "wb")

while s:
    file.write(s)
    s =r.read(1048)

    time.sleep(.01)

file.close()