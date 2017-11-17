"""This class parses a url and determines which child of the 
    download class to use
"""

import http_downloader
import urllib.parse

class DownloadFactory:
    def __init__(self):
        count_created = 0
        self.default_tokens_per_second = 2000
        pass

    #returns a downloadobject instance
    #If failure, returns None
    def make_download(self, url = '', local_file = '', queue = None  ):
        purl = urllib.parse.urlparse(url)[0] #just scheme
        #file = self.open_file(local_file)
        if purl == 'http' or purl == 'https':
            downloader = http_downloader.HttpDownload(local_file, url, queue, self.default_tokens_per_second )
        return downloader
    def open_file(self, local_file):
        file=None
        try:
            file = open(local_file, "wb")
        except IOError:
            pass
            #indicate failure to caller.
        return file


