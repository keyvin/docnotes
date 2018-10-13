import os
import queue
import time
import win32file
import win32con
import threading

class dirWatch(threading.Thread): 

	def __init__(self, path="."):
		threading.Thread.__init__(self)
		self.change_queue = queue.Queue()
		self.ACTIONS = {
		1 : "Created",
		2 : "Deleted",
		3 : "Updated",
		4 : "Renamed from something",
		5 : "Renamed to something"
		}

		# Thanks to Claudio Grondi for the correct set of numbers
		self.FILE_LIST_DIRECTORY = 0x0001

		self.path_to_watch = path
		
		self.hDir = win32file.CreateFile (
		self.path_to_watch,
		self.FILE_LIST_DIRECTORY,
		win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
		None,
		win32con.OPEN_EXISTING,
		win32con.FILE_FLAG_BACKUP_SEMANTICS,
		None
		)

	def run(self):
		print("started watch")
		self.watch_file()
	
	
	def watch_file(self):
		#blocking call
		while 1:
			#
			# ReadDirectoryChangesW takes a previously-created
			# handle to a directory, a buffer size for results,
			# a flag to indicate whether to watch subtrees and
			# a filter of what changes to notify.
			#
			# NB Tim Juchcinski reports that he needed to up
			# the buffer size to be sure of picking up all
			# events when a large number of files were
			# deleted at once.
			#
			results = win32file.ReadDirectoryChangesW (
			self.hDir,
			1024,
			True,
			win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
			win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
			win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
			win32con.FILE_NOTIFY_CHANGE_SIZE |
			win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
			win32con.FILE_NOTIFY_CHANGE_SECURITY,
			None,
			None
			)
			msg = ''
			for action, file in results:
				full_filename = os.path.join (self.path_to_watch, file)
				msg = msg +  self.ACTIONS.get (action, "Unknown")+'\n'
			print(msg)
			self.change_queue.put("changed " + self.path_to_watch)
		
if __name__=="__main__":
	print("Started")
	watch1 = dirWatch("D:\\SteamLibrary\\steamapps\\common\\Knights of the Old Republic II\\saves\\")
	watch1.start()
	while True:
		time.sleep(10)
		#print("top")
		try: 
			n = watch1.change_queue.get(False)
			print(n)
		except:
			pass