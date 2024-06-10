from os import *
from components.GameConstants import *

class MenuManager:
    menuFlag = True
    menuFadeFlag = False
    menu = None
    backgroundAlpha = 0
    messageFadeFlag = False
    messageLifespan = 0
    gameOverFlag = False
    
    @staticmethod
    def scaleMenu(window):
        if MenuManager.menu:
            MenuManager.menu = pygame.transform.scale(MenuManager.menu, (window.get_width(), window.get_height()))
    
    @staticmethod
    def manageMenu(window):
        if MenuManager.messageLifespan <= 0 and not MenuManager.menuFadeFlag:
            MenuManager.backgroundAlpha = 255
            if MenuManager.messageFadeFlag:
                MenuManager.menu = pygame.image.load(path.join(SYSTEM_DIR, "menu2.png")).convert_alpha()
                MenuManager.menu = pygame.transform.scale(MenuManager.menu, (window.get_width(), window.get_height()))
            else:
                MenuManager.menu = pygame.image.load(path.join(SYSTEM_DIR, "menu1.png")).convert_alpha()
                MenuManager.menu = pygame.transform.scale(MenuManager.menu, (window.get_width(), window.get_height()))
            MenuManager.messageFadeFlag = not MenuManager.messageFadeFlag
            MenuManager.messageLifespan = 40
        elif MenuManager.menuFadeFlag:
            MenuManager.backgroundAlpha -= 10
            if MenuManager.backgroundAlpha < 0:
                MenuManager.backgroundAlpha = 0
                MenuManager.menuFadeFlag = False
                MenuManager.menuFlag = False
                MenuManager.messageLifespan = 0
            MenuManager.menu.set_alpha(MenuManager.backgroundAlpha)
        MenuManager.messageLifespan -= 1
        window.blit(MenuManager.menu, (0, 0))
    
    @staticmethod
    def manageGameOver(window):
        if MenuManager.messageLifespan <= 0 and (not MenuManager.menuFadeFlag) and MenuManager.gameOverFlag:
            MenuManager.backgroundAlpha = 255
            MenuManager.messageFadeFlag = not MenuManager.messageFadeFlag
            if MenuManager.messageFadeFlag:
                MenuManager.menu = pygame.image.load(path.join(SYSTEM_DIR, "gameOver1.png")).convert_alpha()
                MenuManager.menu = pygame.transform.scale(MenuManager.menu, (window.get_width(), window.get_height()))
            else:
                MenuManager.menu = pygame.image.load(path.join(SYSTEM_DIR, "gameOver2.png")).convert_alpha()
                MenuManager.menu = pygame.transform.scale(MenuManager.menu, (window.get_width(), window.get_height()))
            MenuManager.messageLifespan = 40
        elif MenuManager.menuFadeFlag:
            MenuManager.backgroundAlpha -= 10
            if MenuManager.backgroundAlpha < 0:
                MenuManager.gameOverFlag = False
                MenuManager.backgroundAlpha = 0
                MenuManager.menuFadeFlag = False
                MenuManager.menuFlag = False
                MenuManager.messageLifespan = 0
            MenuManager.menu.set_alpha(MenuManager.backgroundAlpha)
        if not MenuManager.gameOverFlag:
            if MenuManager.backgroundAlpha == 0:
                MenuManager.menu = pygame.image.load(path.join(SYSTEM_DIR, "gameOver1.png")).convert_alpha()
                MenuManager.menu = pygame.transform.scale(MenuManager.menu, (window.get_width(), window.get_height()))
                MenuManager.backgroundAlpha = 10
                MenuManager.messageFadeFlag = True
            else:
                MenuManager.backgroundAlpha += 10
                if MenuManager.backgroundAlpha >= 255:
                    MenuManager.backgroundAlpha = 255
                    MenuManager.gameOverFlag = True
            MenuManager.menu.set_alpha(MenuManager.backgroundAlpha)
        else:
            MenuManager.messageLifespan -= 1
        window.blit(MenuManager.menu, (0, 0))