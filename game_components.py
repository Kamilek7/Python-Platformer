
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
        pass
    def update_pos(self, other_entities = None):
        key = pygame.key.get_pressed()
        if key[K_LEFT] or key[K_a]:
            self.accel.x = -self.def_speed
        if key[K_RIGHT] or key[K_d]:
             self.accel.x = self.def_speed  
        # tarcie powoduje hamowanie bo acc bedzie ujemne caly czas (dodatnie tylko w chwili nacisniecia klawisza)
        self.accel -= self.friction*self.speed
         # reszta to fizyka lore
        self.speed += self.accel
        self.entity.pos += self.speed + self.accel/2
        self.entity.shape.midbottom = self.entity.pos

class InputComponent:
    def __init__(self) -> None:
        self.move_direction = vector2d(0,0)
    def get_player_movement_vec(self) -> vector2d:
        key = pygame.key.get_pressed()
        if key[K_LEFT] or key[K_a]:
            self.accel.x = -self.def_speed
        if key[K_RIGHT] or key[K_d]:
             self.accel.x = self.def_speed  
        # tarcie powoduje hamowanie bo acc bedzie ujemne caly czas (dodatnie tylko w chwili nacisniecia klawisza)
        self.accel -= self.friction*self.speed
         # reszta to fizyka lore
        self.speed += self.accel
        self.entity.pos += self.speed + self.accel/2
        self.entity.shape.midbottom = self.pos
        