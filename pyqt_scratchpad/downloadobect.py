import queue
import time
import datetime
import threading


#divide it into microseconds

# seconds/ticks = tocs
class Download(threading.Thread):
    def __init__(self):
        self.error = True
        self.error_message = 'Nothing to download'
        self.from_me = queue.Queue()
    def __init__(self, local_file='', url='', parent_queue=None, tokens_per_second=50):
        self.error = False
        self.error_message = ''
        #get the file name
        self.local_file = local_file
        self.from_me = queue.Queue()
        self.to_me = parent_queue
        self.token_refill = tokens_per_second
        self.tokens = tokens_per_second
        threading.Thread.__init__(self)

    def run(self):
        start_time = datetime.datetime.now()

        while True:
            end_time = datetime.datetime.now()

            delta = end_time - start_time

            #Check Messages. Do something about them
            if self.tokens:
                self.from_me.put("depleting tokens")
                self.tokens = self.tokens - 1
                self.do_download()
            else:
                pass
                #self.from_me.put("Tokens expended")
                #time.sleep(.001)
            if delta.seconds >= 1:
                self.tokens = self.token_refill
                self.from_me.put("Refilling Bucket")
                start_time = datetime.datetime.now()


    #override for each type of download
    def do_download(self):
        #simulate a read.
        time.sleep(.1)

if __name__ == "__main__":
    parent_q = queue.Queue()
    d = Download("filename", "url", parent_q, 5 )
    d.start()
    while True:
        while not d.from_me.empty():
            print (d.from_me.get_nowait())

