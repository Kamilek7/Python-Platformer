
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

    def check_colision(self, other_entities = []):
        #temp. colision
        for col_entity in other_entities:
            if self.entity.pos.y > col_entity.pos.y - col_entity.get_height():
                self.entity.pos.y = col_entity.pos.y - col_entity.get_height()
                print(self.entity.pos.y)
                #self.entity.pos.y > self.entity.window.get_height()
                self.speed.y = 0
                self.is_coliding = True
            else:
                self.is_coliding = False
        
    def move(self, move_vec, other_entities = None):
        self.accel.x += self.def_speed*move_vec.x
        self.speed.y += self.def_speed*move_vec.y

    def update_pos(self, in_other_entities = None):
        # tarcie powoduje hamowanie bo acc bedzie ujemne caly czas (dodatnie tylko w chwili nacisniecia klawisza)
        self.speed -= self.friction*self.speed
         # reszta to fizyka lore
        self.speed += self.accel
        self.entity.pos += self.speed + self.accel/2
        
        print(self.entity.pos)
        self.check_colision(in_other_entities)
        self.entity.shape.topleft = self.entity.pos

class InputComponent:
    def __init__(self) -> None:
        self.move_vec = vector2d(0,0)
    def get_movement_vec(self, is_colliding = False):
        move_vec = vector2d(0,0)
        key = pygame.key.get_pressed()
        if key[K_LEFT] or key[K_a] or key[K_l]:
            move_vec.x = -1
        if key[K_RIGHT] or key[K_d] or key[K_QUOTE]:
             move_vec.x = 1
        if (key[K_UP] or key[K_w] or key[K_SPACE] or key[K_p]) and is_colliding:
            move_vec.y = -30
        if key[K_DOWN] or key[K_s]:
            move_vec.y = 1
        return move_vec
        