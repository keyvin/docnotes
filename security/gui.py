#we need a large display with a log (text edit), and an organized list of sensors and there status


import tkinter



class security_gui():
    def __init__(self):
        self.main_window = tkinter.Tk()
        self.status_label = tkinter.Label(self.main_window, text="Status: GOOD", bg='#000000', fg='#008000', font=("Times", 40, "bold"), anchor="w")
        self.state_frame = tkinter.Frame(self.main_window)
        self.log_frame = tkinter.Frame(self.main_window)
        self.state_text = tkinter.Text(self.state_frame, bg="#000000")
        self.log_text = tkinter.Text(self.log_frame)
        self.log_scrollbar = tkinter.Scrollbar(self.log_frame)
        self.log_scrollbar.config(command=self.log_text.yview)
        self.log_text.config(yscrollcommand=self.log_scrollbar.set)
        self.status_label.pack(side=tkinter.TOP,  fill=tkinter.X)
        self.log_frame.pack(side=tkinter.RIGHT, fill = tkinter.BOTH)
        self.state_frame.pack(side=tkinter.LEFT, fill = tkinter.BOTH, expand=True)
        self.state_text.pack(expand=True, fill=tkinter.BOTH)
        self.log_text.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.log_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)



s = security_gui()
s.main_window.mainloop()
