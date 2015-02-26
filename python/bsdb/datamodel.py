import sqlite3
import os.path
import subprocess
import pickle

#todo, return tags, avoid duplicates by checking primary key. 

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        print(idx)
        print(col)
        d[col[0]] = row[idx]
    return d

#helper functions

class DbInterface():

    #I need to check if a file exists. If not create a DB from the templace
    
    def __init__(self, dbFilename):
        self.db = self.open_DB(dbFilename)
        self.db.row_factory = dict_factory
    def make_empty_book(self):
        book = {}
        book['title']='Not Found',
        book['subtitle'] = ''
        book['author'] = ''
        book['description'] = 'No Results'
        book['video'] = '0'
        book['count'] = '0'
        book['isbn'] = ''
        book['bid'] = ''
        return book
    def search(self, book):
        for i in book.keys():
            if book[i]=='':
                book[i]='%'
            else:
                b = book[i].split(' ')
                b = '%'.join(b)
                book[i] = b
        curr = self.db.cursor()        
        query = "select * from book where title like '%s' and subtitle like '%s' and author like '%s' and description like '%s' and video like '%s' and count like '%s' and isbn like '%s';" % (book['title'], book['subtitle'], book['author'], book['description'], book['video'], book['count'], book['isbn'])
        print(query)                                                                                                                                                                                 
        curr.execute('select * from book where title like ? and subtitle like ? and author like ? and description like ? and video like ? and count like ? and isbn like ?;', (book['title'], book['subtitle'], book['author'], book['description'], book['video'], book['count'], book['isbn']))
        list = self.make_list(curr)
        if list ==[]:
            return [self.make_empty_book()]
        return list
    def return_all(self):
        #return all books. Needs to get books and tags. Should be stored in a dict
        curr = self.db.cursor()
        curr.execute('select * from book;')
        return self.make_list(curr)
    def make_list(self, curr):
        
        res = []
        for i in curr.fetchall():
            print(i)
            res.append(i)
        return res
        
    def save(self, book):
        curr = self.db.cursor()
        curr.execute('update book set title=?,subtitle=?,author=?,description=?,video=?,count=?, isbn=? where bid=?', (book['title'], book['subtitle'], book['author'], book['description'], book['video'], book['count'], book['isbn'], book['bid']))
        self.db.commit()
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
        print(book)
        if 'error' in book.keys():
            return False
        #book = { 'title': 'Test book', 'subtitle':'Test subtitle', 'description':'Test Description', 'author':'Test Author' }
        cursor = self.db.cursor()
        if 'description' not in book.keys():
            book['description'] = ''
        if 'subtitle' not in book.keys():
            book['subtitle'] = ''
        if 'averageRating' not in book.keys():
            book['averageRating'] = ''
        if 'authors' not in book.keys():
            book['authors'] = ''
        cursor.execute("insert into book (title, subtitle, description, author, count, leader, isbn, pagecount, averagerating, video ) values (?, ?, ?, ?, 0,0, ?, ?, ?, 0);",
                       (book['title'], book['subtitle'], book['description'], ','.join(book['authors']), isbn, book['pageCount'], book['averageRating']))
        self.db.commit()
        return True
                     
    def open_DB(self, filename):
        if not os.path.isfile(filename):
            return self.create_DB(filename)
        return sqlite3.connect(filename)
    
    def create_DB(self, filename):
        #check if db exists
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        cursor.execute('create table book (bid integer primary key, title varchar, subtitle varchar, description varchar, author varchar, count integer, leader integer, isbn varchar, publisher varchar, pagecount varchar, averagerating varchar, video varchar);')
        conn.commit()
        cursor.execute('create table tag (bid integer not null, note varchar);')
        conn.commit()
        return conn
    

if __name__ == '__main__':
 db = DbInterface('test.db')
 f = open("bulk.txt", "r")
 for i in f:
     b = i.rstrip()
     print(b)
     db.add(b)

 db.add('9780393063790')
 
 db.return_all()
 db.db.close()

