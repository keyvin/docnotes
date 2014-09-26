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
        slideh = Slider(self, label='Pick demo', command self.onMove, variable=self.var, from_=0, to=len(demos)-1, length=200, tickinterval=1, showvalue=YES, orient='horizontal')
        slidev = Slider(self, label='Pick demo', command self.onMove, variable=self.var, from_=0, to=len(demos)-1, length=200, tickinterval=1, showvalue=YES, orient, 'vertical')
        Quitter(self).pack(side=RIGHT)
        Button(self, text='Run Demo', command=self.runner).pack(side=LEFT)
        Button(self, text='State', command=self.getstate).pack(side=RIGHT)
        
