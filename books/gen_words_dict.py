wordlist = {}

words = open("354984si.ngl", "r")

i = words.readline()

while i:
    i = i.rstrip()
    l = list(i)
    l.sort()
    w = ''.join(l)
    if w in wordlist:
        wordlist[w].append(i)
    else:
        wordlist[w] = [i]
    i = words.readline()

print(len(wordlist))

occurence = open("out_file", "r")


i = occurence.readline()
output = open("english_words", "w")
while i:
    word = i.split(" -")
    word = ''.join(word[1:]).lstrip()
    word = word.rstrip()
    hsh = list(word)
    hsh.sort()
    
    hsh = ''.join(hsh)
    
    if hsh in wordlist:
        if word in wordlist[hsh]:
            output.write(i)
    i = occurence.readline()     
occurence.close()
words.close()
output.close()
    
