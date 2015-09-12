from tkinter import *
import os
import pickle

global save_path
save_path = './save.pkl'
class mainWin(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.loadPickle()
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
        
        for i in self.dir_list.keys():
            self.list_box.insert(END, i)
    def add(self):
        pass
    def delete(self):
        pass
    def move(self):
        pass
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
        else:
            self.dir_list = {'Name':'Dir'}
            
if __name__ == "__main__":
    mainWin().mainloop()
    

        
