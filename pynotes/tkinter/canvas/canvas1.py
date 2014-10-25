"Demo the basic canvas interfaces"

from tkinter import *

canvas = Canvas(width=525, height=300, bg='white')
canvas.pack(expand=YES, fill=BOTH)

canvas.create_line(100,100,200,200)
canvas.create_line(100,200,200,300)

for i in range(1, 20, 2):
    canvas.create_line(0, i, 50, i)

widget = Label(canvas, text='Spam', fg='white', bg='black')
widget.pack()

canvas.create_window(100,100, window=widget)

mainloop()
