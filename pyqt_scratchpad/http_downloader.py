import queue
from downloadobect import Download
import http.client

import http

import urllib.parse

import time

class HttpDownload(Download):
    #local file
    def __init__(self, local_file='', url='', parent_queue=None, tokens_per_second=5):
        #Call super class
        Download.__init__(self, local_file, url, parent_queue, tokens_per_second)
        self.file_handle = open(local_file, "wb")
        self.url = url
        self.r = None
        self.so_far = 0
        print(url.netloc)
        self.http_conn = http.client.HTTPConnection(url.netloc)

    def do_download(self):
        #if problems come up, report them on the queue and abort self. Delete download
        if not self.r:
            s = self.http_conn.request('GET', self.url.path)

            self.r = self.http_conn.getresponse()
            print(self.r)
        out = self.r.read(1024)
        #print (len(out))
        self.file_handle.write(out)
        self.so_far = self.so_far + 1
        #if self.tokens == 1:
        #    print ("Done thus:" + str(self.so_far))


if __name__=="__main__":
    p = queue.Queue()
    m = HttpDownload('c:\\users\keyvin\Desktop\hello.iso', urllib.parse.urlparse('http://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-9.1.0-amd64-xfce-CD-1.iso'), p, 20000)
    m.start()
    while True:
        time.sleep(1)
        pass
