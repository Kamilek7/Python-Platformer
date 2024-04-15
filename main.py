
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

class Entity(pygame.sprite.Sprite): # dziedziczenie po sprite
     # test wiarygodnosci argumentow
    def __new__(cls, _x,_y):
        if not isinstance(_x, float) and not isinstance(_x, int):
            raise TypeError("Pierwszy argument inicjalizacji obiektu klasy Entity (_x) musi być typu numerycznego float lub int!")
        if not isinstance(_y, float) and not isinstance(_y, int):
            raise TypeError("Pierwszy argument inicjalizacji obiektu klasy Entity (_y) musi być typu numerycznego float lub int!")
        return super(Entity, cls).__new__(cls)
    def __init__(self,_x,_y, _height, _width, _color, _speed, _friction, _control,_moveable):
        super().__init__()
         # "stałe" dla klasy
        self.HEIGHT = _height
        self.WIDTH = _width
        self.COLOR = _color   # potem sie zrobi slownik z kolorami, wszystko jest w RGB
        self.SPEED = _speed
        self.FRICTION = _friction
        self.MOVEABLE = _moveable
        self.CONTROL = _control
         # definiowanie elementow obiektu
        self.area = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.area.fill(self.COLOR)
        self.shape = self.area.get_rect(center = (_x,APP_HEIGHT- _y))
         # fizyka
        self.pos = vector2d((_x,APP_HEIGHT- _y))
        self.spd = vector2d(0,0)
        self.acc = vector2d(0,0)
    def move(self):
        if self.MOVEABLE:
             # wstepnie ustawia acc na 0
            self.acc = vector2d(0,0)
            if self.CONTROL:
                key = pygame.key.get_pressed()
                 # ustawia sie acc zaleznie od klawisza
                if key[K_LEFT] or key[K_a]:
                    self.acc.x = -self.SPEED
                if key[K_RIGHT] or key[K_d]:
                    self.acc.x = self.SPEED
             # tarcie powoduje hamowanie bo acc bedzie ujemne caly czas (dodatnie tylko w chwili nacisniecia klawisza)
            self.acc -= self.FRICTION*self.spd
             # reszta to fizyka lore
            self.spd += self.acc
            self.pos += self.spd + self.acc/2
            self.shape.midbottom = self.pos

class Player(Entity): # dziedziczenie po entity
    def __init__(self,_x,_y):
         # X, Y, WYSOKOSC, SZEROKOSC, KOLOR, PED PRZY RUCHU, TARCIE, INTERAKTYWNE, MOZNA STEROWAC
        super().__init__(_x, _y, 60, 30, (210,60,60), 1, 0.16, True, True)

class Grounds(Entity):
    def __init__(self,_x,_y):
         # X, Y, WYSOKOSC, SZEROKOSC, KOLOR, PED PRZY RUCHU, TARCIE, INTERAKTYWNE, MOZNA STEROWAC
        super().__init__(_x, _y, 60, APP_WIDTH, (60,60,210), 0, 0.16, False, False)

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
        entity.move()
    for entity in sprites:
        window.blit(entity.area, entity.shape)
    pygame.display.update()
    current_fps.tick(MAX_FPS)