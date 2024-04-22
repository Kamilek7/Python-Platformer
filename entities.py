import pygame
from pygame.locals import *
from game_components import PhysicsComponent, InputComponent
vector2d = pygame.math.Vector2
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
        #komponent odpowiedzialny za fizykę
        self.physics_component = PhysicsComponent(self)
        self.input_component = InputComponent()
        self.physics_component.friction = _friction
        # "stałe" dla klasy
        self.HEIGHT = _height
        self.WIDTH = _width
        self.COLOR = _color   # potem sie zrobi slownik z kolorami, wszystko jest w RGB
        # self.input_component = _speed
        
        self.MOVEABLE = _moveable
        self.CONTROL = _control
         # definiowanie elementow obiektu
        self.area = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.area.fill(self.COLOR)
        self.shape = self.area.get_rect(center = (_x,600-_y))
         # fizyka
        self.pos = vector2d((_x,600 - _y))
        self.physics_component.speed = vector2d(0,0)

        #dodać grawitacje później !!!!!!
        self.physics_component.accel = vector2d(0,0)

    def move(self):
        if self.MOVEABLE:
            # wstepnie ustawia acc na 0
            move_vec = self.input_component.get_movement_vec()
            self.physics_component.accel = vector2d(0,0)
                
            self.physics_component.move(move_vec)
            self.physics_component.update_pos()
