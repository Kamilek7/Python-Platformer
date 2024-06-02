
 # wszystkie definicje i wstepne wartosci
 # meow

from os import *
from game_components import *

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
window = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT), RESIZABLE)
pygame.display.set_caption("MATKA KACPRA - THE GAME")
mainMenu = True

 # elementy gry

while mainMenu:
    key = pygame.key.get_pressed()
    if key[K_RETURN]:
        TextureComponent.menuFadeFlag=True
        mainMenu=False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        elif event.type == VIDEORESIZE:
            TextureComponent.scaleMenu(window)
    TextureComponent.manageMenu(window)
    pygame.display.update()
    current_fps.tick(MAX_FPS)

running=True
package = SystemComponent.loadMaps(window)
levels = package["levels"]
playerSpawn = package["playerSpawn"]
platforms = levels[0]
player = Player(window,playerSpawn[0],playerSpawn[1])
TextureComponent.setSprites(platforms,player)
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
            TextureComponent.scaleBackground(window)
            if TextureComponent.menuFlag:
                TextureComponent.scaleMenu(window)
    
    TextureComponent.manageBackground(window)
    
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
    if len(platforms) < len(TextureComponent.spritesB) + len(TextureComponent.spritesF) - 1:
        TextureComponent.setSprites(platforms, player)
    for entity in TextureComponent.spritesB:
        window.blit(entity.area, entity.shape)
    for entity in TextureComponent.spritesF:
        window.blit(entity.area, entity.shape)
    for messageBox in TextureComponent.messageBoxes:
        TextureComponent.showMessage(window, messageBox)
    if TextureComponent.menuFlag:
        TextureComponent.manageMenu(window)
    pygame.display.update()
    current_fps.tick(MAX_FPS)