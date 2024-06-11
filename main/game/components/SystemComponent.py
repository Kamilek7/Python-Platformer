from components.GameConstants import *
from components.Grounds import *
from components.Enemy import *
from xml.dom import minidom

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
