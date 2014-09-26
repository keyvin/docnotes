from tkinter import *
from quitter import Quitter

def fetch():
    print('Input => "%s"' % ent.get())

root = Tk()
ent = Entry(root)

ent.insert(0, 'Type words here')
ent.pack(side=TOP, fill=X)
ent.focus()
ent.bind('<Return>', (lambda event: fetch()))
btn = Button(root, text='Fetch', command=fetch)
btn.pack(side=LEFT)

Quitter(root).pack(side=RIGHT)
root.mainloop()

