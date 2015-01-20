from tkinter import *
from datamodel import DbInterface
class BrowseDb(Frame):
    #db object should contain information from a previous query to be browsed
    #TODO - add a delete button to this screen
     def __init__(self, parent=None, dbobj=None, **opts):
        Frame.__init__(self, parent, opts)
        #create frames
        self.dbobj = dbobj
        self.title_author_frm = Frame(self)
        self.description_frame = Frame(self)
        self.copies_video_frame = Frame(self)
        self.tags_frame = Frame(self)
        self.buttons_frame = Frame(self)
        #create entry and edit widgets
        self.title_entry = Entry(self.title_author_frm)
        self.authors_entry = Entry(self.title_author_frm)
        self.description_text = Text(self.description_frame)
        self.copies_entry = Entry(self.copies_video_frame)
        self.video_entry = Entry(self.copies_video_frame)
        self.tags_entry = Entry(self.tags_frame)
        #buttons
        self.edit_button = Button(self.buttons_frame, text='Edit', command=None) #TODO, add stub
        self.save_button = Button(self.buttons_frame, text='Save', command=None) #TODO, add stup, lock in init
        self.back_button = Button(self.buttons_frame, text='<', command=self.previous) #TODO add stub
        self.forward_button = Button(self.buttons_frame, text='>', command=self.next) #todo add stub, check in init if db has more than one
        #TODO should add search by author, search by tags, search description, search copies

        #labels - Keep? Easier than packing
        self.title_lbl = Label(self.title_author_frm, text="Title")
        self.author_lbl = Label(self.title_author_frm, text="Author(s)")
        self.description_lbl = Label(self.description_frame, text="Description")
        self.copies_lbl = Label(self.copies_video_frame, text="Copies")
        self.video_lbl = Label(self.copies_video_frame, text="Video(s)")
        self.tags_lbl = Label(self.tags_frame, text="Tags (Topics)")
        self.curr_record_lbl = Label(self.buttons_frame, text="1/1") #todo - set this label based on results
        #Function to update curr_record_lbl when necessary (new search)
        
        #pack title author stuff
        self.title_lbl.pack(side=LEFT)
        self.title_entry.pack(side=RIGHT)
        self.author_lbl.pack(side=RIGHT)
        self.authors_entry.pack(side=RIGHT)
        #pack description:
        self.description_lbl.pack(side=TOP)
        self.description_text.pack(side=TOP)
        #Pack Tags
        self.tags_lbl.pack(side=LEFT)
        self.tags_entry.pack(side=LEFT)
        #pack copies/video
        self.copies_lbl.pack(side=LEFT)
        self.copies_entry.pack(side=LEFT)
        self.video_lbl.pack(side=RIGHT)
        self.video_entry.pack(side=RIGHT)
        #pack BUTTONS
        self.edit_button.pack(side=LEFT)
        self.save_button.pack(side=LEFT)
        self.forward_button.pack(side=RIGHT)
        self.curr_record_lbl.pack(side=RIGHT)
        self.back_button.pack(side=RIGHT)

        self.pack()

        self.title_author_frm.pack(side=TOP)
        self.description_frame.pack(side=TOP)
        self.tags_frame.pack(side=TOP)
        self.copies_video_frame.pack(side=TOP) 
        self.buttons_frame.pack(side=TOP)
        self.get_all()
     def previous(self):
         if not self.pos == 0:
             self.pos = self.pos-1
             self.set_screen()
     def next(self):
         if not self.pos == len(self.records): 
            self.pos = self.pos+1
            
            self.set_screen()
     def get_all(self):
        self.records = self.dbobj.return_all()
        self.pos = 0
        #self.curr_record_lbl['text'] = '0/' + str(len(self.records))
        self.set_screen()
     def set_screen(self):
        self.curr_record_lbl['text'] = str(self.pos+1) + '/' + str(len(self.records))
        self.authors_entry.delete(0,END)
        print(self.records)
        self.authors_entry.insert(0,self.records[self.pos]['author'])

if __name__=='__main__':
    BrowseDb(dbobj=DbInterface('test.db')).mainloop()
