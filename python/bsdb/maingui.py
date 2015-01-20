from tkinter import * 

#todo - remove authors. keep keywords, browse studies. 

class RootWindow(Frame):
    def __init__(self, parent=None, **opts):
        Frame.__init__(self, parent, opts)
        self.browse_btn = Button(self, text="Browse all", command=self.browse)
        self.brs_kwd_btn = Button(self, text="Browse Keywords", command=self.keywd)
        self.brs_auth = Button(self, text="Browse Authors", command=self.auths)
        self.srch_auth = Button(self, text="Search Authors", command=self.sauths)
        self.srch_std = Button(self, text="Search Studies", command=self.s_studs)
        self.srch_kywd = Button(self, text="Search Keywords", command=self.s_kywd)
        self.add_std = Button(self, text="Add Study", command=self.a_std)
        self.add_auth = Button(self, text="Add Author", command = self.a_auth)
        self.browse_btn.pack(side=TOP, expand=True, fill=BOTH)
        self.brs_kwd_btn.pack(side=TOP, expand=True, fill=BOTH)
        self.brs_auth.pack(side=TOP, expand=True, fill=BOTH)
        self.srch_auth.pack(side=TOP, expand=True, fill=BOTH)
        self.srch_std.pack(side=TOP, expand=True, fill=BOTH)
        self.srch_kywd.pack(side=TOP, expand=True, fill=BOTH)
        self.add_std.pack(side=TOP, expand=True, fill=BOTH)
        self.add_auth.pack(side=TOP, expand=True, fill=BOTH)

    def browse(self):
        pass
    def keywd(self):
        pass
    def auths(self):
        pass
    def sauths(self):
        pass
    def s_studs(self):
        pass
    def s_kywd(self):
        pass
    def a_std(self):
        pass
    def a_auth(self):
        pass

if __name__=='__main__':
    RootWindow().pack(expand=True, fill=BOTH)
    mainloop()
