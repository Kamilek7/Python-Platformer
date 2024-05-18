from os import *
from xml.dom import minidom
import pygame
from pygame.locals import *

CURRENT_DIR = path.dirname(path.abspath(__file__))
RESOURCES = path.join(path.dirname(CURRENT_DIR),"resources")
SPRITES_DIR = path.join(RESOURCES,"sprites")
BACKGROUNDS_DIR = path.join(RESOURCES,"backgrounds")
MAPS_DIR = path.join(RESOURCES,"maps")
AVATARS_DIR = path.join(RESOURCES,"avatars")
APP_HEIGHT = 600
APP_WIDTH = 800
vector2d = pygame.math.Vector2

# MAIN GAME COMPONENTS

class TextureComponent:
    spritesB = pygame.sprite.Group()
    spritesF = pygame.sprite.Group()
    messageBoxes = []
    background=None
    fadedBackground = None
    changeFlag = False
    fadeFlag = False
    alpha = 255
    backarea = None
    backareaTemp = None
    backshape = None
    messageFadeFlag = False
    messageVisibility = False
    messageLifespan = 0
    messageSizeFade = 0
    @staticmethod
    def scaleBackground(window):
        TextureComponent.backarea = pygame.transform.scale(TextureComponent.backarea,(window.get_width(),window.get_height()))
    def manageBackground(window):
        if TextureComponent.backarea==None:
            TextureComponent.backarea = pygame.Surface((window.get_width(),window.get_height()), pygame.SRCALPHA, 32)
            TextureComponent.backareaTemp = pygame.Surface((window.get_width(),window.get_height()), pygame.SRCALPHA, 32)
            TextureComponent.backshape = TextureComponent.backarea.get_rect(center = (0,0))
            backpos = vector2d((0,0))
            TextureComponent.backshape.topleft = backpos
        if TextureComponent.changeFlag:
            TextureComponent.changeFlag = False
            TextureComponent.alpha = 255
            if TextureComponent.fadedBackground != None:
                TextureComponent.fadeFlag = True
                TextureComponent.backareaTemp = pygame.image.load(path.join(BACKGROUNDS_DIR,TextureComponent.fadedBackground)).convert()
                TextureComponent.backareaTemp = pygame.transform.scale(TextureComponent.backarea,(window.get_width(),window.get_height()))
                TextureComponent.alpha=0
                TextureComponent.backareaTemp.set_alpha(255)
                window.blit(TextureComponent.backareaTemp, TextureComponent.backshape)
            TextureComponent.backarea = pygame.image.load(path.join(BACKGROUNDS_DIR,TextureComponent.background)).convert()
            TextureComponent.backarea = pygame.transform.scale(TextureComponent.backarea,(window.get_width(),window.get_height()))
            TextureComponent.backarea.set_alpha(TextureComponent.alpha)
        elif TextureComponent.fadeFlag:
            if TextureComponent.alpha<255:
                TextureComponent.alpha+=10
                TextureComponent.backarea.set_alpha(TextureComponent.alpha)
                window.blit(TextureComponent.backareaTemp, TextureComponent.backshape)
            else:
                TextureComponent.alpha=255
                TextureComponent.fadeFlag=False
                TextureComponent.backarea.set_alpha(TextureComponent.alpha)
        window.blit(TextureComponent.backarea, TextureComponent.backshape)

    def changeBackground(newBackground):
        if TextureComponent.background!=newBackground:
            TextureComponent.fadedBackground=TextureComponent.background
            TextureComponent.background = newBackground
            TextureComponent.changeFlag = True
    def setSprites(platforms, player):
        TextureComponent.spritesB = pygame.sprite.Group()
        TextureComponent.spritesF = pygame.sprite.Group()
        for p in platforms:
            if not p.foreground=="True":
                TextureComponent.spritesB.add(p)
            else:
                TextureComponent.spritesF.add(p)
        TextureComponent.spritesB.add(player)

    def appendMessages(package):
        TextureComponent.messageBoxes.append(package)

    def showMessage(_window,package):
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render(package["text"], True, (255, 255, 255))
        # ratio sie pozniej poprawi
        width = int(_window.get_width()/1.1)
        height = int(_window.get_height()/3.5)
        posX = int((_window.get_width()- width)/2)
        posY = int(_window.get_height() - _window.get_height()/3)
        avatarWidth = int(height/1.3)
        avatarHeight = avatarWidth
        border = (height - height/1.3)/2
        if TextureComponent.messageFadeFlag and not TextureComponent.messageVisibility:
            if TextureComponent.messageSizeFade>=100:
                TextureComponent.messageSizeFade=100
                TextureComponent.messageFadeFlag=False
                TextureComponent.messageVisibility=True
                TextureComponent.messageLifespan=100
            else:
                TextureComponent.messageSizeFade+=5
        elif not TextureComponent.messageFadeFlag and TextureComponent.messageVisibility:
            if TextureComponent.messageLifespan>0:
                TextureComponent.messageLifespan-=1
            else:
                TextureComponent.messageLifespan=0
                TextureComponent.messageFadeFlag=True
        elif TextureComponent.messageFadeFlag and TextureComponent.messageVisibility:
            if TextureComponent.messageSizeFade<=0:
                TextureComponent.messageSizeFade=0
                TextureComponent.messageFadeFlag=False
                TextureComponent.messageVisibility=False
                TextureComponent.messageBoxes.remove(package)
            else:
                TextureComponent.messageSizeFade-=5
        height = int(height*TextureComponent.messageSizeFade/100)
        avatarHeight = int(avatarHeight*TextureComponent.messageSizeFade/100)
        pygame.draw.rect(_window, (0,0,0), pygame.Rect(posX,  posY , width, height))
        if package["icon"]!="None":
            temparea = pygame.image.load(path.join(AVATARS_DIR,package["icon"])).convert_alpha()
            temparea = pygame.transform.scale(temparea,(avatarWidth,avatarHeight))
            _window.blit(temparea,(posX + border,posY + border))
            if TextureComponent.messageVisibility and not TextureComponent.messageFadeFlag:
                _window.blit(text_surface,(posX+avatarWidth + 2*border, posY + border))
        elif TextureComponent.messageVisibility and not TextureComponent.messageFadeFlag:
            _window.blit(text_surface,(posX+ border, posY + border))
    
