
 # wszystkie definicje i wstepne wartosci
 # meow

from entities import *
from os import *
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
pygame.display.set_caption("Test")
running = True

 # elementy gry

player = Player(window,APP_WIDTH/5,60)
p1 = Grounds(window,APP_WIDTH/2,APP_HEIGHT-30)
sprites = pygame.sprite.Group()
sprites.add(player)
sprites.add(p1)
moveables = [player]

 # game loop

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        elif event.type == VIDEORESIZE:
            pass
    window.fill((0,0,0))
    for entity in moveables:
        entity.update([p1])
        
    for entity in sprites:
        #,special_flags= BLEND_ADD'
        window.blit(entity.area, entity.shape)
    pygame.display.update()
    current_fps.tick(MAX_FPS)