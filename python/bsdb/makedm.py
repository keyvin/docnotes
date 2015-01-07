import sqlite3

def fixtitle(title):
    title = title.replace('–','-') 
    string = title.replace("'","''")
    a = list(title)
    i = 0
    
   # while i < len(a):
       
    #    if a[i] =="'":
     #       tmp = a[i]
      #      a[i] = "'"
       #     a.insert(i+1, tmp)
        #    i=i+2
       # i=i+2
    #string = ''.join(a)
    print(string)
    return string

#function to read fields from file
fields = ['Tags','Title','Authors','Copies', 'Video', 'Leader','Large Print'] 


lines = open('/home/keyvin/Downloads/bsdb.csv', 'r')
lines.readline()
for i in lines:
    j = i.split(",")
    f = list(zip(fields, j))
    print (f)

    conn = sqlite3.connect("/home/keyvin/bsdb.dm")
    curr = conn.cursor()
    if j[4] == '':
        j[4] = 0
    j[1] = fixtitle(j[1])
    statement = "insert into book (title, copies, video) values ('%s',%d, %d);" % (j[1], int(j[3]), int(j[4]))
   
    print(statement)
    curr.execute(statement);
    conn.commit()
    book = curr.lastrowid

    
    if len(j[2].split()) > 1:
        statement = "select * from author where firstname='%s' and lastname='%s;" % (j[2].split()[0], j[2].split()[1])
        re = curr.execute(statement)
        if 
        statement = "insert into author (aid, firstname, lastname) values (0,'%s', '%s');" % (j[2].split()[0], j[2].split()[1])

    print(statement)
    curr.execute(statement)

    author = curr.lastrowid
    conn.commit()
    statement = "insert into tag (bid, tag) values(%d, '%s');" % (book,j[0])
    print(statement)
    curr.execute(statement);
    conn.commit()
    statement = 'insert into atob (bid,aid) values(%d, %d);' % (author, book)
    print(statement)
    curr.execute(statement)
    conn.commit() 
    

conn.close()

