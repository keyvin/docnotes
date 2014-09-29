from tkinter import *
from quitter import Quitter
from dialoglist import demos

class Demo(Frame):
    def __init__(self, root=None,  **args):
        Frame.__init__(self, root, args)
        self.pack()
        self.var=IntVar()
        valhorizontal = Label(self, text='0', width=5)
        valvertical = Label(self, text='0', width= 5)
        slideh = Scale(self, label='Pick demo', command=self.onMove, variable=self.var, from_=0, to=len(demos)-1, length=200, tickinterval=1, showvalue=YES, orient='horizontal')
        slidev = Scale(self, label='Pick demo', command=self.onMove, variable=self.var, from_=0, to=len(demos)-1, length=200, tickinterval=1, showvalue=YES, orient='vertical')
        slideh.pack(side=TOP)
        slidev.pack(side=RIGHT)
        Quitter(self).pack(side=RIGHT)
        Button(self, text='Run Demo', command=self.runner).pack(side=LEFT)
        Button(self, text='State', command=self.getstate).pack(side=RIGHT)
        
    def onMove(self, event):
        print("Slider Moved")

    def runner(self):
        pos = self.var.get()
        print("You picked %s"%pos)
        demo = list(demos.values())[pos]
        demo()


    def getstate(self):
        print(self.var.get())


if __name__ == '__main__':
    Demo().mainloop()
              
    
