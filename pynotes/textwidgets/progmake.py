"""make rows of labels aligned with entry widgets."""

from tkinter import *
from quitter import Quitter
fields = ["Name", "Job", "pay"]

def fetch(entries):
    for entry in entries:
        print ('input %s\n', entry.get())

def makeform(root, fields):
    entries = []
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=5, text=field)
        ent = Entry(row)
        row.pack(side=TOP, fill=X)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries.append(ent)
    return entries

if __name__=='__main__':
    root = Tk()
    ents = makeform(root, fields)
    root.bind('<Return>', fetch(ents))
    Button(root, text='get fields', command=lambda: fetch(ents)).pack(side=RIGHT)
    Quitter(root).pack(side=RIGHT)
    root.mainloop()
