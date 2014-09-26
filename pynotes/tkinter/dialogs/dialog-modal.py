#!/usr/bin/python3
# demonstrates a few modal prebuilt dialogs. 
from tkinter import *
from tkinter.messagebox import *

def callback():
    if askyesno('Verify', 'Do you really want to quit?'):
        showwarning('Yes', 'Quit not yet implemented')
    else:
        showinfo('No', 'Quit has been canceled')

errmsg = 'Sorry, no spam allowed!'
Button(text='Quit', command=callback).pack(fill=X)

#The reason this lambda is here is to pass defaults when the callback happens.
Button(text='Spam', command=(lambda: showerror('Spam', errmsg))).pack(fill=X)
mainloop()
