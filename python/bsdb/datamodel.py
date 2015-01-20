import sqlite3
import os.path
import subprocess
import pickle
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        print(idx)
        print(col)
        d[col[0]] = row[idx]
    return d

class DbInterface():

    #I need to check if a file exists. If not create a DB from the templace
    
    def __init__(self, dbFilename):
        self.db = self.open_DB(dbFilename)
        self.db.row_factory = dict_factory
    def return_all(self):
        #return all books. Needs to get books and tags. Should be stored in a dict
        curr = self.db.cursor()
        curr.execute('select * from book;')
        
        res = []
        for i in curr.fetchall():
            print(i)
            res.append(i)
        return res
           
    def add(self, isbn):
        #need some way to call the python2 file and get data
        #try:
            
        r = subprocess.Popen("/usr/bin/python booksapi.py "+  isbn, shell=True, stdout=subprocess.PIPE)
       
        out, err = r.communicate()
        #print(out)
        
       # except Exception as e:
        #    out, err 
        #    pass #book = subprocess.output(["/usr/bin/python booksapi.py", isbn], shell=True)
        fl = open('tmp.blah', 'rb')
        book = pickle.load(fl)
        #book = { 'title': 'Test book', 'subtitle':'Test subtitle', 'description':'Test Description', 'author':'Test Author' }
        cursor = self.db.cursor()
        cursor.execute("insert into book (title, subtitle, description, author, count, leader) values (?, ?, ?, ?, 0,0);", (book['title'], ' ', book['description'], ','.join(book['authors'])))
        self.db.commit()
              
                     
    def open_DB(self, filename):
        if not os.path.isfile(filename):
            return self.create_DB(filename)
        return sqlite3.connect(filename)
    
    def create_DB(self, filename):
        #check if db exists
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        cursor.execute('create table book (aid integer primary key, title varchar, subtitle varchar, description varchar, author varchar, count integer, leader integer);')
        conn.commit()
        cursor.execute('create table tag (aid integer not null, note varchar);')
        conn.commit()
        return conn


if __name__ == '__main__':
 db = DbInterface('test.db')
 #db.add('9780393063790')
 db.return_all()
 db.db.close()

