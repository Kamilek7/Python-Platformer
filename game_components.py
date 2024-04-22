
from entities import *

vector2d = pygame.math.Vector2
class PhysicsComponent:
    def __init__(self, entity) -> None:
        self.def_speed = 1
        self.speed = vector2d(0,0)
        self.accel = vector2d(0,-0.1)
        self.friction = vector2d(-0.1,0)
        self.entity = entity
        pass
    def check_colision(self, other_entities):
        pass
    def move(self, move_vec, other_entities = None):
        self.accel.x = self.def_speed*move_vec.x

    def update_pos(self, other_entities = None):
        # tarcie powoduje hamowanie bo acc bedzie ujemne caly czas (dodatnie tylko w chwili nacisniecia klawisza)
        self.accel -= self.friction*self.speed
         # reszta to fizyka lore
        self.speed += self.accel
        self.entity.pos += self.speed + self.accel/2
        self.entity.shape.midbottom = self.entity.pos

class InputComponent:
    def __init__(self) -> None:
        self.move_direction = vector2d(0,0)
    def get_movement_vec(self):
        direction = vector2d(0,0)
        key = pygame.key.get_pressed()
        if key[K_LEFT] or key[K_a]:
            direction.x = -1
        if key[K_RIGHT] or key[K_d]:
             direction.x = 1
        if key[K_UP] or key[K_w]:
            direction.y = 1
        if key[K_DOWN] or key[K_s]:
            direction.y = -1
        return direction
        