#this file will have code for party management, moving the party, etc.


class party:
    def __init__(self):
        self.party = [{'name': "Char 1", 'hp': 100, 'str': 15, 'con': 15, 'dex': 15, 'gear':[]}]
        self.location_x = 4
        self.location_y = 4

    def passable(self, terrain):
        print(terrain)
        if terrain == "Water":
            return False
        return True
        pass