class SystemComponent:
    @staticmethod
    def loadMaps(_window):
        playerSpawn = (APP_WIDTH/5,60)
        levels = []
        for files in listdir(MAPS_DIR):
            maps = []
            plik = minidom.parse(path.join(MAPS_DIR,files))
            mapa = plik.getElementsByTagName('map')[0]
            for child in mapa.childNodes:
                if child.tagName=="spawn":
                    playerSpawn = (int(child.getAttribute("x")),int(child.getAttribute("y")))
                elif child.tagName=="background":
                    maps.append(Grounds(_window,int(child.getAttribute("x")),int(child.getAttribute("y")),int(child.getAttribute("width")),int(child.getAttribute("height")),child.tagName,  background=child.getAttribute("background")))
                elif child.tagName=="trigger":
                    maps.append(Grounds(_window,int(child.getAttribute("x")),int(child.getAttribute("y")),int(child.getAttribute("width")),int(child.getAttribute("height")),child.tagName,  triggerType=child.getAttribute("actionType"), triggerInfo=child.getAttribute("actionSpecs")))
                else:
                    maps.append(Grounds(_window,int(child.getAttribute("x")),int(child.getAttribute("y")),int(child.getAttribute("width")),int(child.getAttribute("height")),child.tagName, child.getAttribute("sprite"), foreground=child.getAttribute("foreground")))
            levels.append(maps)
        package = {"levels": levels, "playerSpawn": playerSpawn}
        return package
    @staticmethod
    def showMessage(package):
        TextureComponent.appendMessages(package)
        TextureComponent.messageFadeFlag = True


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
                    upperBound = pos_to_check.y > col_entity.pos.y - self.entity.get_height()
                    lowerBound = pos_to_check.y < col_entity.pos.y + col_entity.get_height()
                    rightBound = pos_to_check.x + self.entity.get_width()> col_entity.pos.x
                    leftBound = pos_to_check.x < col_entity.pos.x + col_entity.get_width()
                    if upperBound and lowerBound:
                        if rightBound and leftBound:
                            if col_entity.type=="key":
                                self.entity.getKey(col_entity.keyColor)
                                other_entities.remove(col_entity)
                                break
                            elif col_entity.type=="background":
                                TextureComponent.changeBackground(col_entity.background)
                            elif col_entity.type=="trigger":
                                if col_entity.triggerType=="messageBox" and not col_entity.triggered:
                                    SystemComponent.showMessage(col_entity.triggerInfo)
                                    col_entity.triggered = True
                            else:
                                check = False
                                if col_entity.type=="door":
                                    check = self.entity.useKey(col_entity.keyColor)
                                    if check:
                                        col_entity.type = "decor"
                                        col_entity.WIDTH = 80
                                        col_entity.pos.x+=2
                                        col_entity.changeSprite("drzwi_" + col_entity.keyColor + ".png")
                                if not check:
                                    if i == 0:
                                        if col_entity.type=="plat" or col_entity.type=="ladder":
                                            if self.speed.y>0 and pos_to_check.y<=col_entity.pos.y-col_entity.get_height():
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
    
