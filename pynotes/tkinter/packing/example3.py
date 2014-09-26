#!/usr.bin/python3

from tkinter import *
win = Frame()
win.pack()
Button(win, text='Right', command= sys.exit).pack(side=RIGHT)
Button(win, text='Left', command= sys.exit).pack(side=LEFT)
Label(win, text='Top').pack(side=TOP)

win.mainloop()
