from tkinter import *
from scrolledtext import *
from quitter import *


class SimpleEdit(ScrolledText):
    def __init__(self, parent=None, text='', file=None):
        ScrolledText.__init__(self, parent, text, file)
        

    def makewidgets(self):
        btnframe = Frame(self)
        btnframe.pack(side=TOP, fill=X)
        Button(btnframe, text='Save', command=self.save).pack(side=LEFT)
        Button(btnframe, text='Find', command=self.find).pack(side=LEFT)
        Quitter(btn
        ScrolledText.makewidgets(self)

    def save(self):
        print ("In save stub")

    def find(self):
        print("In find stub")


if __name__=='__main__':
    root =Tk()
    se = SimpleEdit(root, text="Heya\n what is going on")
    se.pack()
    root.mainloop()
    
    
