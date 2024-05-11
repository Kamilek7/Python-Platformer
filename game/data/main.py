
 # wszystkie definicje i wstepne wartosci
 # meow

from entities import *
from camera import Camera
from os import *
from xml.dom import minidom
from game_components import *

playerSpawn = (APP_WIDTH/5,60)

class SystemComponent:
    @staticmethod
    def loadMaps(_window):
        MAPS_DIR =  path.join(path.dirname(path.dirname(path.abspath(__file__))), 'maps')
        levels = []
        for files in listdir(MAPS_DIR):
            maps = []
            plik = minidom.parse(path.join(MAPS_DIR,files))
            mapa = plik.getElementsByTagName('map')[0]
            for child in mapa.childNodes:
                if child.tagName=="spawn":
                    global playerSpawn
                    playerSpawn = (int(child.getAttribute("x")),int(child.getAttribute("y")))
                elif child.tagName=="background":
                    maps.append(Grounds(_window,int(child.getAttribute("x")),int(child.getAttribute("y")),int(child.getAttribute("width")),int(child.getAttribute("height")),child.tagName,  background=child.getAttribute("background")))
                else:
                    maps.append(Grounds(_window,int(child.getAttribute("x")),int(child.getAttribute("y")),int(child.getAttribute("width")),int(child.getAttribute("height")),child.tagName, child.getAttribute("sprite"), foreground=child.getAttribute("foreground")))
            levels.append(maps)
        return levels
    
BIDEN_CHECK = path.join(path.dirname(path.abspath(__file__)), "joe_mama.jpg")
if not path.isfile(BIDEN_CHECK):
    raise ImportError("GDZIE JEST BIDEN")
else:
    pygame.init()
 # definicja dla wektora, dla latwych przeksztalcen
vector2d = pygame.math.Vector2
 # stałe
APP_HEIGHT = 600
APP_WIDTH = 800
MAX_FPS = 60
 # definicje dla okna
current_fps = pygame.time.Clock()
window = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT), RESIZABLE)
pygame.display.set_caption("Matka Kacpra - the GAYM")
running = True

 # elementy gry

levels = SystemComponent.loadMaps(window)
platforms = levels[0]
player = Player(window,playerSpawn[0],playerSpawn[1])
TextureComponent.setSprites(platforms,player)
moveables = [player]

backarea = pygame.Surface((window.get_width(),window.get_height()), pygame.SRCALPHA, 32)
backareaTemp = pygame.Surface((window.get_width(),window.get_height()), pygame.SRCALPHA, 32)
backshape = backarea.get_rect(center = (0,0))
backpos = vector2d((0,0))
backshape.topleft = backpos

main_camera = Camera(player, platforms, window.get_height()*0.75)

 # game loop
main_camera.centre_camera(vector2d(window.get_width(), window.get_height()))

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        elif event.type == VIDEORESIZE:
            main_camera.centre_camera(vector2d(window.get_width(), window.get_height()))
            backarea = pygame.transform.scale(backarea,(window.get_width(),window.get_height()))
    if TextureComponent.changeFlag:
        TextureComponent.changeFlag = False
        TextureComponent.alpha = 255
        if TextureComponent.fadedBackground != None:
            TextureComponent.fadeFlag = True
            backareaTemp = backarea
            TextureComponent.alpha=0
            backareaTemp.set_alpha(255)
            window.blit(backareaTemp, backshape)
        backarea = pygame.image.load(path.join(path.dirname(path.abspath(__file__)), 'backgrounds',TextureComponent.background)).convert()
        backarea = pygame.transform.scale(backarea,(window.get_width(),window.get_height()))
        backarea.set_alpha(TextureComponent.alpha)
    elif TextureComponent.fadeFlag:
        if TextureComponent.alpha<255:
            TextureComponent.alpha+=10
            backarea.set_alpha(TextureComponent.alpha)
            window.blit(backareaTemp, backshape)
        else:
            TextureComponent.alpha=255
            TextureComponent.fadeFlag=False
            backarea.set_alpha(TextureComponent.alpha)
    window.blit(backarea, backshape)
    for entity in moveables:
        if entity.spriteChange:
            TextureComponent.setSprites(platforms,player)
        entity.update(platforms)

    main_camera.update(window)
    if len(platforms)<len(TextureComponent.spritesB) + len(TextureComponent.spritesF)-1:
        TextureComponent.setSprites(platforms,player)
    for entity in TextureComponent.spritesB:
        #,special_flags= BLEND_ADD'
        window.blit(entity.area, entity.shape)
    for entity in TextureComponent.spritesF:
        #,special_flags= BLEND_ADD'
        window.blit(entity.area, entity.shape)
    pygame.display.update()
    current_fps.tick(MAX_FPS)