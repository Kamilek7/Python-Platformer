from components.Entity import *
from components.Animation import *

class Enemy(Entity):
    specsChart = {"szczur" : {"width":60,"height":20,"speed":0.20},"roboSzczur" : {"width":60,"height":20,"speed":0.20},"zombieSzczur" : {"width":60,"height":20,"speed":0.20},"szczurBoss" : {"width":180,"height":60,"speed":0.05}, "matkaKacpra" : {"width":40,"height":80,"speed":0.10}}
    def __init__(self, okno, x, y, type="szczur", id=None):
        super().__init__(okno, x, y,Enemy.specsChart[type]["width"],Enemy.specsChart[type]["height"],False, True, type="enemy")
        self.type = "enemy"
        self.id = id
        if self.id=="None":
            self.id = None
        self.enemType = type
        self.zdrowie = 1  # Przykladowy atrybut dla zdrowia wroga
        sprite = type + "_left0.png"
        self.area = pygame.image.load(path.join(SPRITES_DIR, sprite)).convert_alpha()
        self.area = pygame.transform.scale(self.area, (self.WIDTH, self.HEIGHT))

        # Nowe atrybuty
        self.delay = 0
        self.who = None
        self.movementToMake = None
        self.destroyed = False
        self.speed = Enemy.specsChart[type]["speed"]
        self.direction = vector2d(self.speed, 0)  # Kierunek ruchu (zmniejszony krok dla wolniejszego ruchu)
        self.steps_taken = 0  # Licznik kroków
        self.wait = True
        self.coolDown = 0
        animPackage = {"type": self.enemType, "width": self.WIDTH, "height": self.HEIGHT}
        self.animation = Animation(animPackage)
        self.flipFlag = True
        self.directionTemp = 1

    def zniszcz(self):
        self.destroyed=True

    def takeDamage(self, obrazenia=1):
        if self.coolDown<=0:
            self.zdrowie -= obrazenia
            self.coolDown=100
        if self.zdrowie <= 0:
            self.zniszcz()
    
    def animate(self):
        self.area = self.animation.animate()
    
    def triggerPass(self, triggerMovement, sender):
        def decompress(tekst):
            temp=""
            num = ""
            for i in tekst:
                if i.isdigit():
                    num+= i
                else:
                    temp+= int(num)*i
                    num=""
            return temp
        self.delay = int(triggerMovement["delay"])
        self.movementToMake = decompress(triggerMovement["movement"])
        
        self.steps_taken = 0
        self.who = sender

    def triggerManagement(self):
        if self.delay>0:
            self.delay -=1
        else:
            if self.steps_taken < 45:
                self.steps_taken += 1
                if self.movementToMake[0]=="L":
                    self.direction.x = -self.speed
                elif self.movementToMake[0]=="R":
                    self.direction.x = self.speed
                if self.movementToMake[0]!="W":
                    if self.direction.x != self.directionTemp:
                        self.flipFlag = True
                    self.physics_component.move(vector2d(self.direction.x, 0))
            else:
                self.steps_taken = 0
                if len(self.movementToMake)>1:
                    self.movementToMake = self.movementToMake[1:]
                else:
                    self.movementToMake = None
                    self.who.catchEndOfAction()

    def update(self, in_other_entities=[], player_pos=None):
        prev_pos = vector2d(self.pos.x, self.pos.y)
        # Sprawdź odległość między graczem a wrogiem
        if self.movementToMake!=None:
            self.triggerManagement()
        else:
            if player_pos and self.pos.distance_to(player_pos) < 200 and self.enemType!="matkaKacpra":
                # Jeśli gracz jest w odległości mniejszej niż 75, zmień kierunek ruchu na kierunek gracza
                self.direction = player_pos - self.pos
                self.direction.y = 0
                if self.direction.x!=0:
                    self.direction.x = self.direction.x/abs(self.direction.x)*self.speed*3
                    if self.direction.x != self.directionTemp:
                        self.flipFlag = True
                self.physics_component.move(self.direction)
            else:
                # W przeciwnym razie kontynuuj zwykły schemat ruchu
                if self.steps_taken < 75:
                    if not self.wait:
                        if self.direction.x>self.speed:
                            self.direction.x = self.speed
                        self.physics_component.move(self.direction)
                    self.steps_taken += 1
                else:
                    if self.wait:
                        self.direction.x *= -1  # Zmień kierunek ruchu
                        self.flipFlag = True
                    self.wait = not self.wait
                    self.steps_taken = 0  # Zresetuj licznik kroków
        self.directionTemp = self.direction.x
        if self.flipFlag:
            self.animation.flip_img()
            self.flipFlag = False
        self.animate()
        
        if self.coolDown>0:
            self.coolDown-=1
        self.physics_component.update_pos(in_other_entities)
        self.last_movement = self.pos - prev_pos
    