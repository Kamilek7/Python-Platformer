from components.Entity import *

class Player(Entity): # dziedziczenie po entity
    def __new__(cls, _window, posX, posY):
        if not isinstance(posX, (int, float)) or not isinstance(posY, (int, float)):
            raise TypeError("posX i posY musza byc int lub float")
        return super(Player, cls).__new__(cls, _window, posX, posY)
    
    def __init__(self,window,_x,_y, in_width = 36, in_height = 75):
         # X, Y, WYSOKOSC, SZEROKOSC, KOLOR, PED PRZY RUCHU, TARCIE, RUCHOME, MOZNA STEROWAC
                 #grawitacja
        super().__init__(window,_x, _y, in_width, in_height, True, True, type="player",sprite="protag_idle.png")

        self.blockedMovement = False
         # inventory
        self.id = "player"
        self.coolDown = 0
        self.zdrowie = 4
        self.destroyed = False
        self.type= "player"
        self.keys = {"red":0,"purple":0,"green":0}
    def getKey(self,type):
        self.keys[type]+=1

    def useKey(self, type):
        if self.keys[type]>0:
            self.keys[type]-=1
            return True
        else:
            return False

    def zniszcz(self):
        self.destroyed=True

    def takeDamage(self, obrazenia=1):
        if self.coolDown<=0:
            self.zdrowie -= obrazenia
            self.coolDown = 200
        if self.zdrowie <= 0:
            self.zniszcz()

    def update(self, in_other_entities = [], in_other_moveables = []):
        prev_pos = vector2d(self.pos.x, self.pos.y)
        if not self.blockedMovement:
            move_input = self.input_component.get_movement_vec(self.physics_component.is_on_ground)
            self.physics_component.move(move_input)
        self.physics_component.update_pos(in_other_entities, others = in_other_moveables)
        self.last_movement = self.pos - prev_pos
        if self.coolDown>0:
            self.coolDown-=1
