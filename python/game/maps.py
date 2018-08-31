import copy

map_commands = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}

map_terrains = {'w': 'water', 'g': 'grass', 'm': "mountain"}
w = 'w'
g = 'g'
m = 'm'

map1 = [[w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w],
        [w,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,g,g,g,g,g,m,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,g,g,g,g,g,m,m,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,g,g,g,g,g,m,m,m,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,g,g,g,g,g,g,w,m,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,g,g,g,g,g,g,g,m,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,g,g,g,g,g,g,g,m,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,g,g,g,g,g,g,g,m,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,g,g,g,g,g,g,g,m,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,g,g,g,g,g,g,g,m,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,g,g,g,g,g,g,g,m,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,g,g,g,g,g,g,g,m,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,g,g,g,g,g,g,g,m,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,g,g,g,g,g,g,g,m,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,g,g,g,g,g,g,g,m,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,g,g,g,g,g,g,g,m,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w],
        [w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w]]



cell_defaults = {"north": True, "south": True, "east": True, "west": True, "special": 0, "message": 0, "type": "grass"}

class cell:
    def __init__(self, my_type, **kwargs):
        #assign defaults        
        self.properties = copy.deepcopy(cell_defaults)
        for i in kwargs.keys():
            self.properties[i] = kwargs[i]
        self.properties["type"] = map_terrains[my_type]

    def __getitem__(self, key):
        return self.properties[key]
                
class maps:
    def __init__(self, **kwargs):
        self.x_size = len(map1[0])
        self.y_size = len(map1)
        grid = []
        for y in range(self.y_size):
            row = []
            for x in range(self.x_size):
                row.append(cell(map1[y][x]))
            grid.append(row)
        self.grid = grid



    def terrain(self, x, y):
        return self.grid[y][x]["type"]

    def load(self, file_name):
        pass

    def navigate(self, command, party_obj):
       
        curr_x = party_obj.location_x
        curr_y = party_obj.location_y

        curr_x = curr_x + map_commands[command][0]
        curr_y = curr_y + map_commands[command][1]
        if curr_x < 0 or curr_x >= self.x_size:
            print("Out of Bounds")
            return


        if curr_y < 0 or curr_y >= self.y_size:
            print("Out of Bounds")
            return

        print(f"{curr_y}, {curr_x}")

        if not party_obj.passable(self.grid[curr_y][curr_x]["type"]):
            print("Impassible Terrain")
            return



        #move was allright
        party_obj.location_x = curr_x
        party_obj.location_y = curr_y
        return
    

