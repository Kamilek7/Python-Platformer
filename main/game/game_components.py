from os import *
from xml.dom import minidom
from pygame.locals import *

from components.InputComponent import *
from components.SpriteManager import *
from components.MessageManager import *
from components.MenuManager import *
from components.BackgroundManager import *
from components.Entity import *
from components.Enemy import *
from components.Player import *
from components.Camera import *



class SystemComponent:
    @staticmethod
    def loadMaps(_window):
        playerSpawn = (APP_WIDTH/5,60)
        levels = []
        for files in listdir(MAPS_DIR):
            maps = []
            moveables = []
            plik = minidom.parse(path.join(MAPS_DIR,files))
            mapa = plik.getElementsByTagName('map')[0]
            for child in mapa.childNodes:
                if child.tagName=="spawn":
                    playerSpawn = (int(child.getAttribute("x")),int(child.getAttribute("y")))
                elif child.tagName=="background":
                    maps.append(Grounds(_window,int(child.getAttribute("x")),int(child.getAttribute("y")),int(child.getAttribute("width")),int(child.getAttribute("height")),child.tagName,  background=child.getAttribute("background")))
                elif child.tagName=="trigger":
                    maps.append(Grounds(_window,int(child.getAttribute("x")),int(child.getAttribute("y")),int(child.getAttribute("width")),int(child.getAttribute("height")),child.tagName,  cutsceneInfo=child.getAttribute("cutsceneInfo")))
                elif child.tagName=="enemy":
                    temp = Enemy(_window,int(child.getAttribute("x")),int(child.getAttribute("y")), type=child.getAttribute("type"), id=child.getAttribute("id"))
                    moveables.append(temp)
                    maps.append(temp)
                else:
                    maps.append(Grounds(_window,int(child.getAttribute("x")),int(child.getAttribute("y")),int(child.getAttribute("width")),int(child.getAttribute("height")),child.tagName, child.getAttribute("sprite"), foreground=child.getAttribute("foreground")))
            levels.append(maps)
        package = {"levels": levels, "playerSpawn": playerSpawn, "moveables": moveables}
        return package
    @staticmethod
    def showMessage(package, sender):
        MessageManager.appendMessages(package)
        MessageManager.messageFadeFlag = True
        MessageManager.who = sender
        MessageManager.delay = int(package["delay"])
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
                SystemComponent.showMessage(tempTrigger, self)
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
                        if isinstance(i,Enemy):
                            i.zniszcz()
                self.catchEndOfAction()
        else:
            self.player.blockedMovement = False

    


