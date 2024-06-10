import pygame
from pygame.locals import *

vector2d = pygame.math.Vector2

class InputComponent:
    def __init__(self) -> None:
        self.move_vec = vector2d(0,0)
    def get_movement_vec(self, is_colliding = False):
        move_vec = vector2d(0,0)
        speed = 1.2
        key = pygame.key.get_pressed()
        if key[K_LEFT] or key[K_a] or key[K_l]:
            move_vec.x = -1*speed
        if key[K_RIGHT] or key[K_d] or key[K_QUOTE]:
             move_vec.x = 1*speed
        if (key[K_UP] or key[K_w] or key[K_SPACE] or key[K_p]) and is_colliding:
            move_vec.y = -speed*25
        return move_vec