
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
window = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
pygame.display.set_caption("Test")
running = True

 # elementy gry

 # !!! początek ukladu wspolrzednych ustalamy w lewym dolnym rogu, a nie lewym gornym jak np w html !!!
player = Player(APP_WIDTH/5,60)
p1 = Grounds(APP_WIDTH/2,30)
sprites = pygame.sprite.Group()
sprites.add(player)
sprites.add(p1)
moveables = [player]

 # game loop

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
    window.fill((0,0,0))
    for entity in moveables:
        entity.update()
        
    for entity in sprites:
        window.blit(entity.area, entity.shape)
    pygame.display.update()
    current_fps.tick(MAX_FPS)