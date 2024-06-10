from os import *
from components.GameConstants import *

class MessageManager:
    delay = 0
    who = None
    messageBoxes = []
    tempIcon = None
    messageFadeFlag = False
    messageVisibility = False
    messageLifespan = 0
    messageSizeFade = 0
    
    @staticmethod
    def appendMessages(package):
        MessageManager.messageBoxes.append(package)
    
    @staticmethod
    def showMessage(_window, package):
        if MessageManager.delay > 0:
            MessageManager.delay -= 1
        else:
            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = my_font.render(package["text"], True, (255, 255, 255))
            width = int(_window.get_width() / 1.1)
            height = int(_window.get_height() / 3.5)
            posX = int((_window.get_width() - width) / 2)
            posY = int(_window.get_height() - _window.get_height() / 3)
            avatarWidth = int(height / 1.3)
            avatarHeight = avatarWidth
            border = (height - height / 1.3) / 2
            if MessageManager.tempIcon is None and package["icon"] != "None":
                MessageManager.tempIcon = pygame.image.load(path.join(AVATARS_DIR, package["icon"])).convert_alpha()
            if MessageManager.messageFadeFlag and not MessageManager.messageVisibility:
                if MessageManager.messageSizeFade >= 100:
                    MessageManager.messageSizeFade = 100
                    MessageManager.messageFadeFlag = False
                    MessageManager.messageVisibility = True
                    MessageManager.messageLifespan = 100
                else:
                    MessageManager.messageSizeFade += 5
            elif not MessageManager.messageFadeFlag and MessageManager.messageVisibility:
                if MessageManager.messageLifespan > 0:
                    MessageManager.messageLifespan -= 1
                else:
                    MessageManager.messageLifespan = 0
                    MessageManager.messageFadeFlag = True
            elif MessageManager.messageFadeFlag and MessageManager.messageVisibility:
                if MessageManager.messageSizeFade <= 0:
                    MessageManager.messageSizeFade = 0
                    MessageManager.messageFadeFlag = False
                    MessageManager.messageVisibility = False
                    MessageManager.messageBoxes.remove(package)
                    MessageManager.who.catchEndOfAction()
                else:
                    MessageManager.messageSizeFade -= 5
            height = int(height * MessageManager.messageSizeFade / 100)
            avatarHeight = int(avatarHeight * MessageManager.messageSizeFade / 100)
            pygame.draw.rect(_window, (0, 0, 0), pygame.Rect(posX, posY, width, height))
            if package["icon"] != "None":
                temparea = MessageManager.tempIcon
                temparea = pygame.transform.scale(temparea, (avatarWidth, avatarHeight))
                _window.blit(temparea, (posX + border, posY + border))
                if MessageManager.messageVisibility and not MessageManager.messageFadeFlag:
                    _window.blit(text_surface, (posX + avatarWidth + 2 * border, posY + border))
            elif MessageManager.messageVisibility and not MessageManager.messageFadeFlag:
                _window.blit(text_surface, (posX + border, posY + border))