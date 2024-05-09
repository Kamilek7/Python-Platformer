
 # wszystkie definicje i wstepne wartosci
 # meow

from entities import *
from camera import Camera
from os import *
from xml.dom import minidom

playerSpawn = (APP_WIDTH/5,60)

class SystemComponent:
    spritesB = pygame.sprite.Group()
    spritesF = pygame.sprite.Group()
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
                    print(child.tagName)
                    global playerSpawn
                    playerSpawn = (int(child.getAttribute("x")),int(child.getAttribute("y")))
                else:
                    maps.append(Grounds(_window,int(child.getAttribute("x")),int(child.getAttribute("y")),int(child.getAttribute("width")),int(child.getAttribute("height")),child.tagName, child.getAttribute("sprite"), foreground=child.getAttribute("foreground")))
            levels.append(maps)
        return levels
    def setSprites(platform, player):
        SystemComponent.spritesB = pygame.sprite.Group()
        SystemComponent.spritesF = pygame.sprite.Group()
        for p in platforms:
            if not p.foreground=="True":
                SystemComponent.spritesB.add(p)
            else:
                SystemComponent.spritesF.add(p)
        SystemComponent.spritesB.add(player)

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
SystemComponent.setSprites(platforms,player)
moveables = [player]
main_camera = Camera(player, platforms, window.get_height()*0.75)

 # game loop
main_camera.centre_camera(vector2d(window.get_width(), window.get_height()))

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        elif event.type == VIDEORESIZE:
            main_camera.centre_camera(vector2d(window.get_width(), window.get_height()))
            pass
    window.fill((0,0,0))
    for entity in moveables:
        if entity.spriteChange:
            SystemComponent.setSprites(platforms,player)
        entity.update(platforms)

    main_camera.update(window)
    if len(platforms)<len(SystemComponent.spritesB) + len(SystemComponent.spritesF)-1:
        SystemComponent.setSprites(platforms,player)
    for entity in SystemComponent.spritesB:
        #,special_flags= BLEND_ADD'
        window.blit(entity.area, entity.shape)
    for entity in SystemComponent.spritesF:
        #,special_flags= BLEND_ADD'
        window.blit(entity.area, entity.shape)
    pygame.display.update()
    current_fps.tick(MAX_FPS)