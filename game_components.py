
from entities import *

APP_HEIGHT = 600
APP_WIDTH = 800
vector2d = pygame.math.Vector2
class PhysicsComponent:
    def __init__(self, entity) -> None:
        self.def_speed = 1
        self.speed = vector2d(0,0)
        self.accel = vector2d(0,2)
        self.friction = vector2d(-0.1,0)
        self.entity = entity
        self.is_coliding = False

    def check_colision(self, other_entities = None):
        #temp. colision remove later
        if self.entity.pos.y > APP_HEIGHT - self.entity.HEIGHT:
            self.entity.pos.y = APP_HEIGHT - self.entity.HEIGHT
            self.speed.y = 0
            self.is_coliding = True
        else:
            self.is_coliding = False
        
    def move(self, move_vec, other_entities = None):
        self.accel.x += self.def_speed*move_vec.x
        self.speed.y += self.def_speed*move_vec.y

    def update_pos(self, other_entities = None):
        # tarcie powoduje hamowanie bo acc bedzie ujemne caly czas (dodatnie tylko w chwili nacisniecia klawisza)
        self.speed -= self.friction*self.speed
         # reszta to fizyka lore
        self.speed += self.accel
        self.entity.pos += self.speed + self.accel/2
        self.entity.shape.midbottom = self.entity.pos
        self.check_colision()

class InputComponent:
    def __init__(self) -> None:
        self.move_vec = vector2d(0,0)
    def get_movement_vec(self, is_colliding = False):
        move_vec = vector2d(0,0)
        key = pygame.key.get_pressed()
        if key[K_LEFT] or key[K_a]:
            move_vec.x = -1
        if key[K_RIGHT] or key[K_d]:
             move_vec.x = 1
        if key[K_UP] or key[K_w] or key[K_SPACE] and is_colliding:
            move_vec.y = -20
        if key[K_DOWN] or key[K_s]:
            move_vec.y = 1
        return move_vec
        