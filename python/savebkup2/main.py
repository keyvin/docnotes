from tkinter import *
import os
import pickle
import tkinter.filedialog
import tkinter.simpledialog
import tkinter.messagebox
import zipfile
import shutil
import win32process
import datetime
import filewatch
global save_path
global save_root


save_path = './save.pkl'
#data struct - {Pairname:[Sourcepath, destpath, isdir, clobber, auto]}
save_root = 'C:\\Users\\zeeba\\keyvin@gmail.com\\saves\\big-laptop\\'

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
        self.t_label = Label(self, text="Destination: " + save_root, width=20)
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

        self.log_frame = Frame(self)
        self.log_sbar = Scrollbar(self.log_frame, orient=VERTICAL)
        self.log_widget = Text(self.log_frame,width=20, height=3)
        self.log_sbar.config(command=self.log_widget.yview)
        self.log_widget.config(yscrollcommand=self.log_sbar.set)
        self.log_sbar.pack(side=RIGHT, fill=Y)
        self.log_widget.pack(side=RIGHT, expand=True ,fill=BOTH)
        self.log_frame.pack(side=TOP, fill=BOTH)

        self.move_button.pack(side=RIGHT, expand =True, fill=X)
        self.b_frame.pack(side=TOP, fill=X)
        self.del_button.pack(side=LEFT)
        self.add_button.pack(side=LEFT)

        self.move_one_button.pack(side=RIGHT)
        self.protocol('WM_DELETE_WINDOW', self.close_handler)

        self.file_watchers = []
        self.loadPickle()
        self.after(10000, self.checkChange)
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
        auto_bkup = tkinter.messagebox.askquestion(title="Auto copy?", message="Do you wish to automatically copy saves?")
        finalok = tkinter.messagebox.askokcancel(title="Create pair?", message= "Pair named: " + str(name) + "\n" + "Source: "+ str(source) + "\n" +'\nClobber: ' + clobber  )
        # print(finalok)
        #if source == destination:
        #    tkinter.messagebox.showerror(title="Error!", message="Source and Destination are the same!")
        #    return
        if finalok:
            self.addpair(name, source, '', isdir, clobber, auto_bkup )
        if auto_bkup:
            tmp_watch = filewatch.dirWatch(self.dir_list[i][0], not self.dir_list[i][2], name)
            self.file_watchers.append(tmp_watch)
            self.writeLog("Watching " + name)
            tmp_watch.start()
            
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
            if self.dir_list[current][3] == 'yes':
                #clobber
                zf = zipfile.ZipFile(save_root + current + '.zip', 'w')
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

    def addpair(self, name, source, destination, isdir, clobber, auto_copy):
        self.dir_list[name] = [source, destination, isdir, clobber, auto_copy]
        self.addtolistbox(name)

    def addtolistbox(self, name):
        self.list_box.insert(END, name)

    def close_handler(self):
        file = open(save_path, 'wb')
        pickle.dump(self.dir_list, file)
        file.close()
        win32process.ExitProcess(0)

    def checkChange(self):
        print("anything changed?")
        for i in self.file_watchers:
            if i.change_queue.empty():
                continue
            try:
                while i.change_queue.get(False):
                    pass
            except:
                pass
            self.writeLog(i.name + " has changed. Copying.")
            if i.name in self.dir_list.keys():
                self.domove(i.name)
        self.after(10000, self.checkChange)

    def loadPickle(self):
        if os.path.isfile(save_path):
            file = open(save_path,'rb')
            self.dir_list = pickle.load(file)
            file.close()
            print(self.dir_list)
            for i in self.dir_list.keys():
                print(i)
                self.addtolistbox(i)
                if self.dir_list[i][4]:
                    tmp_watch = filewatch.dirWatch(self.dir_list[i][0], not self.dir_list[i][2], i)
                    self.file_watchers.append(tmp_watch)
                    tmp_watch.start()
                    self.writeLog("Watching " + i)
        else:
            self.dir_list = {}

    def writeLog(self, text='', state="normal"):
        self.log_widget.config(state='normal')
        self.log_widget.insert(END, text+'\n')

        self.log_widget.config(state='disabled')
            
# class 
			
if __name__ == "__main__":
    mainWin().mainloop()
    

        
