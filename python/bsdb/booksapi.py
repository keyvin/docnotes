import sys
import pickle
import os
import apiclient
from apiclient.discovery import build
isbn = sys.argv[1]

service = build('books', 'v1')
query = "isbn:%s" % (isbn,)
print query
s = service.volumes()

r = s.list(q=query)
r = r.execute()

d = r['items'][0]['volumeInfo']
print d['author']
