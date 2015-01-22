from tkinter import *
from datamodel import DbInterface

#need to add a cancel to the menubar
#Helper functions
def update_entry(entry, value):
    entry.configure(state = 'normal')
    entry.delete(0,END)
    entry.insert(0, value)
    entry.configure(state='readonly')
    return
def update_label(label, value):
    label['text'] = value
    return
def update_text(text, value):
    text.configure(state = 'normal')
    text.delete('0.0', END)
    text.insert('0.0', value)
    text.configure(state = 'disabled')
    return

class BrowseDb(Frame):
    #db object should contain information from a previous query to be browsed
    #TODO - add a delete button to this screen
     def __init__(self, parent=None, dbobj=None, **opts):
        Frame.__init__(self, parent, opts)
        #create frames
        self.editable_list = []
        self.dbobj = dbobj
        self.title_author_frm = Frame(self)
        self.description_frame = Frame(self)
        self.copies_video_frame = Frame(self)
        self.tags_frame = Frame(self)
        self.buttons_frame = Frame(self)
        #create entry and edit widgets
        self.title_entry = Entry(self.title_author_frm)
        self.editable_list.append(self.title_entry)
        self.authors_entry = Entry(self.title_author_frm)
        self.editable_list.append(self.authors_entry)
        self.description_text = Text(self.description_frame)
        #self.editable_list.append(self.description_text)
        self.copies_entry = Entry(self.copies_video_frame)
        self.editable_list.append(self.copies_entry)
        self.video_entry = Entry(self.copies_video_frame)
        self.editable_list.append(self.video_entry)
        self.tags_entry = Entry(self.tags_frame)
        self.editable_list.append(self.tags_entry)
        #buttons
        self.search_button = Button(self.buttons_frame, text='Search', command=self.search)
        self.execute_button = Button(self.buttons_frame, text='Execute Search', state='disabled',command=self.execute)
        self.edit_button = Button(self.buttons_frame, text='Edit', command=self.edit) #TODO, add stub
        self.cancel_button = Button(self.buttons_frame, text='Cancel', state='disabled', command=self.cancel)
        self.save_button = Button(self.buttons_frame, text='Save', state='disabled', command=self.save) #TODO, add stup, lock in init
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
        self.search_button.pack(side=LEFT)
        self.execute_button.pack(side=LEFT)
        self.edit_button.pack(side=LEFT)
        self.save_button.pack(side=LEFT)
        self.cancel_button.pack(side=LEFT)
        self.forward_button.pack(side=RIGHT)
        self.curr_record_lbl.pack(side=RIGHT)
        self.back_button.pack(side=RIGHT)
    
        self.pack()

        self.title_author_frm.pack(side=TOP)
        self.description_frame.pack(side=TOP)
        self.tags_frame.pack(side=TOP)
        self.copies_video_frame.pack(side=TOP) 
        self.buttons_frame.pack(side=TOP)
        self.pos=0
        self.get_all()
        self.make_uneditable()

     def make_editable(self):
        for i in self.editable_list:
            i.config(state='normal')
        self.description_text.config(state='normal')
     def make_uneditable(self):
        for i in self.editable_list:
            i.config(state='readonly')
        self.description_text.config(state='disabled')
     def clear_editable(self):
         for i in self.editable_list:
             update_entry(i, '')
         update_text(self.description_text, '')
     def unlock_buttons(self):
        pass
     def edit(self):
        self.edit_button.config(state='disabled')
        self.forward_button.configure(state='disabled')
        self.back_button.configure(state='disabled')
        self.save_button.configure(state='active')
        self.cancel_button.configure(state='active')
        self.make_editable()
     def execute(self):
        book = self.records[0]
        for i in book.keys():
            book[i] = ''
        
        book['title']="%"+self.title_entry.get()+"%"
        book['count']="%"+self.copies_entry.get()+"%"
        book['author']="%"+self.authors_entry.get()+"%"
        book['description'] = "%"+self.description_text.get('0.0', END)+"%"
        self.records = self.dbobj.search(book)
        self.pos = 0
        self.make_uneditable()
        self.set_screen()
     def search(self):
        self.clear_editable()
        self.edit()
        self.save_button.config(state='disabled')
        self.execute_button.config(state='active')
     def save(self):
         #basically a functional stub
        book=self.records[self.pos]
        book['title']=self.title_entry.get()
        book['count']=self.copies_entry.get()
        book['author']=self.authors_entry.get()
        book['description'] = self.description_text.get('0.0', END)
        #book['leader'] = self.leader_entry.get()
        self.dbobj.save(book)
        self.edit_button.config(state='active')
        self.forward_button.configure(state='active')
        self.back_button.configure(state='active')
        self.save_button.configure(state='disabled')
        self.cancel_button.configure(state='disabled')
        self.make_uneditable()
     def cancel(self):
        self.edit_button.config(state='active')
        self.forward_button.configure(state='active')
        self.back_button.configure(state='active')
        self.save_button.configure(state='disabled')
        self.cancel_button.configure(state='disabled')
        self.set_screen()
        self.make_uneditable()

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
        curr_rec = self.records[self.pos]
        update_label(self.curr_record_lbl, str(self.pos+1) + '/' + str(len(self.records)))
        update_entry(self.authors_entry, curr_rec['author']) 
        update_entry(self.title_entry, curr_rec['title'])
        update_entry(self.copies_entry, curr_rec['count'])
        update_entry(self.video_entry, curr_rec['video'])
        update_text(self.description_text, curr_rec['description'])
if __name__=='__main__':
    BrowseDb(dbobj=DbInterface('test.db')).mainloop()
