
 # wszystkie definicje i wstepne wartosci
 # meow

from components.InputComponent import *
from components.SpriteManager import *
from components.MessageManager import *
from components.MenuManager import *
from components.BackgroundManager import *
from components.Entity import *
from components.Enemy import *
from components.Player import *
from components.Camera import *
from components.Grounds import *
from components.SystemComponent import *

pygame.init()
pygame.font.init()
    
 # definicja dla wektora, dla latwych przeksztalcen
vector2d = pygame.math.Vector2
 # stałe
APP_HEIGHT = 600
APP_WIDTH = 800
MAX_FPS = 60
 # definicje dla okna
current_fps = pygame.time.Clock()
flags = RESIZABLE | DOUBLEBUF | SCALED
window = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT), flags)
pygame.display.set_caption("MATKA KACPRA - THE GAME")
mainMenu = True

 # elementy gry

while mainMenu:
    key = pygame.key.get_pressed()
    if key[K_RETURN]:
        MenuManager.menuFadeFlag=True
        mainMenu=False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
    MenuManager.manageMenu(window)
    pygame.display.update()
    current_fps.tick(MAX_FPS)

while True:
    running=True
    package = SystemComponent.loadMaps(window)
    levels = package["levels"]
    playerSpawn = package["playerSpawn"]
    platforms = levels[0]
    player = Player(window,playerSpawn[0],playerSpawn[1])
    SpriteManager.setSprites(platforms,player)
    moveables = package["moveables"]
    moveables.append(player)
    main_camera = Camera(player, platforms)
    # game loop
    

    main_camera.centre_camera(vector2d(window.get_width(), window.get_height()))
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == VIDEORESIZE:
                main_camera.update(window, force=True)
        
        BackgroundManager.manageBackground(window)
        
        # Aktualizacja wrogów, przekazując im pozycję gracza
        for entity in moveables:
            if not entity.destroyed:
                if isinstance(entity, Enemy):
                    entity.update(platforms, player.pos)
                else:
                    entity.update(platforms, moveables)
            else:
                if isinstance(entity, Enemy):
                    platforms.remove(entity)
                else:
                    player.changeSprite(None)
                moveables.remove(entity)

        main_camera.update(window)
        if len(platforms) < len(SpriteManager.spritesB) + len(SpriteManager.spritesF) - 1:
            SpriteManager.setSprites(platforms, player)
        for entity in SpriteManager.spritesB:
            window.blit(entity.area, entity.shape)
        for entity in SpriteManager.spritesF:
            window.blit(entity.area, entity.shape)
        for messageBox in MessageManager.messageBoxes:
            MessageManager.showMessage(window, messageBox)
        if MenuManager.menuFlag:
                MenuManager.manageMenu(window)
        if MenuManager.gameOverFlag:
            MenuManager.manageGameOver(window)
        pygame.display.update()
        current_fps.tick(MAX_FPS)
        
        while player.zdrowie <= 0:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
            key = pygame.key.get_pressed()
            if key[K_RETURN]:
                MenuManager.menuFadeFlag=True
                running=False
                player.zdrowie=1
            MenuManager.manageGameOver(window)
            pygame.display.update()
            current_fps.tick(MAX_FPS)