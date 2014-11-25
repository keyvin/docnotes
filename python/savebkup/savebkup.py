import sys
import os
import shelve
from tkinter import *
from tkinter.filedialog import askopenfilename

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
        self.sbar.pack(side=LEFT, expand=False, fill=Y)
        self.lstframe.pack(side=TOP, expand=True, fill=BOTH)
        self.btnframe.pack(side=BOTTOM, expand=False , fill=None)

    def addbtn(self):
        adddialog = adddlg()
        self.wait_window(adddialog.toplevel)
		
    def delbtn(self):
        pass
    def cpybtn(self):
        pass

class adddlg():
	def __init__(self, parent=None, **opts):
		self.toplevel = Toplevel(parent, opts)
		self.frame = Frame(self.toplevel)
		self.pathentry = Entry(self.toplevel, width=80, text='Select File or Directory')
		self.nameentry = Entry(self.toplevel, width=80, text='Enter name of game or file')
		self.selbutton = Button(self.toplevel, text='...', command=self.selbutton)		
		self.okbutton = Button(self.toplevel, text='Ok', command=self.okbutton)
		self.pathentry.pack()
		self.nameentry.pack()
		self.selbutton.pack()
		self.okbutton.pack()
		self.toplevel.protocol('WM_DELETE_WINDOW', self.toplevel.destroy)
		self.file =  ''
		self.description = ''
		self.toplevel.grab_set()
	def okbutton(self):
		self.file = self.pathentry.get()
		self.description = self.nameentry.get()
		self.toplevel.destroy()
	def selbutton(self):
		self.file = askopenfilename()
		self.pathentry.delete(0, END)
		self.pathentry.insert(0, self.file)
		
		
		
		
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
	savedlist = filelist()
	savedlist.closelist()
	mainloop()
	