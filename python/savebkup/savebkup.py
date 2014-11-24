import sys
import os
from tkinter import *


class savedlg(Frame):
    def __init__(self, parent=None, **opts):
        Frame.__init__(self, parent,  opts)
        self.lstframe = Frame(self)
        self.listbox = Listbox(self.lstframe)
        self.sbar = Scrollbar(self.lstframe)
        self.sbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.sbar.set)
        
        #need a scrollbar for listbox. Need to link the two
        self.btnframe = Frame(self)
        
        self.addbutton = Button(self.btnframe, text='Add', command=self.addbtn)
        self.delbutton = Button(self.btnframe, text='Delete', command=self.delbtn)
        self.copybutton = Button(self.btnframe, text='Copy', command=self.cpybtn)
        self.addbutton.pack(side=LEFT)
        self.delbutton.pack(side=LEFT)
        self.copybutton.pack(side=LEFT)
        self.listbox.pack(side=LEFT, expand=True, fill=BOTH)
        self.sbar.pack(side=RIGHT, expand=True, fill=Y)
        self.lstframe.pack(side=TOP, expand=True, fill=BOTH)
        self.btnframe.pack(side=BOTTOM, expand=False , fill=None)

    def addbtn(self):
        pass
    def delbtn(self):
        pass
    def cpybtn(self):
        pass

if __name__=='__main__':
    savedlg().pack(expand=True, fill=BOTH)
    mainloop()
