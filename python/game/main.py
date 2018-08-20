import maps
import party





if __name__ == "__main__":
    a_party = party.party()
    amap = maps.maps()
    status_location = "Location %d, %d - Terrain %s"
    status_party = "%s, HP - %d"
    print("Welcome to game")
    print( status_location % (a_party.location_x, a_party.location_y, amap.terrain(a_party.location_x, a_party.location_y)))
    print( status_party % (a_party.party[0]["name"], a_party.party[0]["hp"]))
    input()
                          
          

