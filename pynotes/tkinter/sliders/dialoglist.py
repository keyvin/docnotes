#!/usr/bin/python3

from tkinter.filedialog import askopenfilename
from tkinter.colorchooser import askcolor
from tkinter.messagebox import askquestion, showerror
from tkinter.simpledialog import askfloat

demos = {
    'open':askopenfilename,
    'color': askcolor,
    'query': lambda: askquestion('Warning', 'You typed rm *\n confirm'),
    'error': lambda: showerror('Error', 'its dead'),
    'Input': lambda: askfloat('entry', 'enter number')
}

