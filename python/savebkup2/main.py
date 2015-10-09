from tkinter import *
import os
import pickle
import tkinter.filedialog
import tkinter.simpledialog
import tkinter.messagebox
import zipfile
import shutil
import datetime
global save_path
global save_root
save_path = './save.pkl'
#data struct - {Pairname:[Sourcepath, destpath, isdir, clobber]}
save_root = 'C:\\Users\\admin\\keyvin@gmail.com\\x250savegames\\'

#Flow
# if one file 
#       delete existing zip (unless marked to not clobber)
#       create zip file with one file in it using zipfile
# If directory
#       delete existing zip file
#       use shutil to create the zip file again with latest version (unless no clobber)
#todo - I need to refactor to account for zip file saves. I should always clobber archives. 
#create a zip archive with just one file, or clobber. 

class mainWin(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.wm_title("File mover")
        self.t_label = Label(self, text="Destination: " + save_root)
        self.listbox_frame = Frame(self)
        self.list_box = Listbox(self.listbox_frame)
        self.b_frame = Frame(self)
        self.add_button = Button(self.b_frame, text="Add", command = self.add)
        self.del_button = Button(self.b_frame, text="Delete", command = self.delete)
        self.move_button = Button(self.b_frame, text="Move All", command = self.moveall)
        self.move_one_button = Button(self.b_frame, text="Move Current", command = self.moveone)
        self.sbar = Scrollbar(self.listbox_frame, orient=VERTICAL)
        self.sbar.config(command=self.list_box.yview)
        self.list_box.config(yscrollcommand = self.sbar.set)
        self.t_label.pack(side=TOP)
        self.listbox_frame.pack(side=TOP, expand=True, fill=BOTH)
        self.list_box.pack(side=LEFT, expand=True, fill=BOTH)
        self.sbar.pack(side=RIGHT, fill=Y)
        self.move_button.pack(side=RIGHT, expand =True, fill=X)       
        self.b_frame.pack(side=TOP, fill=X)
        self.del_button.pack(side=LEFT)
        self.add_button.pack(side=LEFT)
        
        self.move_one_button.pack(side=RIGHT)
        self.protocol('WM_DELETE_WINDOW', self.close_handler)
        self.loadPickle()
        
        # # for i in self.dir_list.keys():
            # self.list_box.insert(END, i)
    def add(self):
        name = tkinter.simpledialog.askstring("Name of game", "What is the name you want this pair to have?")
        isdir = tkinter.messagebox.askquestion(title="Direcrtory?", message="Is the source a directory?")
        
        if isdir == 'yes':
            isdir = True
            source = tkinter.filedialog.askdirectory(title="What is the source folder")
        else:
            isdir = False
            source = tkinter.filedialog.askopenfilename(title="File to move")
        
        #destination = tkinter.filedialog.askdirectory(title="Destination?")
        clobber = tkinter.messagebox.askquestion(title="Overwrite?", message="Do you wish to overwrite old versions?")
        finalok = tkinter.messagebox.askokcancel(title="Create pair?", message= "Pair named: " + str(name) + "\n" + "Source: "+ str(source) + "\n" +'\nClobber: ' + clobber  )
        # print(finalok)
        #if source == destination:
        #    tkinter.messagebox.showerror(title="Error!", message="Source and Destination are the same!")
        #    return
        if finalok:
            self.addpair(name, source, '', isdir, clobber )
        
            
    def delete(self):
        active = self.list_box.get(ACTIVE)
        info = self.dir_list[active]
        delete_it = tkinter.messagebox.askokcancel(title = "Remove game?", message="Remove " + str(active) + "from save list?")
        if delete_it == True:
            del(self.dir_list[active])
            self.list_box.delete(ACTIVE)
    def moveall(self):
        for i in self.dir_list.keys():
            if os.path.exists(self.dir_list[i][0]):
                self.domove(i)
    def moveone(self):
        current = self.list_box.get(ACTIVE)
        if not current:
            return
        else:
            if os.path.exists(self.dir_list[current][0]):
                self.domove(current)
    def domove(self, current):
        #directory
        if self.dir_list[current][2] == True:
            #clobber 
            if self.dir_list[current][3] == 'yes':
                shutil.make_archive(save_root + current + ".zip", "zip", self.dir_list[current][0] )
            else:
                #noclobber
                #get date and time
                date = datetime.datetime.now()
                date = date.isoformat().split('.')[0:-1][0].replace(':',"")
                shutil.make_archive(save_root + current + date + ".zip", "zip", self.dir_list[current][0] )
        else:
        #single file
            if  self.dir_list[current][3] == 'yes':
                #clobber
                zf = zipfile(save_root + current + '.zip', 'w')
                zf.write(self.dir_list[current][0])
                zf.close()
            else:
                #append to zipfile 
                date = datetime.datetime.now()
                date = date.isoformat().split('.')[0:-1][0].replace(':',"")
                zf = zipfile.ZipFile(save_root + current + date+ '.zip', 'w')
                
                zf.write(self.dir_list[current][0])
                zf.close()
        return
                
                
        pass
    def addpair(self, name, source, destination, isdir, clobber):
        self.dir_list[name] = [source, destination, isdir, clobber]
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
    

        
