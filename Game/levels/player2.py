import pygame

class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super(Player2, self).__init__()
        self.surface = pygame.Surface((50, 50))
        self.surface.fill((60,120,180))
        self.rectangle = self.surface.get_rect()


    def moveLeft(self):
        self.rectangle.move_ip(-1, 0)

    def moveRight(self):
        self.rectangle.move_ip(1, 0)

    def jump(self):
        self.rectangle.move_ip(0, -3)
    
    def moveDown(self):
        self.rectangle.move_ip(0, 1)


    def update(self, pressedKeys):
        if pressedKeys[pygame.K_LEFT] or pressedKeys[ord('a')]:
            self.moveLeft()
        if pressedKeys[pygame.K_RIGHT] or pressedKeys[ord('d')]:
            self.moveRight()
        if pressedKeys[pygame.K_SPACE]:
            self.jump()

        if pressedKeys[pygame.K_ESCAPE]:
            exit()

        #outOfBounds
        if self.rectangle.left < 0:
            self.rectangle.left = 0
        if self.rectangle.right > 720:
            self.rectangle.right = 720
        if self.rectangle.top <= 0:
            self.rectangle.top = 0
        if self.rectangle.bottom >= 480:
            self.rectangle.bottom = 480        

        

