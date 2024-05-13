
 # wszystkie definicje i wstepne wartosci
 # meow

from os import *
from xml.dom import minidom
from game_components import *

# z jakiegos powodu Grounds nie dziala w game_components ale dziala tutaj?

    
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

package = SystemComponent.loadMaps(window)
levels = package["levels"]
playerSpawn = package["playerSpawn"]
platforms = levels[0]
player = Player(window,playerSpawn[0],playerSpawn[1])
TextureComponent.setSprites(platforms,player)
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
            TextureComponent.scaleBackground(window)
    TextureComponent.manageBackground(window)
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