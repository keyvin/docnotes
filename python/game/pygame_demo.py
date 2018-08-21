import pygame
import os

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:'+ name)
        raise SystemExit
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()



if __name__=="__main__":
    pygame.init()
    screen = pygame.display.set_mode((650, 500))
    pygame.display.set_caption('Game')
    pygame.mouse.set_visible(0)
    img_ld, r_rect = load_image("c:\\gfiles\\grass.png")
    img_wat, rect = load_image("c:\\gfiles\\water.png")
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    for x in range(int(650/50)):
        for y in range(int(500/50)):
            screen.blit(img_ld,(x*50,y*50))
            screen.blit(img_wat,(300,300))
    pygame.display.flip()
    breaks = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                breaks = True
        if breaks:
            break