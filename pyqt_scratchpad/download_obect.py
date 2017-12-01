import queue
import time
import datetime
from threading import thread

class Download():
    def __init__(self):
        self.error = True
        self.error_message = 'Nothing to download'

    def __init__(self, local_file, url, parent_queue, tokens_per_second):
        self.error = False
        self.error_message = ''
        #get the file name
        self.local_file = local_file
        self.from_me = queue.Queue()
        self.to_me = parent_queue
        self.token_refill = tokens_per_second
        self.tokens = tokens_per_second

    def mainThread(self):
        start_time = datetime.datetime.now()

        while more:
            end_time = datetime.datetime.now()

            delta = end_time - start_time
            if delta.seconds >= 1:
                self.tokens = self.token_refill
                start_time = datetime.datetime.now()