# CAMERA

class Camera:
    def __init__(self, focus_object, other_objects = [], y_centre = 400) -> None:
        self.focus_object = focus_object
        self.other_objects = other_objects
        self.y_centre = y_centre
        self.current_pos = vector2d(0,0)
    def update(self, window):
        camera_centre = vector2d(window.get_width()/2,window.get_height()/2);
        new_camera_pos = vector2d(0,0);
        player_pos = self.focus_object.pos
        vec_to_player = camera_centre - player_pos;
        
        self.move_camera(new_camera_pos.lerp(vec_to_player, 0.1), window);


    def move_camera(self,move_vector, window):
        
        #run every tick
        #moves the camera by changing pos of all objects
        #move_vec = -self.focus_object.last_movement
        move_vec = move_vector;
        #move_vec.y = 0
        self.focus_object.move_by(move_vec)
        #window_height = window.get_height()
        #abs_f_obj_y = abs(self.focus_object.pos.y)
        #offset = window_height/2.3\
        
        #if abs_f_obj_y < window_height/2 - offset or abs_f_obj_y > window_height/2 + offset:
        #    self.centre_camera(vector2d(window.get_width(), window.get_height()))
        for entity in self.other_objects:
            entity.move_by(vector2d((move_vec.x), (move_vec.y)))

    def centre_camera(self, window_dimensions):
        #centers the camera to the middle of window_dimensions
        window_centre = window_dimensions/2
        window_centre.x -= window_dimensions.x/10
        window_centre.y += window_dimensions.y/6
        move_vec = window_centre - self.focus_object.pos
        self.focus_object.move_by(move_vec)
        for entity in self.other_objects:
            entity.move_by(vector2d((move_vec.x), (move_vec.y)))

# CLASSES FOR GAME ENTITIES

class Entity(pygame.sprite.Sprite): # dziedziczenie po sprite
     # test wiarygodnosci argumentow
    def __new__(cls, _window, _x,_y, width=10, height=10, type=None, sprite=None, foreground=False, background=None, triggerType=None, triggerInfo=None):
        #do checks for window, height, width later
        if not isinstance(_x, float) and not isinstance(_x, int):
            raise TypeError("Pierwszy argument inicjalizacji obiektu klasy Entity (_x) musi być typu numerycznego float lub int!")
        if not isinstance(_y, float) and not isinstance(_y, int):
            raise TypeError("Pierwszy argument inicjalizacji obiektu klasy Entity (_y) musi być typu numerycznego float lub int!")
        return super(Entity, cls).__new__(cls)
    def __init__(self,window,_x,_y, _width, _height, _control,_moveable, type=None,sprite=None, foreground=False, triggerType=None, triggerInfo=None):
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
            self.area = pygame.image.load(path.join(SPRITES_DIR,sprite)).convert_alpha()
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
        self.area = pygame.image.load(path.join(SPRITES_DIR,spriteDir)).convert_alpha()
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
    def __init__(self,window, _x, _y, in_width = APP_WIDTH, in_height = 120, _type = "block", sprite=None, foreground=False, background=None, triggerType=None, triggerInfo=None):
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
        elif self.type =="trigger":
            self.triggerInfo = eval(triggerInfo)
            self.triggerType = triggerType
            self.triggered = False
