import pygame
import time

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surface = pygame.Surface((50, 50))
        self.surface.fill((60,120,180))
        self.rectangle = self.surface.get_rect()
        self.right = True
        self.nextJump = 0
        self.jumpDelay = 700


    def moveLeft(self):
        self.rectangle.move_ip(-1, 0)

    def moveRight(self):
        self.rectangle.move_ip(1, 0)

    def jump(self):
        #print(f"current ticks: {pygame.time.get_ticks()}")
        #print(self.nextJump)
        #print(pygame.time.get_ticks() > self.nextJump)
        if pygame.time.get_ticks() > self.nextJump:
            self.rectangle.move_ip(0, -250) 
            self.nextJump = pygame.time.get_ticks() + self.jumpDelay
            
    
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

        

