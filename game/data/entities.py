# Modul zawierajacy klasy w grze reprezentujace nieabstrakcyjne elementy

import pygame
from pygame.locals import *
from os import *
from game_components import (PhysicsComponent, InputComponent)
vector2d = pygame.math.Vector2


APP_HEIGHT = 600
APP_WIDTH = 800

 # klasy w grze
class Entity(pygame.sprite.Sprite): # dziedziczenie po sprite
     # test wiarygodnosci argumentow
    def __new__(cls, _window, _x,_y, width=10, height=10, type=None, sprite=None, foreground=False, background=None):
        #do checks for window, height, width later
        if not isinstance(_x, float) and not isinstance(_x, int):
            raise TypeError("Pierwszy argument inicjalizacji obiektu klasy Entity (_x) musi być typu numerycznego float lub int!")
        if not isinstance(_y, float) and not isinstance(_y, int):
            raise TypeError("Pierwszy argument inicjalizacji obiektu klasy Entity (_y) musi być typu numerycznego float lub int!")
        return super(Entity, cls).__new__(cls)
    def __init__(self,window,_x,_y, _width, _height, _control,_moveable, type=None,sprite=None, foreground=False):
        super().__init__()

        self.window = window

        # "stałe" dla klasy
        self.HEIGHT = _height
        self.WIDTH = _width
        # self.input_component = _speed

        # moveable ze dziala na niego kolizja
        self.MOVEABLE = _moveable

        # control ze mozna sie nim poruszac
        self.CONTROL = _control
        self.spriteChange = False
        self.foreground = foreground

         # definiowanie elementow obiektu
        self.area = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA, 32)
        if sprite!=None and sprite!="None":
            self.area = pygame.image.load(path.join(path.dirname(path.abspath(__file__)), 'sprites',sprite)).convert_alpha()
            self.area = pygame.transform.scale(self.area,(self.WIDTH,self.HEIGHT))
        self.shape = self.area.get_rect(center = (_x,_y))
         # fizyka
        self.pos = vector2d((_x,_y))
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
        self.shape.topleft = self.pos
    def move_by(self, movement_vec):
        self.pos += movement_vec
        self.shape.topleft = self.pos


    def get_height(self):
        return self.area.get_height()
    def get_width(self):
        return self.area.get_width()

    def update(self, in_other_entities = []):
        if self.MOVEABLE:
            pass
            # wstepnie ustawia acc na 0
    def changeSprite(self, spriteDir):
        self.spriteChange = True
        self.area = pygame.image.load(path.join(path.dirname(path.abspath(__file__)), 'sprites',spriteDir)).convert_alpha()
        self.area = pygame.transform.scale(self.area,(self.WIDTH,self.HEIGHT))
        self.shape = self.area.get_rect(center = (self.pos.x,self.pos.y))




class Player(Entity): # dziedziczenie po entity
    def __init__(self,window,_x,_y, in_width = 38, in_height = 75):
         # X, Y, WYSOKOSC, SZEROKOSC, KOLOR, PED PRZY RUCHU, TARCIE, RUCHOME, MOZNA STEROWAC
                 #grawitacja
        super().__init__(window,_x, _y, in_width, in_height, True, True, type="player",sprite="brick.png")

         # inventory
        self.keys = {"red":0,"purple":0,"green":0}
    def getKey(self,type):
        self.keys[type]+=1

    def useKey(self, type):
        if self.keys[type]>0:
            self.keys[type]-=1
            return True
        else:
            return False
        
        

    def update(self, in_other_entities = []):
            prev_pos = vector2d(self.pos.x, self.pos.y)
            #get input from player
            move_input = self.input_component.get_movement_vec(self.physics_component.is_on_ground)
            #debug
            if move_input != vector2d(0,0):
                pass
                # debug print("pos: ",self.pos,"accel: ", self.physics_component.accel, "speed: ", self.physics_component.speed)
            
            
            self.physics_component.move(move_input)
            self.physics_component.update_pos(in_other_entities)
            self.last_movement = self.pos - prev_pos

class Grounds(Entity):
    def __init__(self,window, _x, _y, in_width = APP_WIDTH, in_height = 120, _type = "block", sprite=None, foreground=False, background=None):
        super().__init__(window, _x, _y, in_width, in_height, False, False, sprite=sprite, foreground=foreground)
        self.type = _type
        if self.type=="key" or self.type=="door":
            if "red" in sprite:
                self.keyColor = "red"
            elif "purple" in sprite:
                self.keyColor = "purple"
            elif "green" in sprite:
                self.keyColor = "green"
        elif self.type == "background":
            self.background = background
