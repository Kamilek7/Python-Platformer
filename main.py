
 # wszystkie definicje i wstepne wartosci

import pygame
from pygame.locals import *
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

 # klasy w grze

 # tutaj od razu mozna dac klase entity zeby nie powtarzac kodu
class Player(pygame.sprite.Sprite): # dziedziczenie po sprite
     # test wiarygodnosci argumentow
    def __new__(cls, _x,_y):
        if not isinstance(_x, float) and not isinstance(_x, int):
            raise TypeError("Pierwszy argument inicjalizacji obiektu klasy Player (_x) musi być typu numerycznego float lub int!")
        if not isinstance(_y, float) and not isinstance(_y, int):
            raise TypeError("Pierwszy argument inicjalizacji obiektu klasy Player (_y) musi być typu numerycznego float lub int!")
        return super(Player, cls).__new__(cls) 
    def __init__(self,_x,_y):
        super().__init__()
         # "stałe" dla klasy
        self.HEIGHT = 60
        self.WIDTH = 30
        self.COLOR = (210,60,60)   # potem sie zrobi slownik z kolorami, wszystko jest w RGB
        self.SPEED = 1
        self.FRICTION = 0.16
         # definiowanie elementow obiektu
        self.area = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.area.fill(self.COLOR)
        self.shape = self.area.get_rect(center = (_x,APP_HEIGHT- _y))
         # fizyka
        self.pos = vector2d((_x,APP_HEIGHT- _y))
        self.spd = vector2d(0,0)
        self.acc = vector2d(0,0)
    def move(self):
        self.acc = vector2d(0,0)
        key = pygame.key.get_pressed()
        if key[K_LEFT] or key[K_a]:
            self.acc.x = -self.SPEED
        if key[K_RIGHT] or key[K_d]:
            self.acc.x = self.SPEED
        self.acc -= self.FRICTION*self.spd
        self.spd += self.acc
        self.pos += self.spd + self.acc/2
        self.shape.midbottom = self.pos

class Grounds(pygame.sprite.Sprite):
     # test wiarygodnosci argumentow
    def __new__(cls, _x,_y):
        if not isinstance(_x, float) and not isinstance(_x, int):
            raise TypeError("Pierwszy argument inicjalizacji obiektu klasy Grounds (_x) musi być typu numerycznego float lub int!")
        if not isinstance(_y, float) and not isinstance(_y, int):
            raise TypeError("Pierwszy argument inicjalizacji obiektu klasy Grounds (_y) musi być typu numerycznego float lub int!")
        return super(Grounds, cls).__new__(cls) 
    def __init__(self,_x,_y):
        super().__init__()
         # "stałe" dla klasy
        self.HEIGHT = 60
        self.WIDTH = APP_WIDTH
        self.COLOR = (60,60,210)   # potem sie zrobi slownik z kolorami, wszystko jest w RGB
         # definiowanie elementow obiektu
        self.area = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.area.fill(self.COLOR)
        self.shape = self.area.get_rect(center = (_x,APP_HEIGHT- _y))
         # fizyka, na wypadek gdyby to byla ruchoma platforma
        self.pos = vector2d((_x,APP_HEIGHT- _y))
        self.speed = vector2d(0,0)
        self.acceler = vector2d(0,0)

 # elementy gry

 # !!! początek ukladu wspolrzednych ustalamy w lewym dolnym rogu, a nie lewym gornym jak np w html !!!
player = Player(APP_WIDTH/5,60)
p1 = Grounds(APP_WIDTH/2,30)
sprites = pygame.sprite.Group()
sprites.add(player)
sprites.add(p1)

 # game loop

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
    window.fill((0,0,0))
    player.move()
    for entity in sprites:
        window.blit(entity.area, entity.shape)
    pygame.display.update()
    current_fps.tick(MAX_FPS)