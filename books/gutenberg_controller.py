import sys
import os
from threading import Thread

import _thread
import queue
from subprocess import Popen, PIPE
import time
books = []

for dirpath, dirnames, filenames in os.walk("c:\\books"):
    for filename in [f for f in filenames if f.endswith(".txt")]:
        books.append(os.path.join(dirpath, filename))

quarter = int(len(books)/4)

first = books[0:quarter]
second = books[quarter+1:quarter*2]
third = books[quarter*2+1:quarter*3]
fourth =  books[quarter*3+1:len(books)]
outqueue = queue.Queue()


def book_thread(book_list, output_queue):
    for book in book_list:
        process = Popen(['analyzer.exe', book])
        if process.wait() != 0:
            #ouput_queue.write(book + " error\n")
            pass
       # else:
           # output_queue.write(book + " done\n")

a = _thread.start_new_thread(book_thread, (first, outqueue))
b = _thread.start_new_thread(book_thread, (second, outqueue))
c = _thread.start_new_thread(book_thread, (third, outqueue))
d = _thread.start_new_thread(book_thread, (fourth, outqueue))                              


time.sleep(300)
                              
