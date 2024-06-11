from components.GameConstants import *

class Animation(pygame.sprite.Sprite):
    frameAmountDict = {"szczur": 3, "matkaKacpra" : 1, "player" : 1, "roboSzczur": 5, "szczurBoss": 4, "zombieSzczur": 6 }
    def __init__(self, package):
        self.flip = False
        self.animationDelayConst = 10
        self.width = package["width"]
        self.height = package["height"]
        self.type = package["type"]
        self.loadImages()

    def loadImages(self, flipped=False):
        self.animationFrameList = []
        self.animationFrame = -1
        self.animationDelay = 0
        for i in range (Animation.frameAmountDict[self.type]):
            sprite = self.type + "_left" + str(i) + ".png"
            image_path = path.join(SPRITES_DIR, sprite)
            self.animationFrameList.append(pygame.image.load(image_path).convert_alpha())
            if flipped:
                self.animationFrameList[i]= pygame.transform.flip(self.animationFrameList[i], True, False)
            self.animationFrameList[i] = pygame.transform.scale(self.animationFrameList[i], (self.width, self.height))

    def animate(self):
        if self.animationDelay >= self.animationDelayConst:
            self.animationFrame = (self.animationFrame + 1) % Animation.frameAmountDict[self.type]
            self.animationDelay = 0
        else:
            self.animationDelay += 1
        return self.animationFrameList[self.animationFrame]

    def flip_img(self):
        self.flip = not self.flip
        self.loadImages(flipped = self.flip)