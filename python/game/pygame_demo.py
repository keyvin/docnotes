import pygame
import maps
import party
import os


keymap = {pygame.K_LEFT:"west", pygame.K_RIGHT:"east", pygame.K_UP:"north", pygame.K_DOWN:"south"}

def load_image(name, colorkey=None):
    #fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(name)
    except pygame.error:
        print ('Cannot load image:'+ name)
        raise SystemExit
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()



x_size = 700
y_size = 700
tile_size = 50
max_x = int(x_size/tile_size)
max_y = int(y_size/tile_size)
#party is at x, y
#viewport stretches to x-6 to x + 6
#                      y-5 to y + 5

#translation from screen co-ordinate to map co-ordinate is given by the function
#                       player.x+ (screen_x-6)

def redraw(screen, current_map, party ):
    for screen_x in range(0, max_x):
        for screen_y in range(0, max_y):
            map_x = party.location_x + (screen_x-6)
            map_y = party.location_y + (screen_y-6)
            if map_x < 0 or map_x >= current_map.x_size or map_y < 0 or map_y >= current_map.y_size:
                tile = img_wat
            else:
#                print(f"Party {party.location_x},{party.location_y}")
#                print(f"{map_x}, {map_y} : {current_map.x_size}, {current_map.y_size}")
                tile = tile_map[current_map.terrain(map_x, map_y )]

            screen.blit(tile,(screen_x*50,screen_y*50))

    screen.blit(img_player,( x_size/2-25, y_size/2-25) )




amap = maps.maps()
aparty = party.party()
pygame.init()
screen = pygame.display.set_mode((x_size, y_size))
pygame.display.set_caption('Game')
pygame.mouse.set_visible(0)
img_ld, r_rect = load_image("grass.png")
img_wat, rect = load_image("water.png")
img_mtn, rect = load_image("mountain.png")
img_player, rect = load_image("player.png")
tile_map = {'water':img_wat, 'mountain':img_mtn, 'grass':img_ld}
background = pygame.Surface(screen.get_size())
background = background.convert()

background.fill((250, 250, 250))


pygame.display.flip()
breaks = False
redraw(screen, amap, aparty)
pygame.display.flip()

do_draw = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            breaks = True
        elif event.type == pygame.KEYDOWN and event.key in keymap.keys():
            amap.navigate(keymap[event.key], aparty)
            do_draw = True

    if breaks:
        break

    if do_draw:
        do_draw = False
        redraw(screen, amap, aparty)
        pygame.display.flip()
