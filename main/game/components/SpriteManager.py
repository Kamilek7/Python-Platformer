import pygame
from components.GameConstants import *

class SpriteManager:
    spritesB = pygame.sprite.Group()
    spritesF = pygame.sprite.Group()
    heartIcon = None
    @staticmethod
    def setSprites(platforms, player):
        SpriteManager.spritesB = pygame.sprite.Group()
        SpriteManager.spritesF = pygame.sprite.Group()
        for p in platforms:
            if not p.foreground == "True":
                SpriteManager.spritesB.add(p)
            else:
                SpriteManager.spritesF.add(p)
        SpriteManager.spritesB.add(player)
    @staticmethod
    def drawHearts(window, num):
        if SpriteManager.heartIcon==None:
            SpriteManager.heartIcon = pygame.image.load(path.join(SYSTEM_DIR, "heart.png")).convert_alpha()
            SpriteManager.heartIcon = pygame.transform.scale(SpriteManager.heartIcon, (27, 27))
        for i in range (num-1):
            window.blit(SpriteManager.heartIcon,(i*30, 0))