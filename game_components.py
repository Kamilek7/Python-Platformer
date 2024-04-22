import pygame
from entities import Entity
vector2d = pygame.math.Vector2
class PhysicsComponent:
    def __init__(self):
        self.speed = vector2d(0,0)
        self.accel = vector2d(0,-5)
        self.friction = vector2d(0,0)
        pass
    def check_colision(self):
        pass
    def move(self, entity, move_vec):
        pass
        