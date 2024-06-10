import pygame
from components.GameConstants import *

class BackgroundManager:
    backgrounds = []
    tempBG1 = None
    tempBG2 = None
    backgroundAlpha = 0
    currentBGcoords = vector2d((0, 0))
    currentBGsize = vector2d((0, 0))
    
    @staticmethod
    def scaleBackground(window):
        if BackgroundManager.tempBG1:
            BackgroundManager.tempBG1 = pygame.transform.scale(BackgroundManager.tempBG1, (window.get_width(), window.get_height()))
    
    @staticmethod
    def manageBackground(window):
        if len(BackgroundManager.backgrounds) == 2:
            if BackgroundManager.tempBG2 is None:
                BackgroundManager.tempBG2 = pygame.image.load(path.join(BACKGROUNDS_DIR, BackgroundManager.backgrounds[1])).convert_alpha()
                BackgroundManager.tempBG2 = pygame.transform.scale(BackgroundManager.tempBG2, (window.get_width(), window.get_height()))
                BackgroundManager.tempBG2.set_alpha(0)
            window.blit(BackgroundManager.tempBG1, (0, 0))
            window.blit(BackgroundManager.tempBG2, (0, 0))
            if BackgroundManager.backgroundAlpha < 255:
                BackgroundManager.backgroundAlpha += 10
                if BackgroundManager.backgroundAlpha > 255:
                    BackgroundManager.backgroundAlpha = 255
                BackgroundManager.tempBG2.set_alpha(BackgroundManager.backgroundAlpha)
            else:
                BackgroundManager.backgroundAlpha = 0
                BackgroundManager.tempBG1 = pygame.image.load(path.join(BACKGROUNDS_DIR, BackgroundManager.backgrounds[1])).convert_alpha()
                BackgroundManager.tempBG1 = pygame.transform.scale(BackgroundManager.tempBG1, (window.get_width(), window.get_height()))
                BackgroundManager.backgrounds.remove(BackgroundManager.backgrounds[0])
                BackgroundManager.tempBG2 = None
        elif len(BackgroundManager.backgrounds) == 1:
            if BackgroundManager.tempBG1 is None:
                BackgroundManager.tempBG1 = pygame.image.load(path.join(BACKGROUNDS_DIR, BackgroundManager.backgrounds[0])).convert_alpha()
                BackgroundManager.tempBG1 = pygame.transform.scale(BackgroundManager.tempBG1, (window.get_width(), window.get_height()))
            window.blit(BackgroundManager.tempBG1, (0, 0))
    
    @staticmethod
    def changeBackground(newBackground):
        BackgroundManager.currentBGcoords.x = newBackground.pos.x - 40
        BackgroundManager.currentBGcoords.y = newBackground.pos.y - 40
        BackgroundManager.currentBGsize.x = newBackground.get_width() + 40
        BackgroundManager.currentBGsize.y = newBackground.get_height()
        checkLengthLess = len(BackgroundManager.backgrounds) < 2
        checkIfNotDefined = len(BackgroundManager.backgrounds) == 0
        check = checkLengthLess and (checkIfNotDefined or BackgroundManager.backgrounds[0] != newBackground.background)
        if check:
            BackgroundManager.backgrounds.append(newBackground.background)
