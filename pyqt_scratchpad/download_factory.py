"""This class parses a url and determines which child of the 
    download class to use
"""

import http_downloader
import urllib.parse

class DownloadFactory:
    def __init__(self):
        count_created = 0
        self.default_tokens_per_second = 20
        pass

    #returns a downloadobject instance
    #If failure, returns None
    def make_download(self, url = '', local_file = '', queue = None  ):
        url = urllib.parse(url)
        file = self.open_file(local_file)
        if url.scheme == 'http':
            downloader = http_downloader.HttpDownloader(file, url, queue, self.default_tokens_per_second )

    def open_file(self, local_file):
        file=None
        try:
            file = open(local_file, "wb")
        except IOError:
            pass
            #indicate failure to caller.
        return file


