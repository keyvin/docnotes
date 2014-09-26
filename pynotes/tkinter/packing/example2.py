#!/usr.bin/python3

from tkinter import *

win = Frame()

Button(win, text='Left', command= sys.exit).pack(side=LEFT)
Label(win, text='Top').pack(side=TOP)
Button(win, text='Right', command= sys.exit).pack(side=RIGHT)
win.mainloop()

