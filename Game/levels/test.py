import pygame

pygame.init()

screenHeight = 480
screenWidth = 720

screen = pygame.display.set_mode((screenWidth,screenHeight))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            exit()

    pressedKeys = pygame.key.get_pressed()

    screen.fill((255,255,255))
    #screen.blit()   
    
    pygame.display.flip()
