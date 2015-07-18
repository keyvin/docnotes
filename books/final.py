import os
import os.path

books = []
dictionary = {}
tally = []

puts = open(".\\out_file", "w")
for dirpath, dirnames, filenames in os.walk("c:\\books\\"):
    for filename in [f for f in filenames if f.endswith(".out")]:
        books.append(os.path.join(dirpath, filename))

for i in books:
    print(i + "\n")
    print (str(len(dictionary)) + "\n")
    f = open(i,"r", errors="ignore")    
    i = f.readline()
    while i:
        o = i.split(' -')
        #print(o)
        c = int(o[0])
        w = ''.join(o[1:])
        w =w.rstrip()
        w =w.lstrip()
        #print(str(c) + w + "\n")
        if w == '':
            i = f.readline()
            continue
        if w in dictionary:
            dictionary[w] = dictionary[w] + c
           # print(str(dictionary[w])+ w + '\n')
        else:
            dictionary[w] = c
            #print(str(dictionary[w])+ w + '\n')
        #print (str(dictionary[w]) + " - " + w + '\n')
        i = f.readline()
        
    f.close()

print(len(dictionary.keys()))

count = 0
for i in dictionary.keys():
    count = count +1
    #puts.write(str(dictionary[i]) + i)
    tally.append([dictionary[i], i])
print (count)
print(tally[1])
print(len(tally))
print(dictionary["the"])
    #tally.append([dictionary[i], i])
#print(dictionary["the"])

a = sorted(tally, key=lambda i: i[0])
print (len(a))
for i in a:
    puts.write( str(i[0]) + " - " + i[1] + '\n')

#for i in tally:
#   puts.write(str(i[0]) + " - " + str(i[1]) + '\n')
