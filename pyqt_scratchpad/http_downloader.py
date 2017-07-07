import queue
from downloadobect import Download
import http.client
import http
import time

class HttpDownload(Download):
    def __init__(self, local_file='', url='', parent_queue=None, tokens_per_second=5):
        Download.__init__(self, local_file, url, parent_queue, tokens_per_second)
        self.file_handle = open(local_file, "wb")
        self.http_connection = http.client.HTTPConnection("gensho.ftp.acc.umu.se")
        self.r = None


    def do_download(self):
        if not self.r:
            self.http_connection.request('GET', '/debian-cd/current/amd64/iso-dvd/debian-9.0.0-amd64-DVD-1.iso')
            self.r = self.http_connection.getresponse()
        out = self.r.read(1024)
        self.file_handle.write(out)

if __name__=="__main__":
    p = queue.Queue()
    m = HttpDownload('c:\\users\keyvin\Desktop\hello.iso', '', p, 400)
    m.start()
    while True:
        time.sleep(1)
        pass
