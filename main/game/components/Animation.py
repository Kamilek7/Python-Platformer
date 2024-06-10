from components.GameConstants import *
from components.Entity import *

class Animation(Entity):
    def __init__(self, window, _x, _y, animationFrameList):
            super().__init__(window, _x, _y, sprite=None)
            self.animationFrameList = animationFrameList

    def animate(self, typ):
            if typ != "matkaKacpra":
                if typ == "szczur":
                    self.animationFrameList = ["szczur_idle.png", "szczur_left1.png", "szczur_left2.png"]
                if typ == "szczurBoss":
                    self.animationFrameList = ["szczurBoss_idle.png", "szczurBoss_left1.png", "szczurBoss_left2.png", "szczurBoss_left3.png"]
                if self.animationDelay >= self.animationDelayConst:
                    self.animationFrame = (self.animationFrame + 1) % len(self.animationFrameList)
                    self.changeSprite(self.animationFrameList[self.animationFrame])
                    self.animationDelay = 0
                else:
                    self.animationDelay += 1

    def flip_img(self):
    
        for sprite in self.animationFrameList:
            image_path = path.join(SPRITES_DIR, sprite)
  

            # Load the image
            image = pygame.image.load(image_path).convert_alpha()

            # Flip the image horizontally
            flipped_image = pygame.transform.flip(image, True, False)

            # Save the flipped image
            pygame.image.save(flipped_image, image_path)
            self.flip *= -1
  