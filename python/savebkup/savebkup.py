import sys
import os
import shelve
from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.filedialog

class SaveDlg(Frame):
    def __init__(self, parent=None, **opts):
        Frame.__init__(self, parent,  opts)
        self.lstframe = Frame(self)
        self.listbox = Listbox(self.lstframe)
        self.sbar = Scrollbar(self.lstframe)
        self.sbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.sbar.set)
        
        #need a scrollbar for listbox. Need to link the two
        self.btnframe = Frame(self)
        
        self.addbutton = Button(self.btnframe, text='Add', command=self.add_btn)
        self.delbutton = Button(self.btnframe, text='Delete', command=self.del_btn)
        self.copybutton = Button(self.btnframe, text='Copy', command=self.cpy_btn)
        self.addbutton.pack(side=LEFT)
        self.delbutton.pack(side=LEFT)
        self.copybutton.pack(side=LEFT)
        self.listbox.pack(side=LEFT, expand=True, fill=BOTH)
        self.sbar.pack(side=LEFT, expand=False, fill=Y)
        self.lstframe.pack(side=TOP, expand=True, fill=BOTH)
        self.btnframe.pack(side=BOTTOM, expand=False , fill=None)

    def add_btn(self):
        add_dialog = AddDlg()
        self.wait_window(add_dialog.top_level)
        self.listbox.insert(0, add_dialog.description)
		#do something here with the data from that dialog
    def del_btn(self):
        pass
    def cpy_btn(self):
        pass

class AddDlg():
	def __init__(self, parent=None, **opts):
		self.top_level = Toplevel(parent, opts)
		self.file_frame = Frame(self.top_level)
		
		self.lbl_1 = Label(self.file_frame, text='Select File Name')
		self.path_entry = Entry(self.file_frame, width=40, text='Select File or Directory')
		self.name_entry = Entry(self.top_level, width=40, text='Enter name of game or file')
		self.sel_file_button = Button(self.file_frame, text='Open File', command=self.sel_file_button)		
		self.sel_dir_button = Button(self.file_frame, text='Open Directory', command=self.sel_dir_button)
		self.ok_button = Button(self.top_level, text='Ok', command=self.ok_button)
		self.path_entry.pack(side=LEFT, expand=True, fill=X)		
		self.sel_file_button.pack(side=LEFT, expand=False)
		self.sel_dir_button.pack(side=LEFT, expand=False)
		self.file_frame.pack(side=TOP, expand=True, fill=X)
		self.name_entry.pack(side=TOP, expand=True, fill=X)
		self.ok_button.pack(side=BOTTOM)
		self.top_level.protocol('WM_DELETE_WINDOW', self.top_level.destroy)
		self.file =  ''
		self.description = ''
		self.top_level.grab_set()
	def ok_button(self):
		self.file = self.path_entry.get()
		self.description = self.name_entry.get()
		self.top_level.destroy()
	def sel_file_button(self):
		self.file = tkinter.filedialog.askopenfilename()
		self.path_entry.delete(0, END)
		self.path_entry.insert(0, self.file)
	def sel_dir_button(self):
		self.file = tkinter.filedialog.askdirectory()
		self.path_entry.delete(0, END)
		self.path_entry.insert(0, self.file)
		
		
		
#This class loads and saves state for the file list, maintains a list of files in the last backup. For ease of use, uses a shelve
class FileList():
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
	SaveDlg().pack(expand=True, fill=BOTH)
	SavedList = FileList()
	SavedList.closelist()
	mainloop()
	