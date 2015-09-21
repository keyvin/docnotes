from tkinter import *
import os
import pickle
import tkinter.filedialog
import tkinter.simpledialog
import tkinter.messagebox
global save_path
save_path = './save.pkl'
#data struct - {Pairname:[Sourcepath, destpath, isdir]}

class mainWin(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        self.t_label = Label(self, text="Save Mover")
        self.listbox_frame = Frame(self)
        self.list_box = Listbox(self.listbox_frame)
        self.b_frame = Frame(self)
        self.add_button = Button(self.b_frame, text="Add", command = self.add)
        self.del_button = Button(self.b_frame, text="Delete", command = self.delete)
        self.move_button = Button(self.b_frame, text="Move!", command = self.move)
        self.sbar = Scrollbar(self.listbox_frame, orient=VERTICAL)
        self.sbar.config(command=self.list_box.yview)
        self.list_box.config(yscrollcommand = self.sbar.set)
        self.t_label.pack(side=TOP)
        self.listbox_frame.pack(side=TOP)
        self.list_box.pack(side=LEFT)
        self.sbar.pack(side=RIGHT)
        self.b_frame.pack(side=TOP)
        self.del_button.pack(side=LEFT)
        self.add_button.pack(side=LEFT)
        self.move_button.pack(side=RIGHT)
        self.protocol('WM_DELETE_WINDOW', self.close_handler)
        self.loadPickle()
        
        # # for i in self.dir_list.keys():
            # self.list_box.insert(END, i)
    def add(self):
        name = tkinter.simpledialog.askstring("Name of game", "What is the name you want this pair to have?")
        isdir = tkinter.messagebox.askquestion(title="Direcrtory?", message="Is the source a directory?")
        
        if isdir == 'yes':
            isdir = True
            source = tkinter.filedialog.askdirectory(title="wWhat is the source folder")
        else:
            isdir = False
            source = tkinter.filedialog.askopenfilename(title="File to move")
        
        destination = tkinter.filedialog.askdirectory(title="Destination?")
        
        finalok = tkinter.messagebox.askokcancel(title="Create pair?", message= "Pair named: " + str(name) + "\n" + "Source "+ str(source) + "\n" + "Destination" + str(destination) )
        # print(finalok)
        if finalok:
            self.addpair(name, source, destination, isdir )
            
    def delete(self):
        active = self.list_box.get(ACTIVE)
        info = self.dir_list[active]
        delete_it = tkinter.messagebox.askokcancel(title = "Remove game?", message="Remove " + str(active) + "from save list?")
        if delete_it == True:
            del(self.dir_list[active])
            self.list_box.delete(ACTIVE)
    def move(self):
        pass
    def addpair(self, name, source, destination, isdir):
        self.dir_list[name] = [source, destination, isdir]
        self.addtolistbox(name)
    def addtolistbox(self, name):
        self.list_box.insert(END, name)
    def close_handler(self):
        file = open(save_path, 'wb')
        pickle.dump(self.dir_list, file)
        file.close()
        self.quit()
    def loadPickle(self):
        if os.path.isfile(save_path):
            file = open(save_path,'rb')
            self.dir_list = pickle.load(file)
            file.close()
            print(self.dir_list)
            for i in self.dir_list.keys():
                print(i)
                self.addtolistbox(i)
        else:
            self.dir_list = {}
            
# class 
			
if __name__ == "__main__":
    mainWin().mainloop()
    

        
