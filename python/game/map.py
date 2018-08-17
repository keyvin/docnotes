import copy




cell_defaults = {"north": True, "south": True, "east": True, "west": True, "special": 0, "message": 0}

class cell:
    def __init__(self,  **kwargs):
        #assign defaults        
        self.properties = copy.deepcopy(cell_defaults)
        for i in kwargs.keys():
            self.properties[i] = kwargs[i]
        
        
        


class map:
    def __init__(self, **kwargs):
        self.x_size = 10
        self.y_size = 10
        self.grid = [[cell() for x in range(self.x_size)] for y in range(self.y_size)]
        pass

    def load(self, file_name):
        pass

    def navigate(self, command, party_obj):
        pass


    



    



