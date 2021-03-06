#!/usr/bin/python3

#This file creates a frame sub class that verifies a quit request.

from tkinter import *
from tkinter.messagebox import *

class Quitter(Frame):
    def __init__(self, parent=None):
        #first thing with subclassing, call the parent's init function to properly initialize the object
        Frame.__init__(self, parent)
        self.pack()
        widget = Button(self, text='Quit', command=self.quit)
        widget.pack(side=LEFT, expand=YES, fill=BOTH)

    def quit(self):
        ans = askokcancel('Verify exit', "Really quit?")
        if ans: Frame.quit(self)

if __name__=='__main__': Quitter().mainloop()


