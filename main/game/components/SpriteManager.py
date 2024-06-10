import pygame

class SpriteManager:
    spritesB = pygame.sprite.Group()
    spritesF = pygame.sprite.Group()
    
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