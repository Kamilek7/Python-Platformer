
from components.GameConstants import *
from components.BackgroundManager import *

class PhysicsComponent:
    def __init__(self, entity) -> None:
        self.def_speed = 1
        self.speed = vector2d(0,0)
        self.accel = vector2d(0,2)
        self.friction = vector2d(-0.1,0)
        self.entity = entity
        self.is_on_ground = False

    def check_colision(self, moved_by_vec, other_entities = [], others=[]):
        def verticalAdjustment(col_entity, pos_to_check, temp_moved_vec):
            key = pygame.key.get_pressed()
            if self.entity.type!="enemy" and (col_entity.type=="plat" or col_entity.type=="ladder" or col_entity.type=="enemy"):
                if self.speed.y>0 and pos_to_check.y<=col_entity.pos.y-col_entity.get_height()+10 and not (key[K_DOWN] or key[K_s] or key[K_SEMICOLON]) and col_entity.type!="ladder":
                    self.speed.y = 0
                    self.is_on_ground = True
                    upFlag = True
                    if col_entity.type=="enemy" and col_entity.enemType!="matkaKacpra":
                        if col_entity.checkCoolDown():
                            self.entity.knockBack(col_entity.get_height())
                        else:
                            upFlag = False
                        col_entity.takeDamage(destroyer = self.entity)
                    if upFlag:
                        self.entity.move_to_pos(vector2d(self.entity.pos.x, col_entity.pos.y - self.entity.get_height()))
                elif col_entity.type=="ladder":
                    if key[K_UP] or key[K_w] or key[K_SPACE] or key[K_p]:
                        self.speed.y = -7
                    elif key[K_DOWN] or key[K_s] or key[K_SEMICOLON]:
                        self.speed.y = 0
                    else:
                        self.speed.y = -3
                elif col_entity.type=="enemy" and col_entity.enemType!="matkaKacpra":
                    self.entity.takeDamage()
                    self.entity.knockBack(col_entity.get_height(), direction = self.entity.pos - col_entity.pos)
            else:
                if not (self.entity.type=="enemy" and col_entity.type=="ladder"):
                    self.speed.y = 0
                    if temp_moved_vec.y > 0:
                        self.is_on_ground = True
                        self.entity.move_to_pos(vector2d(self.entity.pos.x, col_entity.pos.y - self.entity.get_height()))
                    else:
                        self.entity.move_to_pos(vector2d(self.entity.pos.x, col_entity.pos.y + col_entity.get_height()))
        def horizontalAdjustment(col_entity, temp_moved_vec):
            if col_entity.type!="plat" and col_entity.type!="enemy" and col_entity.type!="ladder":
                self.speed.x = 0
                if temp_moved_vec.x > 0:
                    self.entity.move_to_pos(vector2d(col_entity.pos.x - self.entity.get_width(), self.entity.pos.y))
                else:
                    self.entity.move_to_pos(vector2d(col_entity.pos.x + col_entity.get_width(), self.entity.pos.y))
        def doorCheck(col_entity):
            check = False
            if col_entity.type=="door":
                check = self.entity.useKey(col_entity.keyColor)
                if check:
                    col_entity.type = "decor"
                    col_entity.WIDTH = 80
                    col_entity.pos.x+=2
                    col_entity.changeSprite("drzwi_" + col_entity.keyColor + ".png")
            return check
        def checksForPlayer(col_entity):
            check = True
            removeFlag = False
            if col_entity.type=="key":
                self.entity.getKey(col_entity.keyColor)
                other_entities.remove(col_entity)
                removeFlag=True
            elif col_entity.type=="background":
                BackgroundManager.changeBackground(col_entity)
                self.entity.currentBG = col_entity.background
            elif col_entity.type=="trigger":
                col_entity.manageTrigger(others, self.entity)
            else:
                check = doorCheck(col_entity)
            return [removeFlag,check]
        def mainCollisionHandler(col_entity):
            removeFlag = False
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
            upperBound = pos_to_check.y > col_entity.pos.y - self.entity.get_height()
            lowerBound = pos_to_check.y < col_entity.pos.y + col_entity.get_height()
            rightBound = pos_to_check.x + self.entity.get_width()> col_entity.pos.x
            leftBound = pos_to_check.x < col_entity.pos.x + col_entity.get_width()
            if upperBound and lowerBound and rightBound and leftBound:
                check = self.entity.type=="player"
                if check:
                    temp = checksForPlayer(col_entity)
                    removeFlag = temp[0]
                    check = temp[1]
                if not check:
                    if col_entity.type=="key" or col_entity.type=="trigger" or col_entity=="player":
                        pass
                    elif col_entity.type=="background":
                        self.entity.currentBG = col_entity.background
                    elif i == 0:
                        verticalAdjustment(col_entity, pos_to_check, temp_moved_vec)
                    elif i == 1:
                        horizontalAdjustment(col_entity, temp_moved_vec)
            return removeFlag
        self.is_on_ground = False
        for col_entity in other_entities:
            decor = col_entity.type=="decor"
            spawn = col_entity.type=="spawn" or col_entity.type=="spawnE"
            selfColliding = (self.entity.type=="enemy" and col_entity.type=="enemy")

            if decor or spawn or selfColliding:
                pass
            else:
                removeFlag = False
                for i in range(2):
                    if not removeFlag:
                        removeFlag = mainCollisionHandler(col_entity)
                            
    def move(self, move_vec):
        self.speed.x += self.def_speed*move_vec.x
        self.speed.y += self.def_speed*move_vec.y

    def update_pos(self, in_other_entities = None, others=[]):
        prev_pos = vector2d(self.entity.pos.x, self.entity.pos.y)
        # tarcie powoduje hamowanie bo acc bedzie ujemne caly czas (dodatnie tylko w chwili nacisniecia klawisza)
        self.speed.x -= self.friction*self.speed.x
        
         # reszta to fizyka lore
        self.speed += self.accel
        self.entity.pos += self.speed + self.accel/2
        moved_by_vec = self.entity.pos - prev_pos

        # (self.entity.pos)
        self.check_colision(moved_by_vec, in_other_entities, others=others)
        self.entity.shape.topleft = self.entity.pos + self.entity.cameraPos