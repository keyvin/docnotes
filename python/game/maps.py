import copy

map_commands = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}

cell_defaults = {"north": True, "south": True, "east": True, "west": True, "special": 0, "message": 0, "type": "grass"}

class cell:
    def __init__(self,  **kwargs):
        #assign defaults        
        self.properties = copy.deepcopy(cell_defaults)
        for i in kwargs.keys():
            self.properties[i] = kwargs[i]
    def __getitem__(self, key):
        return self.properties[key]
                
class maps:
    def __init__(self, **kwargs):
        self.x_size = 100
        self.y_size = 100
        self.grid = [[cell() for x in range(self.x_size)] for y in range(self.y_size)]
        pass

    def terrain(self, x, y):
        return self.grid[x][y]["type"]

    def load(self, file_name):
        pass

    def navigate(self, command, party_obj):
       
        curr_x = party_obj.location_x
        curr_y = party_obj.location_y

        curr_x = curr_x + map_commands[command][0]
        curr_y = curr_y + map_commands[command][1]
        if curr_x < 0 or curr_x > self.x_size:
            print("Out of Bounds")
            pass
            
        
            #xfault
        if curr_y < 0 or curr_y > self.y_size:
            print("Out of Bounds")
            
            #yfault
        if not party_obj.passable(self.grid[curr_x][curr_y]):
            print("Impassible Terrain")
            pass
            #travel fault

        #move was allright
        party_obj.location_x = curr_x
        party_obj.location_y = curr_y
        return
    

