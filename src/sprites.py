import pygame
import config as cf
import math
import random

class Spritesheet():
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def getSprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(cf.BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = cf.PLAYER_LAYER
        self.groups = self.game.allSprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * cf.TILEWIDTH
        self.y = y * cf.TILEHEIGHT
        self.width = cf.TILEWIDTH
        self.height = cf.TILEHEIGHT

        self.xChange = 0
        self.yChange = 0


        self.facing = "left"
        self.animationLoop = 1

        image_to_load = self.game.characterSpriteSheet.getSprite(8,3, 15, 30)

        self.image = pygame.Surface([self.width, self.height])
        #leftover area of the sprite is now transparent
        self.image.set_colorkey(cf.BLACK)
        self.image.blit(image_to_load, (0,0))

        self.rect =self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.gravity()
        self.animate()
        
        
        self.rect.x += self.xChange
        self.collideBlocks("x")

        self.rect.y += self.yChange
        self.collideBlocks("y")
        
        self.xChange = 0
        self.yChange = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.xChange -= cf.PLAYER_SPEED
            self.facing = "left"
        if keys[pygame.K_RIGHT]:
            self.xChange += cf.PLAYER_SPEED
            self.facing = "right"
        if keys[pygame.K_UP]:
            self.yChange -= cf.PLAYER_JUMP_SPEED
            self.facing = "up"
        if keys[pygame.K_DOWN]:
            self.yChange += cf.PLAYER_SPEED
            self.facing = "down"
    
    def gravity(self):
        self.yChange += 2.5
    
    def animate(self):
        walkingAnimation = [
            self.game.characterSpriteSheet.getSprite(0,0,32,32),
            self.game.characterSpriteSheet.getSprite(0,32,32,32),
            self.game.characterSpriteSheet.getSprite(0,64,32,32),
            self.game.characterSpriteSheet.getSprite(0,96,32,32),
            self.game.characterSpriteSheet.getSprite(0,128,32,32),
            self.game.characterSpriteSheet.getSprite(0,160,32,32),
            self.game.characterSpriteSheet.getSprite(0,192,32, 32),
            self.game.characterSpriteSheet.getSprite(0,224, 32, 32)
        ]
        if self.facing == "left":
            if self.xChange == 0:
                self.image = pygame.transform.flip(walkingAnimation[4], True, False)
            else:
                self.image = pygame.transform.flip(walkingAnimation[math.floor(self.animationLoop)], True, False)
                self.animationLoop += 0.2
                if self.animationLoop >= len(walkingAnimation):
                    self.animationLoop = 1

        if self.facing == "right":
            if self.xChange == 0:
                self.image = walkingAnimation[1]
            else:
                self.image = walkingAnimation[math.floor(self.animationLoop)]
                self.animationLoop += 0.2
                if self.animationLoop >= len(walkingAnimation):
                    self.animationLoop = 1
    
    def collideBlocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.xChange > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.xChange < 0:
                    self.rect.x = hits[0].rect.right
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.yChange > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.yChange < 0:
                    self.rect.y = hits[0].rect.bottom


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = cf.BLOCK_LAYER
        self.groups = self.game.allSprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * cf.TILEWIDTH
        self.y = y * cf.TILEHEIGHT
        self.height = cf.TILEHEIGHT
        self.width = cf.TILEWIDTH

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(cf.BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class collectable(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = cf.COLLLECTABLE_LAYER
        self.groups = self.game.allSprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * cf.TILEWIDTH
        self.y = y * cf.TILEHEIGHT
        self.height = cf.TILEHEIGHT
        self.width = cf.TILEWIDTH

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(cf.GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
