
 # wszystkie definicje i wstepne wartosci
 # meow

from entities import *
from os import *
from camera import Camera
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
running = True

 # elementy gry

player = Player(window,APP_WIDTH/5,60)
p1 = Grounds(window,APP_WIDTH/6 ,APP_HEIGHT-30)
p2 = Grounds(window,APP_WIDTH/2 ,APP_HEIGHT-120,120,80)
p3 = Grounds(window,APP_WIDTH/1.5 ,APP_HEIGHT-220,120,80)
sprites = pygame.sprite.Group()
sprites.add(player)
sprites.add(p1)
sprites.add(p2)
sprites.add(p3)
moveables = [player]

platforms = [p1,p2,p3]

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
        entity.update(platforms)
        
    main_camera.update(window)
    for entity in sprites:
        #,special_flags= BLEND_ADD'
        window.blit(entity.area, entity.shape)
    pygame.display.update()
    current_fps.tick(MAX_FPS)