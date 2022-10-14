import pygame
from player import Player

pygame.init()

screenHeight = 480
screenWidth = 720

screen = pygame.display.set_mode((screenWidth,screenHeight))

player = Player()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            exit()

    pressedKeys = pygame.key.get_pressed()
    player.update(pressedKeys)
    player.moveDown()

    screen.fill((255,255,255))
    screen.blit(player.surface, player.rectangle)   
    
    pygame.display.flip()
