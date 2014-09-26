#!/usr/bin/python3
"""This file contains a custom class that will get an entry. You should check if result is empty."""
from tkinter import *

class GetEntry(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.result = ''
        self.pack()
        self.ent = Entry(self)
        self.ent.pack(side=TOP, expand=YES, fill=X)
        self.btn = Button(self, text='Enter', command=self.endit)
        self.btn.pack(side=BOTTOM)
        self.btn.bind('<Return>', self.endit)
        #self.ent.bind('<Tab>', lambda a:self.btn.setfocus())
        
    def endit(self, event):
        self.result=self.ent.get()
        if self.result: Frame.quit(self)

if __name__ == '__main__':
    get = GetEntry()
    get.mainloop()
    print(get.result)
    
