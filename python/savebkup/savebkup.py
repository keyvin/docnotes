import sys
import os
import shelve
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

#This class loads and saves state for the file list, maintains a list of files in the last backup. For ease of use, uses a shelve
class filelist():
    def __init__(self, path=''):
        if path:
            self.path = path
        else:
            self.path = './savelist.shlf'
        self.shelve=shelve.open(self.path)
    def getlist(self):
        retlist = []
        for i in self.shelve.keys():
            retlist.append((i,shelve[i]))
        return retlist
    def addlist(self, key, value):
        self.shelve[key] = value
    def closelist(self):
        self.shelve.close()
        
                

if __name__=='__main__':
    savedlg().pack(expand=True, fill=BOTH)
    mainloop()
