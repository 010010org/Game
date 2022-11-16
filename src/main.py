import pygame
import sprites as sp
import config as cf
import sys
import os

class Game:
    iconPath = os.path.join(os.getcwd(), "Game/sprites/icons")
    playerPath = os.path.join(os.getcwd(), "Game/sprites/Players")

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((cf.WIN_WIDTH, cf.WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        icon = pygame.image.load(self.iconPath + "/010010.png")
        pygame.display.set_icon(icon)
        
        #self.font = pygame.font.Font('Arial', 32)
        self.running = True

        self.characterSpriteSheet = sp.Spritesheet(self.playerPath + "/Bibber_walkcycle.png")

    
    def createTilemap(self):
        """draw the map according to the 2d array tilemap"""
        for i, row in enumerate(cf.tilemap):
            for j, column in enumerate(row):
                if column == "B":
                    sp.Block(self, j, i)
                if column == "P":
                    sp.Player(self, j, i)
                if column == "C":
                    sp.collectable(self, j, i)
    
    def new(self):
        """a new game starts"""

        self.playing = True

        self.allSprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    def events(self):
        """game loop events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        """game loop updates"""
        self.allSprites.update()


    def draw(self):
        self.screen.fill(cf.BLUE)
        self.allSprites.draw(self.screen)
        self.clock.tick(cf.FPS)
        pygame.display.update()

    def main(self):
        """game loop"""
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.playing = False

    def gameOver(self):
        pass

    def introScreen(self):
        pass





game = Game()
game.introScreen()
game.new()
while game.running:
    game.main()
    game.gameOver()


pygame.quit()
sys.exit()