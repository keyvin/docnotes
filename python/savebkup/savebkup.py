import sys
import os
import os.path
import shelve
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import shutil
import distutils.dir_util


class SaveDlg(Frame):
    def __init__(self, list=None, parent=None, **opts):
        Frame.__init__(self, parent,  opts)
        self.list=list
        self.lst_frame = Frame(self)
        self.list_box = Listbox(self.lst_frame, selectmode=SINGLE)
        self.sbar = Scrollbar(self.lst_frame)
        self.sbar.config(command=self.list_box.yview)
        self.list_box.config(yscrollcommand=self.sbar.set)
        
        #need a scrollbar for listbox. Need to link the two
        self.btn_frame = Frame(self)
        
        self.add_button = Button(self.btn_frame, text='Add', command=self.add_btn)
        self.del_button = Button(self.btn_frame, text='Delete', command=self.del_btn)
        self.copy_button = Button(self.btn_frame, text='Copy', command=self.cpy_btn)
        self.add_button.pack(side=LEFT)
        self.del_button.pack(side=LEFT)
        self.copy_button.pack(side=LEFT)
        self.list_box.pack(side=LEFT, expand=True, fill=BOTH)
        self.sbar.pack(side=LEFT, expand=False, fill=Y)
        self.lst_frame.pack(side=TOP, expand=True, fill=BOTH)
        self.btn_frame.pack(side=BOTTOM, expand=False , fill=None)
        self.load_list(list)
    def load_list(self, list):
        for i in list.shelve.keys():
            self.list_box.insert(END, i)
    def add_btn(self):
        add_dialog = AddDlg()
        self.wait_window(add_dialog.top_level)
        if not add_dialog.description:
            return
        if self.list.in_list(add_dialog.description):
            if not tkinter.messagebox.askokcancel("Already in the list, replace?"):
                return
            self.list.add_to_list(add_dialog.description, add_dialog.file)
            return
        self.list_box.insert(END, add_dialog.description)
        #Just use the description as the key on the shelve. 
        self.list.add_to_list(add_dialog.description, add_dialog.file)

    def del_btn(self):
        if self.list_box.curselection():
            self.list.delete_key(self.list_box.get(self.list_box.curselection()))
            self.list_box.delete(self.list_box.curselection())
			#delete from a shelve.
		
    def cpy_btn(self):
        copier(self.list, 'C:\\Users\\keyvi_000\\Google Drive\\saves\\')

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
        self.path_entry.delete(0,END)
        self.name_entry.delete(0, END)
    
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
    def get_list(self):
        retlist = []
        for i in self.shelve.keys():
            retlist.append((i,shelve[i]))
        return retlist
    def add_to_list(self, key, value):
        self.shelve[key] = value
    def delete_key(self, key):
        if key in self.shelve.keys():
            del self.shelve[key]
    def close_list(self):
        self.shelve.close()
    def get_file(self, key):
        if key in self.shelve.keys():
            return self.shelve[key]
        else:
            return None
    def in_list(self, key):
        return (key in self.shelve.keys())

def copier(list, targetdir):
        for key in list.shelve.keys():
            to_copy = list.get_file(key)
            if os.path.exists(to_copy):
                #shutil.copy(to_copy, targetdir)
                if os.path.isdir(to_copy):
                    distutils.dir_util.copy_tree(to_copy, targetdir+'\\'+key+'\\')
                if os.path.isfile(to_copy):
                    shutil.copy(to_copy, targetdir)
					

if __name__=='__main__':
	saved_list = FileList()
	SaveDlg(saved_list).pack(expand=True, fill=BOTH)
	mainloop()
	saved_list.close_list()