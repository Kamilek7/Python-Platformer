from components.Entity import *
from components.MessageManager import *
from components.GameConstants import *

class Grounds(Entity):
    def __new__(cls, _window, posX, posY, width, height, type, sprite=None, foreground=False,background=None, cutsceneInfo=None):
        if not isinstance(sprite, str) and sprite != None:
            raise TypeError("sprite musi być str")
        return super(Grounds, cls).__new__(cls, _window, posX, posY, width, height, "block", sprite=sprite, foreground=foreground, background=background,cutsceneInfo=None)
    
    def __init__(self,window, _x, _y, in_width = APP_WIDTH, in_height = 120, _type = "block", sprite=None, foreground=False, background=None, cutsceneInfo=None):
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
            self.cutsceneInfo = eval(cutsceneInfo)
            self.triggered = False
            self.others = []
            self.player = None

    def manageTrigger(self, others, player):
        if not self.triggered:
            self.others = others
            self.triggered = True
            self.catchEndOfAction()
            self.player = player
            self.player.blockedMovement= True

    def catchEndOfAction(self):
        if len(self.cutsceneInfo)>0:
            tempTrigger = self.cutsceneInfo[0]
            self.cutsceneInfo = self.cutsceneInfo[1:]
            if tempTrigger["type"]=="messageBox":
                MessageManager.passMessage(tempTrigger, self)
            elif tempTrigger["type"]=="moveEntity":
                for i in self.others:
                    if i.id == tempTrigger["id"]:
                        i.triggerPass(tempTrigger, self)
            elif tempTrigger["type"]=="endGame":
                for i in self.others:
                    if i.id == "player":
                        i.zdrowie = 0
                self.catchEndOfAction()
            elif tempTrigger["type"]=="killEntity":
                for i in self.others:
                    if i.id == tempTrigger["id"]:
                        if i.type=="enemy":
                            i.zniszcz()
                self.catchEndOfAction()
        else:
            if self.player!=None:
                self.player.blockedMovement = False
