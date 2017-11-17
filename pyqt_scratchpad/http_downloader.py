import queue
from downloader import Download
import http.client

import http

import urllib.parse

import time

class HttpDownload(Download):
    #local file
    def __init__(self, local_file='', url='', parent_queue=None, tokens_per_second=5):
        #Call super class
        Download.__init__(self, local_file, url, parent_queue, tokens_per_second)
        print (local_file)
        self.file_handle = open(str(local_file), "wb")


        self.r = None
        self.so_far = 0
        self.url = urllib.parse.urlparse(url)
        print(self.url.netloc)
        self.http_conn = http.client.HTTPConnection(self.url.netloc)

    def do_download(self):
        #if problems come up, report them on the queue and abort self. Delete download
        if not self.r:
            s = self.http_conn.request('GET', self.url.path)

            self.r = self.http_conn.getresponse()
            print(self.r)
        out = self.r.read(1024)
        print (len(out))
        if len(out) == 0:
            self._stop()
        self.file_handle.write(out)
        self.so_far = self.so_far + 1
        #if self.tokens == 1:
        #    print ("Done thus:" + str(self.so_far))


if __name__=="__main__":
    p = queue.Queue()
    m = HttpDownload('c:\\users\keyvin\Desktop\hello.jpg', urllib.parse.urlparse('https://i.imgur.com/csTzqqQ.jpg'), p, 20000)
    m.start()
    m.join()