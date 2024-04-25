import pygame
from pygame.locals import *
from game_components import PhysicsComponent, InputComponent
vector2d = pygame.math.Vector2


APP_HEIGHT = 600
APP_WIDTH = 800

 # klasy w grze
class Entity(pygame.sprite.Sprite): # dziedziczenie po sprite
     # test wiarygodnosci argumentow
    def __new__(cls, _window, _x,_y):
        if not isinstance(_x, float) and not isinstance(_x, int):
            raise TypeError("Pierwszy argument inicjalizacji obiektu klasy Entity (_x) musi być typu numerycznego float lub int!")
        if not isinstance(_y, float) and not isinstance(_y, int):
            raise TypeError("Pierwszy argument inicjalizacji obiektu klasy Entity (_y) musi być typu numerycznego float lub int!")
        return super(Entity, cls).__new__(cls)
    def __init__(self,window,_x,_y, _height, _width, _color, _control,_moveable):
        super().__init__()
        #komponent odpowiedzialny za fizykę
        self.window = window
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
        self.shape = self.area.get_rect(center = (_x,_y))
         # fizyka
        self.pos = vector2d((_x,_y))
        self.shape.topleft = self.pos

    def move_to_pos(self, in_pos):
        self.pos = in_pos
        self.shape.topleft = self.pos


    def get_height(self):
        return self.area.get_height()

    def update(self, in_other_entities = []):
        if self.MOVEABLE:
            pass
            # wstepnie ustawia acc na 0




class Player(Entity): # dziedziczenie po entity
    def __init__(self,window,_x,_y):
         # X, Y, WYSOKOSC, SZEROKOSC, KOLOR, PED PRZY RUCHU, TARCIE, RUCHOME, MOZNA STEROWAC
                 #grawitacja
        super().__init__(window,_x, _y, 60, 30, (210,60,60), True, True)

        self.physics_component = PhysicsComponent(self)
        #gravity
        self.physics_component.accel = vector2d(0,2)
        #self.physics_component.accel.y = 0

        self.physics_component.speed = vector2d(0,0)
        self.physics_component.friction = 0.08

        #input handling
        self.input_component = InputComponent()
        

    def update(self, in_other_entities = []):
            #get input from player
            move_vec = self.input_component.get_movement_vec(self.physics_component.is_coliding)
            #debug
            if move_vec != vector2d(0,0):
                pass
                # debug print("pos: ",self.pos,"accel: ", self.physics_component.accel, "speed: ", self.physics_component.speed)
            
            
            self.physics_component.move(move_vec)
            self.physics_component.update_pos(in_other_entities)

class Grounds(Entity):
    def __init__(self,window,_x,_y):
         # X, Y, WYSOKOSC, SZEROKOSC, KOLOR, PED PRZY RUCHU, TARCIE, RUCHOME, MOZNA STEROWAC
        super().__init__(window, _x, _y, 60, APP_WIDTH, (60,60,210), False, False)