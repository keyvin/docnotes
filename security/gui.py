#we need a large display with a log (text edit), and an organized list of sensors and there status


import tkinter
import network_server
import queue
#message_queue = queue.Queue()
status = {}



class security_gui():
    def __init__(self):
        self.main_window = tkinter.Tk()
        self.status_label = tkinter.Label(self.main_window, text="Status: GOOD", bg='#000000', fg='#008000', font=("Times", 40, "bold"), anchor="w")
        self.state_frame = tkinter.Frame(self.main_window)
        self.log_frame = tkinter.Frame(self.main_window)
        self.state_text = tkinter.Text(self.state_frame, bg="#000000", fg="green", font=("Times", 20, "bold"))
        self.log_text = tkinter.Text(self.log_frame, width=40)
        self.log_scrollbar = tkinter.Scrollbar(self.log_frame)
        self.log_scrollbar.config(command=self.log_text.yview)
        self.log_text.config(yscrollcommand=self.log_scrollbar.set)
        self.status_label.pack(side=tkinter.TOP,  fill=tkinter.X)
        self.log_frame.pack(side=tkinter.RIGHT, fill = tkinter.BOTH)
        self.state_frame.pack(side=tkinter.LEFT, fill = tkinter.BOTH, expand=True)
        self.state_text.pack(expand=True, fill=tkinter.BOTH)
        self.log_text.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.log_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.main_window.after(500, self.check_update)

    def check_update(self):
        network_server.check_sensors()
        while True:
            try:
                lines = str(network_server.message_queue.get(0), encoding='UTF-8').split('\n')
                for line in lines:
                   
                    self.log_text.insert(tkinter.END, line)
                    ip = line.split()[0]
                    #print (ip)
                    pin = line.split()[1]
                    #print(pin)
                    state = line.split(':')[1]
                    #print(state)
                    if ip in status.keys():    
                        if pin in status[ip].keys():
                            if not state == status[ip][pin]:
                                self.log_text.insert(tkinter.END, str((ip + " pin: " + pin + " changed state to " + state)))
                                status[ip][pin] = state
                        else:
                            print("new pin")
                            status[ip][pin] = state
                    else:
                        status[ip] = {}
                        self.log_text.insert(tkinter.END, "New IP: " + ip)
                    
            except:
                break
                pass
        

        self.main_window.after(500, self.check_update)




s = security_gui()
s.main_window.mainloop()
