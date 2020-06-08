import sys

class location:
    def __init__(self, location_file):
        self.room_num = location_file.read()
        self.name = location_file.read()
        self.short_description = location_file.read()
        self.long_description = location_file.read()
        line = location_file.read()
        while not line.rstrip == "END":
            #do something here to parse exits
            pass
        #attributes (like dark, water, etc)

class exit:
    def __init__(self, location_file):
        self.name = location_file.read()
        self.short_description = location_file.read()
        self.long_description = location_file.read()
        self.locked = location_file.read()
        self.key = location_file.read()
        self.bi_directional()
        #attribute tags (noise blocking, dark, opaque, etc)

#an area's interface is that of a sparsely populated array. Data structure backing it is just a python list
#doubtful this will ever be a performance issue, but it does scale poorly

class area_file:
    def __init__(self, file_name):
        self.area_f = open(file_name, "r")
    def read():
        try:
            line = self.area_f.readline()
            return line
        except:
            print("Error on reading line")
            sys.exit()
        

            
class area:
    def __init__(self, area_file_name):
        self.locations = []
        
    def __getitem__(self, key):
        for i in locations:
            if i.room_num == i:
                return i
            else:
                return None
            
            
        
        
