import pygame
from os import *
from components.GameConstants import *
from components.PhysicsComponent import *
from components.InputComponent import *

class Entity(pygame.sprite.Sprite): # dziedziczenie po sprite
    def __new__(cls, _window, _x,_y, width=10, height=10, type=None, sprite=None, foreground=False, background=None, triggerType=None, cutsceneInfo=None, id=None):
        if not isinstance(_x, float) and not isinstance(_x, int):
            raise TypeError("Pierwszy argument inicjalizacji obiektu klasy Entity (_x) musi być typu numerycznego float lub int!")
        if not isinstance(_y, float) and not isinstance(_y, int):
            raise TypeError("Pierwszy argument inicjalizacji obiektu klasy Entity (_y) musi być typu numerycznego float lub int!")
        return super(Entity, cls).__new__(cls)
     # test wiarygodnosci argumentow
    def __init__(self,window,_x,_y, _width, _height, _control,_moveable, type=None,sprite=None, foreground=False, triggerType=None, cutsceneInfo=None):
        super().__init__()

        self.window = window

        # "stałe" dla klasy
        self.HEIGHT = _height
        self.WIDTH = _width
        # moveable ze dziala na niego kolizja
        self.MOVEABLE = _moveable
        # control ze mozna sie nim poruszac
        self.CONTROL = _control

        self.spriteChange = False
        self.foreground = foreground
        self.animationDelayConst = 15
        self.animationDelay = 0
        self.animationFrame = -1
        self.animationFrameList = []
        self.flip = -1
         # definiowanie elementow obiektu
        self.area = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA, 32)
        if sprite!=None and sprite!="None":
            self.area = pygame.image.load(path.join(SPRITES_DIR,sprite)).convert_alpha()
            self.area = pygame.transform.scale(self.area,(self.WIDTH,self.HEIGHT))
        self.shape = self.area.get_rect(center = (_x,_y))
         # fizyka
        self.pos = vector2d((_x,_y))
        self.cameraPos = vector2d((_x,_y))
        self.shape.topleft = self.pos

         # oblsuga kolizji i ruchu
        if self.MOVEABLE:
            self.last_movement = vector2d(0,0)
            self.physics_component = PhysicsComponent(self)

            # gravity
            self.physics_component.accel = vector2d(0,2)
            self.physics_component.speed = vector2d(0,0)
            self.physics_component.friction = 0.10

            # input handling
            if self.CONTROL:
                self.input_component = InputComponent()

    def move_to_pos(self, in_pos):
        self.pos = in_pos
    def changeCameraOffset(self, camera_offset):
        self.cameraPos = camera_offset
        self.shape.topleft = self.pos + self.cameraPos

    def get_height(self):
        return self.area.get_height()
    def get_width(self):
        return self.area.get_width()

    def animate(self):
        if self.animationFrame>-1:
            if self.animationDelay >= self.animationDelayConst:
                self.changeSprite(self.animationFrameList[self.animationFrame])
                self.animationDelay = -1
            self.animationDelay+=1

    def changeSprite(self, spriteDir):
        self.spriteChange = True
        if spriteDir!=None:
            self.area = pygame.image.load(path.join(SPRITES_DIR,spriteDir)).convert_alpha()
            self.area = pygame.transform.scale(self.area,(self.WIDTH,self.HEIGHT))
        else:
            self.area = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA, 32)