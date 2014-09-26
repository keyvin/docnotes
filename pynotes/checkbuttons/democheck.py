from tkinter import *
from dialoglist import demos
from quitter import Quitter

class Demo(Frame):
    def __init__(self, parent = None, **options):
        Frame.__init__(self, parent, options)
        self.pack()
        self.tools()
        Label(self, text="Check demos").pack()
        self.vars=[]
        for key in demos:
            var = IntVar()
            Checkbutton(self, text=key, variable=var, command=demos[key]).pack(side=LEFT)
            self.vars.append(var)

    def report(self):
        for var in self.vars:
            print(var.get(), end=' ')
            print()
    def tools(self):
        frm = Frame(self)
        frm.pack(side=RIGHT)
        Button(frm, text='state', command=self.report).pack(fill=X)
        Quitter(frm).pack(fill=X)

if __name__=='__main__': Demo().mainloop()
