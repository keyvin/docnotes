from download_factory import DownloadFactory
from queue import Queue
#Collection abstraction.



class DownloadManager:
    def __init__(self):
        self.factory = DownloadFactory()
        self.downloads = []
        pass

    def add_download(self, url, target_file):
        try:
            self.downloads.append(self.factory.make_download(url, target_file, Queue()))
        except:
            pass
        try:
            self.downloads[-1].start()
        except:
            pass

    def gen_list(self):
        a = []
        for i in self.downloads:
            a.append((i.local_file, i.progress, i.size))
        print(a)
        return a

    def stop_all(self):
        for i in self.downloads:
            i.to_me.put("stop")