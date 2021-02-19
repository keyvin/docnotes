import sys

synonyms = {}
synonyms["N"] = ["NORTH", "N"]
synonyms["E"] = ["EAST", "E"]
synonyms["W"] = ["WEST", "W"]
synonyms["S"] = ["SOUTH", "S"]
synonyms["NE"] = ["NORTH EAST", "NE"]
synonyms["NW"] = ["NORTH WEST", "NW"]
synonyms["SE"] = ["SOUTH WEST", "SE"]
synonyms["SW"] = ["SOUTH WEST", "SW"]

class location:
    def __init__(self, location_file):
        """Takes a file to load location from."""
        self.room_num = location_file.read()
        if self.room_num == "":
            self.name = "EOF"
            return
        self.name = location_file.read()
        self.short_description = location_file.read()
        self.long_description = location_file.read()
        line = location_file.read()
        while not line.rstrip == "END" and not line == "":
            #do something here to parse exits
            line = location_file.read()
        #attributes (like dark, water, etc)
        
    def parse_exit(self, string:str):
        """helper function to parse out exit data"""
        #pass
        return
    
class exit:
    def __init__(self, location_file: str):
        """Parses an exit"""
        self.name = location_file.read()
        self.short_description = location_file.read()
        self.long_description = location_file.read()
        self.locked = location_file.read()
        self.key = location_file.read()
        self.bi_directional()
        self.synonyms = synonyms

        #attribute tags (noise blocking, dark, opaque, etc)

#an area's interface is that of a sparsely populated array. Data structure backing it is just a python list
#doubtful this will ever be a performance issue, but it does scale poorly

class area_file:
    def __init__(self, file_name):
        self.area_f = open(file_name, "r")
    def read(self):
        try:
            line = self.area_f.readline()
            print(line)
            if line == "" or line=="EOF":
                return ""
        except:
            print("Error on reading line")
            sys.exit()
        return line.rstrip()

            
class area:
    def __init__(self, area_file_name):
        self.locations = {}
        try:
            self.af = area_file(area_file_name)
            self.area_name = self.af.read()
            new_location = location(self.af)
            
            while not new_location.name == "EOF":
                self.locations[new_location.room_num] = new_location
                new_location = location(self.af)
        except:
            print("Error accessing file")
        self.af.area_f.close()
        
            
    def __getitem__(self, key):
        for i in self.locations:
            if i.room_num == i:
                return i
            else:
                return None
            
if __name__ == "__main__":
    new_area = area("world.txt")
    
        
        
