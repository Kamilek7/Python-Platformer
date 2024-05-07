
from entities import *
from os import *
from xml.dom import minidom

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
        self.is_on_ground = False
    
    def check_colision(self, moved_by_vec, other_entities = []):
        #collision detection and handling
        #handling is temp need to add more checks later
        self.is_on_ground = False
        for col_entity in other_entities:
            if col_entity.type=="decor" or col_entity.type=="spawn" or col_entity.type=="spawnE":
                pass
            else:
                for i in range(2):
                    temp_moved_vec = vector2d(moved_by_vec.x, moved_by_vec.y)
                    pos_to_check = vector2d(self.entity.pos.x,self.entity.pos.y)
                    if i == 0:
                        #checks only y axis
                        pos_to_check.x -= temp_moved_vec.x
                        temp_moved_vec.x = 0
                    elif i == 1:
                        #checks only x axis
                        pos_to_check.y -= temp_moved_vec.y
                        temp_moved_vec.y = 0
                    if pos_to_check.y > col_entity.pos.y - self.entity.get_height() and pos_to_check.y < col_entity.pos.y + col_entity.get_height():
                        if pos_to_check.x + self.entity.get_width()> col_entity.pos.x and pos_to_check.x < col_entity.pos.x + col_entity.get_width():
                            if col_entity.type=="key":
                                self.entity.getKey(col_entity.keyColor)
                                other_entities.remove(col_entity)
                                break
                            else:
                                check = False
                                if col_entity.type=="door":
                                    check = self.entity.useKey(col_entity.keyColor)
                                    if check:
                                        # tutaj mozna potem dac zmiane sprite'u
                                        col_entity.type = "decor"
                                        col_entity.WIDTH = 80
                                        col_entity.pos.x+=2
                                        col_entity.changeSprite("drzwi_" + col_entity.keyColor + ".png")
                                if not check:
                                    if i == 0:
                                        if col_entity.type=="plat" or col_entity.type=="ladder":
                                            if self.speed.y>0:
                                                self.speed.y = 0
                                                self.is_on_ground = True
                                                self.entity.move_to_pos(vector2d(self.entity.pos.x, col_entity.pos.y - self.entity.get_height()))
                                            elif col_entity.type=="ladder":
                                                self.speed.y = -7
                                        else:
                                            self.speed.y = 0
                                            if temp_moved_vec.y > 0:
                                                self.is_on_ground = True
                                                self.entity.move_to_pos(vector2d(self.entity.pos.x, col_entity.pos.y - self.entity.get_height()))
                                            else:
                                                self.entity.move_to_pos(vector2d(self.entity.pos.x, col_entity.pos.y + col_entity.get_height()))
                                    elif i == 1:
                                        if col_entity.type!="plat" and col_entity.type!="ladder":
                                            self.speed.x = 0
                                            if temp_moved_vec.x > 0:
                                                self.entity.move_to_pos(vector2d(col_entity.pos.x - self.entity.get_width(), self.entity.pos.y))
                                            else:
                                                self.entity.move_to_pos(vector2d(col_entity.pos.x + col_entity.get_width(), self.entity.pos.y))
                            

        
    def move(self, move_vec, other_entities = None):
        self.speed.x += self.def_speed*move_vec.x
        self.speed.y += self.def_speed*move_vec.y

    def update_pos(self, in_other_entities = None):
        prev_pos = vector2d(self.entity.pos.x, self.entity.pos.y)
        # tarcie powoduje hamowanie bo acc bedzie ujemne caly czas (dodatnie tylko w chwili nacisniecia klawisza)
        self.speed.x -= self.friction*self.speed.x
         # reszta to fizyka lore
        self.speed += self.accel
        self.entity.pos += self.speed + self.accel/2
        moved_by_vec = self.entity.pos - prev_pos
        
        #
        # (self.entity.pos)
        self.check_colision(moved_by_vec, in_other_entities)
        self.entity.shape.topleft = self.entity.pos

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
        if key[K_DOWN] or key[K_s]:
            move_vec.y = 1
        return move_vec