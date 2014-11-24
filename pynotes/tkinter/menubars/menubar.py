from tkinter import *

from tkinter.messagebox import *

def notdone():
    showerror('Not Implemented', 'duh')

def makemenu(win):
    top = Menu(win)
###Note the lowercase top here....
    win.config(menu=top)
    file = Menu(top)
    file.add_command(label='New', command=notdone, underline=0)
    file.add_command(label='Save', command=notdone, underline=0)
    top.add_cascade(label='File', menu=file, underline=0)

    edit=Menu(top, tearoff=False)
    edit.add_command(label='Cut', command=notdone, underline=0)
    edit.add_separator()
    edit.add_command(label='bar dude', command=notdone, underline=0)
    top.add_cascade(label='Edit', menu=edit, underline=0)
    submenu = Menu(edit, tearoff=True)
    submenu.add_command(label='spam', command=notdone, underline=0)
    edit.add_cascade(label='Submenu', menu=submenu, underline=0)

if __name__=='__main__':
    root = Tk()
    root.title("Menu Window")
    makemenu(root)
    msg = Label(root, text='Basic menus')
    msg.pack(expand=YES, fill=BOTH)
    root.mainloop()
    

