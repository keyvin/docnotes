from tkinter import *



class ScrolledList(Frame):
    def __init__(self, options, parent=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.makeWidget(options)

    def handleList(self, event):
        index = self.listbox.curselection()
        label = self.listbox.get(index)
        self.runCommand(label)

    def makeWidget(self, options):
        sbar = Scrollbar(self)
        hsbar = Scrollbar(self, orient='horizontal')
        list = Listbox(self)
        sbar.config(command=list.yview)
        hsbar.config(command=list.xview)
        list.config(yscrollcommand=sbar.set, xscrollcommand=hsbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        hsbar.pack(side=BOTTOM, fill=X)
        list.pack(side=LEFT, expand=YES, fill=BOTH)
        pos = 0
        for label in options:
            list.insert(pos, label)
            pos+=1
            #list.config(selectmode=SINGLE, setgrid=1)
        list.bind('<Double-1>', self.handleList)
        self.listbox=list

    def runCommand(self, selection):
        print ('You selected %s' % selection)


if __name__=='__main__':
    options=(('Lumberjack-%s' % x) for x in range(20))
    ScrolledList(options).mainloop()

