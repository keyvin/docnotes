from tkinter import *

#we explicitly make root here, although not passing a root to a widget will create a default root
root = Tk()


trees = [('Tree 1', 'light blue'),
         ('Tree 2', 'light green'),
         ('Tree 3', 'red')
         ]

for (tree, color) in trees:
    win = Toplevel(root)
    win.title('Sing...')
    win.protocol('WM_DELETE_WINDOW', lambda:None)
    #win.iconbitmap('blah.bmp')
    msg = Button(win, text=tree, command=win.destroy)
    msg.pack(expand=YES, fill=BOTH)
    msg.config(padx=10, pady=10, bd=10, relief=RAISED)
    msg.config(bg='black', fg=color, font=('times', 30, 'bold italic'))
root.title('Lumberjack demo')
Label(root, text='Main window', width=30).pack()
Button(root, text='Quit ALL', command=root.quit).pack()
root.mainloop()


#adds widgets to the window, pops up three toplevels and uses toplevel protocols?
