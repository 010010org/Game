#Imports
import pygame
import math
import asyncio



#Initialiseren
pygame.init()



#Globale constanten
VERSION = "RELEASE 1.0 KEY/MOUSE"

WIDTH = 900
HEIGHT = 540
GRID_WIDTH = 20 
GRID_HEIGHT = 10
MIN_GRID_WIDTH = 1
MIN_GRID_HEIGHT = 1

FPS = 60

BLOCK_WIDTH = WIDTH / GRID_WIDTH
BLOCK_HEIGHT = BLOCK_WIDTH #Hoogte gelijk aan breedte; vierkant

MAIN_MENU, CHALLENGES_MENU, INSTRUCTIONS, BIBBER, ASSIGN_MOVEMENT, GRID_EDITOR, LEVEL_EDITOR, CODE_EDITOR, ENDING = 0, 1, 2, 3, 4, 5, 6, 7, 8 #Voor de gameMode variabel
LEFT, RIGHT, UP, DOWN = 0, 1, 2, 3 #Index voor player.movement
INCREASE, DECREASE = 1, -1 #Voor het aanpassen van de grid
X, Y = 0, 1 #Voor het aanpassen van de grid
DEFAULT, HOVER = 0, 1 #Index voor buttons (normale sprite / hover sprite)
PREVIOUS, NEXT = -1, 1 #Voor de cursor.setItem() functie
EMPTY, BLOCK, FINISH, RESET, GAME_OVER, PLAYER = 0, 1, 2, 3, 4, 5 #EMPTY = Lege ruimte op de grid

GRAVITY = 1
JUMP_SPEED = -15 #Negatief omdat de y-as bovenaan het 0-punt heeft
SPEED = 3

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)




#Display aanmaken
display = pygame.display.set_mode((WIDTH, HEIGHT))




#Clock (voor FPS) aanzetten
clock = pygame.time.Clock()




#Venstertitel instellen
pygame.display.set_caption('010010 - Bibber')




#Variabelen
items = [EMPTY, BLOCK, FINISH, RESET, GAME_OVER, PLAYER]
colors = [BLACK, GREEN, WHITE, BLUE, RED]




#Sprites
spriteEraser = pygame.image.load("assets/sprites/itemEraser.png").convert_alpha()
spriteBlock = pygame.image.load("assets/sprites/itemBlock.png").convert()
spriteFinish = pygame.image.load("assets/sprites/itemFinish.png").convert_alpha()
spriteReset = pygame.image.load("assets/sprites/itemReset.png").convert_alpha()
spriteGameOver = pygame.image.load("assets/sprites/itemGameOver.png").convert_alpha()
spritePlayer = pygame.image.load("assets/sprites/player.png").convert_alpha()
spriteStarEmpty = pygame.image.load("assets/sprites/starEmpty.png").convert_alpha()
spriteStarFull = pygame.image.load("assets/sprites/starFull.png").convert_alpha()
spriteChallengeLocked = pygame.image.load("assets/sprites/challengeLocked.png").convert_alpha()
spriteButtonLocked = pygame.image.load("assets/sprites/buttonLocked.png").convert_alpha()
sprites = [spriteEraser, spriteBlock, spriteFinish, spriteReset, spriteGameOver, spritePlayer] #Alleen de sprites die nodig zijn voor de opbouw van een level

backgroundMenu = pygame.image.load("assets/sprites/backgroundMenu.png").convert()
backgroundChallenges = pygame.image.load("assets/sprites/backgroundChallenges.png").convert()
backgroundGame = pygame.image.load("assets/sprites/backgroundGame.png").convert()
backgroundEnding = pygame.image.load("assets/sprites/backgroundEnding.png").convert()
bottomOverlay = pygame.image.load("assets/sprites/overlay.png").convert_alpha()

levelInstructions = []
for n in range(10):
    levelInstructions.append(pygame.image.load("assets/sprites/levelInstructions" + str(n + 1) + ".png").convert())




#Classes (Controller)
class Controller():
    def __init__(self):
        self.isGameFinished = False
        self.gameMode = MAIN_MENU
        self.challengeIndex = 0
        self.challengeLock = [False, True, True, True, True, True, True, True, True, True]
        self.instructionsFirstTime = True #Om ervoor te zorgen dat de map niet reset als de speler later nog een keer teruggaat naar de instructies TO-DO: Dit fixen!
        self.map = [[EMPTY] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.totalBlocks = 0 #Index voor het inladen van blocks
        self.isMouseClicked = [False, False] #Linker muisknop + rechter muisknop, LEFT en RIGHT als index gebruiken
        self.gridSizeMax = [MIN_GRID_WIDTH, MIN_GRID_HEIGHT]
        self.gridBorderLeft = [9, 10]
        self.gridBorderRight = [10, 10]
        self.gridBorderTop = [0, 5]
        self.gridBorderBottom = [0, 4]
        self.leftBorder = pygame.Surface((self.gridBorderLeft[X] * BLOCK_WIDTH, self.gridBorderLeft[Y] * BLOCK_HEIGHT))
        self.rightBorder = pygame.Surface((self.gridBorderRight[X] * BLOCK_WIDTH, self.gridBorderRight[Y] * BLOCK_HEIGHT))
        self.topBorder = pygame.Surface((WIDTH - (self.leftBorder.get_width() + self.rightBorder.get_width()), self.gridBorderTop[Y] * BLOCK_HEIGHT))
        self.bottomBorder = pygame.Surface((WIDTH - (self.leftBorder.get_width() + self.rightBorder.get_width()), self.gridBorderBottom[Y] * BLOCK_HEIGHT))
        self.leftBorderRect = self.leftBorder.get_rect()
        self.rightBorderRect = self.rightBorder.get_rect()
        self.topBorderRect = self.topBorder.get_rect()
        self.bottomBorderRect = self.bottomBorder.get_rect()
        self.playerStartingPosition = [-100, -100]
    def setGameMode(self, mode):
        if (mode == BIBBER):
            Bibber.reset() #Game resetten als Bibber opnieuw geopend wordt
        elif (mode == LEVEL_EDITOR):
            LevelEditor.reset()
        self.gameMode = mode
    def setChallenge(self, challengeNr):
        self.challengeIndex = challengeNr
    def resizeGridBorder(self, increaseDecrease, axis):
        if (increaseDecrease == INCREASE):
            if (axis == X and self.gridSizeMax[X] < GRID_WIDTH):
                self.gridSizeMax[X] += 1
                if (self.gridSizeMax[X] % 2 == 0):
                    self.gridBorderRight[X] -= 1
                elif (self.gridSizeMax[X] % 2 != 0):
                    self.gridBorderLeft[X] -= 1
            elif (axis == Y and self.gridSizeMax[Y] < GRID_HEIGHT):
                self.gridSizeMax[Y] += 1
                if (self.gridSizeMax[Y] % 2 == 0):
                    self.gridBorderTop[Y] -= 1
                elif (self.gridSizeMax[Y] % 2 != 0):
                    self.gridBorderBottom[Y] -= 1
        elif (increaseDecrease == DECREASE):
            if (axis == X and self.gridSizeMax[X] > MIN_GRID_WIDTH):
                self.gridSizeMax[X] -= 1
                if (self.gridSizeMax[X] % 2 != 0):
                    self.gridBorderRight[X] += 1
                elif (self.gridSizeMax[X] % 2 == 0):
                    self.gridBorderLeft[X] += 1
            elif (axis == Y and self.gridSizeMax[Y] > MIN_GRID_HEIGHT):
                self.gridSizeMax[Y] -= 1
                if (self.gridSizeMax[Y] % 2 != 0):
                    self.gridBorderTop[Y] += 1
                elif (self.gridSizeMax[Y] % 2 == 0):
                    self.gridBorderBottom[Y] += 1
    def drawGridBorder(self):
        self.leftBorder = pygame.Surface((self.gridBorderLeft[X] * BLOCK_WIDTH, self.gridBorderLeft[Y] * BLOCK_HEIGHT))
        self.leftBorderRect = self.leftBorder.get_rect()
        self.leftBorder.fill(BLACK)
        display.blit(self.leftBorder, (0, 0))
        self.rightBorder = pygame.Surface((self.gridBorderRight[X] * BLOCK_WIDTH, self.gridBorderRight[Y] * BLOCK_HEIGHT))
        self.rightBorderRect = self.rightBorder.get_rect()
        self.rightBorder.fill(BLACK)
        display.blit(self.rightBorder, ((GRID_WIDTH * BLOCK_WIDTH) - self.rightBorder.get_width(), 0))
        self.topBorder = pygame.Surface((WIDTH - (self.leftBorder.get_width() + self.rightBorder.get_width()), self.gridBorderTop[Y] * BLOCK_HEIGHT))
        self.topBorderRect = self.topBorder.get_rect()
        self.topBorder.fill(BLACK)
        display.blit(self.topBorder, (self.leftBorder.get_width(), 0))
        self.bottomBorder = pygame.Surface((WIDTH - (self.leftBorder.get_width() + self.rightBorder.get_width()), self.gridBorderBottom[Y] * BLOCK_HEIGHT))
        self.bottomBorderRect = self.bottomBorder.get_rect()
        self.bottomBorder.fill(BLACK)
        display.blit(self.bottomBorder, (self.leftBorder.get_width(), (GRID_HEIGHT * BLOCK_HEIGHT) - (self.gridBorderBottom[Y] * BLOCK_HEIGHT)))
    def loadMap(self):
        self.totalBlocks = 0 #Resetten
        block.clear() #Alle blokken verwijderen en opnieuw laten opbouwen
        for n in range(len(self.map)):
            for o in range(len(self.map[0])):
                objectType = int(self.map[n][o])
                if (objectType == PLAYER):
                    player.rect.x = o * BLOCK_WIDTH
                    player.rect.y = n * BLOCK_HEIGHT
                    self.playerStartingPosition[X] = o * BLOCK_WIDTH
                    self.playerStartingPosition[Y] = n * BLOCK_HEIGHT
                elif (objectType != EMPTY):
                    block.append(Block(o * BLOCK_WIDTH, n * BLOCK_HEIGHT, objectType))
                    self.totalBlocks += 1
    def clearMap(self): 
        self.map = [[EMPTY] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        item.clear()
        for n in range(GRID_WIDTH * GRID_HEIGHT):
            item.append(Item())
        LevelEditor.isPlayerDrawn = False
    def resetGame(self):
        self.clearMap()
        self.challengeIndex = 0
        for n in range(len(self.challengeLock)):
            self.challengeLock[n] = True
        self.challengeLock[0] = False
        player.reset()
        player.rect.x = -100
        player.rect.y = -100
    def checkInput(self):
        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN, pygame.KEYUP])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isGameFinished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button == 1): #Linker muisknop
                    self.isMouseClicked[LEFT] = True
                elif (event.button == 3): #Rechter muisknop
                    self.isMouseClicked[RIGHT] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if (event.button == 1): #Linker muisknop
                    self.isMouseClicked[LEFT] = False
                if (event.button == 3):
                    self.isMouseClicked[RIGHT] = False
    def update(self):
        self.checkInput()
        if (self.gameMode == MAIN_MENU):
            Menu.update()
        elif (self.gameMode == CHALLENGES_MENU):
            Challenges.update()
        elif (self.gameMode == INSTRUCTIONS):
            Instructions.update()
        elif (self.gameMode == BIBBER):
            Bibber.update()
            #Goals
            if (self.challengeIndex == 0):
                if (self.gridSizeMax == challenge[self.challengeIndex].gridSize):
                    self.challengeLock[1] = False
            elif (self.challengeIndex == 1):
                if (LevelEditor.isPlayerDrawn == True):
                    self.challengeLock[2] = False
            elif (self.challengeIndex >= 3 and self.challengeIndex <= 5):
                if (player.hitFinish == True):
                    self.challengeLock[self.challengeIndex + 1] = False
            elif (self.challengeIndex >= 6 and self.challengeIndex <= 8):
                if (player.hitFinish == True and LevelEditor.maxItems[BLOCK] == 0 and LevelEditor.maxItems[RESET] == 0 and 
                        LevelEditor.maxItems[GAME_OVER] == 0):
                    self.challengeLock[self.challengeIndex + 1] = False
        elif (self.gameMode == ASSIGN_MOVEMENT):
            AssignMovement.update()
            if (AssignMovement.movementsIndex[LEFT] == LEFT and AssignMovement.movementsIndex[RIGHT] == RIGHT and
                    AssignMovement.movementsIndex[UP] == UP and AssignMovement.movementsIndex[DOWN] == DOWN):
                self.challengeLock[3] = False
        elif (self.gameMode == GRID_EDITOR):
            GridEditor.update()
        elif (self.gameMode == LEVEL_EDITOR):
            LevelEditor.update()
        elif (self.gameMode == ENDING):
            Ending.update()




#Classes (GameModes)
class GM_MainMenu():
    def checkInput(self):
        if (controller.isMouseClicked[LEFT]): #Alleen hover checken als er door de speler op de linkermuisknop is geklikt
            if (buttonPlay.isHovered):
                controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                controller.setGameMode(CHALLENGES_MENU)
    def draw(self):
        display.blit(backgroundMenu, (0, 0))
    def update(self):
        self.draw()
        buttonPlay.update()
        self.checkInput()
                


class GM_ChallengesMenu():
    def __init__(self):
        self.challengeNrFont = pygame.font.SysFont('Consola.ttf', 92)
    def checkInput(self):
        if (controller.isMouseClicked[LEFT]): #Alleen hover checken als er door de speler op de linkermuisknop is geklikt
            if (buttonBackToMenu.isHovered):
                controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                controller.setGameMode(MAIN_MENU)
            else:
                for n in range (len(buttonChallenge)):
                    if (buttonChallenge[n].isHovered and controller.challengeLock[n] == False):
                        controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                        controller.setChallenge(n)
                        controller.setGameMode(INSTRUCTIONS)
    def draw(self):
        display.blit(backgroundChallenges, (0, 0))
        display.blit(bottomOverlay, (0, 0))
        for n in range(len(challenge)):
            for o in range(5):
                if (o < challenge[n].difficulty):
                    display.blit(spriteStarFull, ((buttonChallenge[n].rect.x + 15 + (o * 25)), buttonChallenge[n].rect.y + 60))
                elif (o >= challenge[n].difficulty):
                    display.blit(spriteStarEmpty, ((buttonChallenge[n].rect.x + 15 + (o * 25)), buttonChallenge[n].rect.y + 60))
            challengeNrText = self.challengeNrFont.render("{0}".format(n + 1), True, WHITE)
            display.blit(challengeNrText, (buttonChallenge[n].rect.x + 60, buttonChallenge[n].rect.y + 5))
            if (controller.challengeLock[n] == True):
                display.blit(spriteChallengeLocked, (buttonChallenge[n].rect.x, buttonChallenge[n].rect.y))
    def update(self):
        self.draw()
        for n in range(len(challenge)):
            buttonChallenge[n].update()
        buttonBackToMenu.update()
        self.checkInput()



class GM_Instructions():
    def checkInput(self):
        if (controller.isMouseClicked[LEFT]):
            if (buttonNext.isHovered):
                controller.isMouseClicked[LEFT] = False
                controller.setGameMode(GRID_EDITOR)
    def draw(self):
        display.blit(levelInstructions[controller.challengeIndex], (0, 0))
        display.blit(bottomOverlay, (0, 0))
    def update(self):
        self.checkInput()
        self.draw()
        buttonNext.update()



class GM_Bibber(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    def checkInput(self):
        if (controller.isMouseClicked[LEFT]): #Alleen hover checken als er door de speler op de linkermuisknop is geklikt
            if (buttonBackToMenu.isHovered):
                controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                controller.setGameMode(MAIN_MENU)
            elif (buttonLevelEditor.isHovered):
                controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                controller.setGameMode(LEVEL_EDITOR)
            elif (buttonBack.isHovered):
                controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                controller.setGameMode(CHALLENGES_MENU)
            elif (buttonInstructions.isHovered):
                controller.isMouseClicked[LEFT] = False
                controller.setGameMode(INSTRUCTIONS)
            elif (buttonNext.isHovered):
                if (controller.challengeIndex < 9):  
                    if (controller.challengeLock[controller.challengeIndex + 1] == False):
                        controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                        controller.setChallenge(controller.challengeIndex + 1)
                        controller.setGameMode(INSTRUCTIONS)
                        player.hitFinish = False
                elif (controller.challengeIndex == 9): 
                    controller.isMouseClicked[LEFT] = False
                    controller.setGameMode(ENDING)

    def reset(self):
        player.reset()
        controller.loadMap()
    def draw(self):
        display.blit(backgroundGame, (0, 0))
        display.blit(bottomOverlay, (0, 0))
    def update(self):
        self.checkInput()
        self.draw()
        controller.drawGridBorder()
        buttonBackToMenu.update()
        buttonBack.update()
        buttonNext.update()
        if (controller.challengeIndex <= 8):
            if (controller.challengeLock[controller.challengeIndex + 1] == True):
                display.blit(spriteButtonLocked, (buttonNext.rect.x, buttonNext.rect.y))
        buttonLevelEditor.update()
        buttonInstructions.update()
        player.updateTopDown()
        for n in range (controller.totalBlocks):
            block[n].update()



class GM_AssignMovement():
    def __init__(self):
        self.font = pygame.font.SysFont('Consola.ttf', 40)
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.fill(BLACK)
        self.movements = ["Toets[PijltjeLinks]", "Toets[PijltjeRechts]", "Toets[PijltjeBoven]", "Toets[PijltjeOnder]"]
        self.movementsIndex = [0, 0, 0, 0]
    def checkInput(self):
        if (controller.isMouseClicked[LEFT]):
            for n in range(len(self.movements)):
                if (buttonNextMovement[n].isHovered):
                    controller.isMouseClicked[LEFT] = False
                    if (self.movementsIndex[n] == 3):
                        self.movementsIndex[n] = 0
                    else:
                        self.movementsIndex[n] += 1
                elif (buttonPreviousMovement[n].isHovered):
                    controller.isMouseClicked[LEFT] = False
                    if (self.movementsIndex[n] == 0):
                        self.movementsIndex[n] = 3
                    else:
                        self.movementsIndex[n] -= 1
            if (buttonNext.isHovered and controller.challengeLock[controller.challengeIndex + 1] == False):
                controller.isMouseClicked[LEFT] = False
                controller.setChallenge(controller.challengeIndex + 1)
                controller.setGameMode(INSTRUCTIONS)
            elif (buttonBack.isHovered):
                controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                controller.setGameMode(CHALLENGES_MENU)
            elif (buttonBackToMenu.isHovered):
                controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                controller.setGameMode(MAIN_MENU)
    def draw(self):
        display.blit(self.background, (0, 0))
        display.blit(bottomOverlay, (0, 0))
        display.blit(self.font.render("ALS", True, BLUE), (100, 30))
        display.blit(self.font.render("{0}".format(self.movements[self.movementsIndex[LEFT]]), True, GREEN), (300, 30))
        display.blit(self.font.render("DAN:", True, BLUE), (650, 30))
        display.blit(self.font.render("BeweegBibber(LINKS)", True, RED), (250, 70))
        display.blit(self.font.render("ALS", True, BLUE), (100, 120))
        display.blit(self.font.render("{0}".format(self.movements[self.movementsIndex[RIGHT]]), True, GREEN), (300, 120))
        display.blit(self.font.render("DAN:", True, BLUE), (650, 120))
        display.blit(self.font.render("BeweegBibber(RECHTS)", True, RED), (250, 160))
        display.blit(self.font.render("ALS", True, BLUE), (100, 210))
        display.blit(self.font.render("{0}".format(self.movements[self.movementsIndex[UP]]), True, GREEN), (300, 210))
        display.blit(self.font.render("DAN:", True, BLUE), (650, 210))
        display.blit(self.font.render("BeweegBibber(BOVEN)", True, RED), (250, 250))
        display.blit(self.font.render("ALS", True, BLUE), (100, 300))
        display.blit(self.font.render("{0}".format(self.movements[self.movementsIndex[DOWN]]), True, GREEN), (300, 300))
        display.blit(self.font.render("DAN:", True, BLUE), (650, 300))
        display.blit(self.font.render("BeweegBibber(BENEDEN)", True, RED), (250, 340))
    def update(self):
        self.checkInput()
        self.draw()
        buttonBackToMenu.update()
        buttonBack.update()
        buttonNext.update()
        if (controller.challengeLock[controller.challengeIndex + 1] == True):
            display.blit(spriteButtonLocked, (buttonNext.rect.x, buttonNext.rect.y))
        for n in range(len(buttonNextMovement)):
            buttonNextMovement[n].update()
            buttonPreviousMovement[n].update()



class GM_GridEditor():
    def __init__(self):
        self.fontGridSize = pygame.font.SysFont('Consola.ttf', 20)
        self.fontGridSize2 = pygame.font.SysFont('Consola.ttf', 80)
    def checkInput(self):
        if (controller.isMouseClicked[LEFT]): #Alleen hover checken als er door de speler op de linkermuisknop is geklikt
            if (buttonBackToMenu.isHovered):
                controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                controller.setGameMode(MAIN_MENU)
            elif (buttonSaveAndExit_GE.isHovered):
                if (controller.gridSizeMax[X] == challenge[controller.challengeIndex].gridSize[X] and controller.gridSizeMax[Y] == challenge[controller.challengeIndex].gridSize[Y]):
                    controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                    controller.setGameMode(challenge[controller.challengeIndex].nextGameMode)
            elif (buttonIncreaseGridX.isHovered):
                controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                controller.resizeGridBorder(INCREASE, X)
            elif (buttonDecreaseGridX.isHovered):
                controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                controller.resizeGridBorder(DECREASE, X)
            elif (buttonIncreaseGridY.isHovered):
                controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                controller.resizeGridBorder(INCREASE, Y)
            elif (buttonDecreaseGridY.isHovered):
                controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                controller.resizeGridBorder(DECREASE, Y)
    def draw(self): #Teken de grid
        display.blit(backgroundGame, (0, 0))
        display.blit(bottomOverlay, (0, 0))
        for n in range(GRID_WIDTH):
            pygame.draw.line(display, BLUE, (BLOCK_WIDTH + (n * BLOCK_WIDTH), 0), (BLOCK_WIDTH + (n * BLOCK_WIDTH), GRID_HEIGHT * BLOCK_HEIGHT))
        for n in range(GRID_HEIGHT):
            pygame.draw.line(display, BLUE, (0, (BLOCK_HEIGHT + (n * BLOCK_HEIGHT))), (GRID_WIDTH * BLOCK_WIDTH, (BLOCK_HEIGHT + (n * BLOCK_HEIGHT))))
        gridXText = self.fontGridSize.render("X: {0}".format(controller.gridSizeMax[X]), True, WHITE)
        gridYText = self.fontGridSize.render("Y: {0}".format(controller.gridSizeMax[Y]), True, WHITE)
        display.blit(gridXText, (265, 490))
        display.blit(gridYText, (615, 490))
    def drawInstructions(self): #Deze apart tekenen omdat het anders onder de gridborder staat
        gridSizeText = self.fontGridSize2.render("Stel het speelveld in op {0} bij {1}".format(challenge[controller.challengeIndex].gridSize[X], challenge[controller.challengeIndex].gridSize[Y]), True, WHITE)
        display.blit(gridSizeText, (50, 50))
    def update(self):
        self.checkInput()
        self.draw()
        controller.drawGridBorder()
        self.drawInstructions()
        buttonBackToMenu.update()
        buttonSaveAndExit_GE.update()
        if (controller.gridSizeMax[X] != challenge[controller.challengeIndex].gridSize[X] or controller.gridSizeMax[Y] != challenge[controller.challengeIndex].gridSize[Y]):
            display.blit(spriteButtonLocked, (buttonSaveAndExit_GE.rect.x, buttonSaveAndExit_GE.rect.y))
        buttonIncreaseGridX.update()
        buttonDecreaseGridX.update()
        buttonIncreaseGridY.update()
        buttonDecreaseGridY.update()



class GM_LevelEditor():
    def __init__(self): 
        self.isPlayerDrawn = False #Voorkomt dat er meerdere spelers op het veld staan; er mag er maar 1 zijn
        self.maxItems = []
        self.fontMaxItems = pygame.font.SysFont('Consola.ttf', 45)
        self.changeItemBalance = True #Ervoor zorgen dat je per klik maar één item kunt toevoegen of verwijderen aan de maxItems[] array
    def reset(self):
        self.maxItems.clear()
        for n in range(len(items)):
            self.maxItems.append(challenge[controller.challengeIndex].itemCount[n])
        controller.clearMap()
    def checkInput(self):
        if (controller.isMouseClicked[LEFT] == False):
            self.changeItemBalance = True
        elif (controller.isMouseClicked[LEFT]):
            mouseX, mouseY = pygame.mouse.get_pos()
            gridX = (math.floor(mouseX / BLOCK_WIDTH))
            if (gridX > (GRID_WIDTH - 1)):
                gridX = GRID_WIDTH - 1
            gridY = (math.floor(mouseY / BLOCK_HEIGHT))
            if (gridY > (GRID_HEIGHT - 1)):
                gridY = GRID_HEIGHT - 1
            x = gridX * BLOCK_WIDTH
            if (x > (GRID_WIDTH * BLOCK_WIDTH) - BLOCK_WIDTH):
                x = (GRID_WIDTH * BLOCK_WIDTH) - BLOCK_WIDTH
            y = gridY * BLOCK_HEIGHT
            if (y > (GRID_HEIGHT * BLOCK_HEIGHT) - BLOCK_HEIGHT):
                y = (GRID_HEIGHT * BLOCK_HEIGHT) - BLOCK_HEIGHT
            if (buttonBackToMenu.isHovered):
                controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                controller.setGameMode(MAIN_MENU)
            elif (buttonSaveAndExit_LE.isHovered):
                controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                controller.setGameMode(BIBBER)
            elif (buttonItemPrevious.isHovered):
                controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                cursor.setItem(PREVIOUS)
            elif (buttonItemNext.isHovered):
                controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                cursor.setItem(NEXT)
            elif (mouseY < (HEIGHT - (2 * BLOCK_HEIGHT)) and gridX >= (controller.gridBorderLeft[X]) and gridX <= (GRID_WIDTH - controller.gridBorderRight[X] - 1)
                    and gridY >= (controller.gridBorderTop[Y]) and gridY <= (GRID_HEIGHT - controller.gridBorderBottom[Y] - 1)): 
                #Voorkom dat er een object wordt aangemaakt wanneer er op de knoppen beneden op het scherm wordt getikt en dat je items kan plaatsen op de zwarte grid
                if (cursor.currentItemIndex == EMPTY): #Gum
                    item[gridX + (gridY * GRID_WIDTH)].setVisible(False)
                    if (self.changeItemBalance == True):
                        self.maxItems[controller.map[gridY][gridX]] += 1
                        self.changeItemBalance = False
                    if (controller.map[gridY][gridX] == PLAYER):
                        self.isPlayerDrawn = False
                    controller.map[gridY][gridX] = EMPTY #Leeg veld
                elif (cursor.currentItemIndex == PLAYER and not self.isPlayerDrawn):
                    item[gridX + (gridY * GRID_WIDTH)].spawn(x, y, cursor.currentItemIndex)
                    if (self.changeItemBalance == True):
                        self.maxItems[cursor.currentItemIndex] -= 1
                        self.changeItemBalance = False
                    controller.map[gridY][gridX] = items[cursor.currentItemIndex]
                    self.isPlayerDrawn = True
                elif (cursor.currentItemIndex != PLAYER and self.maxItems[cursor.currentItemIndex] > 0):
                    item[gridX + (gridY * GRID_WIDTH)].spawn(x, y, cursor.currentItemIndex)
                    if (self.changeItemBalance == True):
                        self.maxItems[cursor.currentItemIndex] -= 1
                        self.changeItemBalance = False
                    controller.map[gridY][gridX] = items[cursor.currentItemIndex]
    def draw(self): #Teken de grid
        display.blit(backgroundGame, (0, 0))
        display.blit(bottomOverlay, (0, 0))
        for n in range(GRID_WIDTH * GRID_HEIGHT):
            item[n].draw()
        for n in range(GRID_WIDTH):
            pygame.draw.line(display, BLUE, (BLOCK_WIDTH + (n * BLOCK_WIDTH), 0), (BLOCK_WIDTH + (n * BLOCK_WIDTH), GRID_HEIGHT * BLOCK_HEIGHT))
        for n in range(GRID_HEIGHT):
            pygame.draw.line(display, BLUE, (0, (BLOCK_HEIGHT + (n * BLOCK_HEIGHT))), (GRID_WIDTH * BLOCK_WIDTH, (BLOCK_HEIGHT + (n * BLOCK_HEIGHT))))
        maxItemsText = self.fontMaxItems.render("{0}".format(self.maxItems[cursor.currentItemIndex]), True, WHITE)
        maxItemsTextShadow = self.fontMaxItems.render("{0}".format(self.maxItems[cursor.currentItemIndex]), True, BLACK)
        cursor.draw()
        if (cursor.currentItemIndex != EMPTY):
            display.blit(maxItemsTextShadow, (430, 476))
            display.blit(maxItemsText, (428, 474))
    def update(self):
        self.checkInput()
        self.draw()
        controller.drawGridBorder()
        buttonBackToMenu.update()
        buttonSaveAndExit_LE.update()
        buttonItemPrevious.update()
        buttonItemNext.update()



class GM_Ending():
    def checkInput(self):
        if (controller.isMouseClicked[LEFT]): #Alleen hover checken als er door de speler op de linkermuisknop is geklikt
            if (buttonBackToMenu.isHovered):
                controller.isMouseClicked[LEFT] = False #Voorkomen dat de muisknop ingedrukt kan worden gehouden
                controller.setGameMode(MAIN_MENU)
    def draw(self):
        display.blit(backgroundEnding, (0, 0))
        display.blit(bottomOverlay, (0, 0))
    def update(self):
        self.checkInput()
        self.draw()
        buttonBackToMenu.update()




#Classes (elementen)
class Button(pygame.sprite.Sprite):
    def __init__(self, spritePath, x, y):
        super().__init__()
        self.image = pygame.image.load(spritePath).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.isHovered = False
    def checkHover(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        if (mouseX > self.rect.x and mouseX < (self.rect.x + self.width) and
            mouseY > self.rect.y and mouseY < (self.rect.y + self.height)):
            self.isHovered = True
        else:
            self.isHovered = False
    def draw(self):
        display.blit(self.image, (self.rect.x, self.rect.y))
    def update(self):
        self.checkHover()
        self.draw()



class Challenge():
    def __init__(self, gridSize, itemCount, difficulty, nextGameMode):
        self.gridSize = gridSize #X en Y
        self.itemCount = itemCount
        self.difficulty = difficulty
        self.nextGameMode = nextGameMode
        


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spritePlayer
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hasJumped = False #Voorkomt dubbel springen
        self.direction = 0
        self.jumpSpeed = 0
        self.dx = 0
        self.dy = 0
        self.rect.x = -100 #Spawnt de speler buiten beeld
        self.rect.y = -100 #Spawnt de speler buiten beeld
        self.fontCollide = pygame.font.SysFont('Consola.ttf', 45)
        self.hitFinish = False
    def reset(self):
        self.rect.x = controller.playerStartingPosition[X]
        self.rect.y = controller.playerStartingPosition[Y]
        self.hasJumped = False
        self.direction = 0
        self.jumpSpeed = 0
        self.dx = 0
        self.dy = 0
        self.hitFinish = False
    def checkCollision(self):
        for n in range(controller.totalBlocks):
            if (pygame.Rect.colliderect(self.rect, block[n].rect)):
                if (block[n].spriteIndex == FINISH):
                    self.hitFinish = True
                elif (block[n].spriteIndex == RESET):
                    player.reset()
                elif (block[n].spriteIndex == GAME_OVER):
                    controller.resetGame()
                    controller.setGameMode(MAIN_MENU)
                if (self.direction == LEFT): 
                    self.rect.x = block[n].rect.x + BLOCK_WIDTH
                elif (self.direction == RIGHT): 
                    self.rect.x = block[n].rect.x - self.width
                elif (self.direction == UP):
                    self.rect.y = block[n].rect.y + BLOCK_HEIGHT
                elif (self.direction == DOWN):
                    self.rect.y = block[n].rect.y - self.height
        if (self.rect.x < controller.leftBorderRect.x + (controller.gridBorderLeft[X] * BLOCK_WIDTH) and self.direction == LEFT):
            self.rect.x = controller.leftBorderRect.x + (controller.gridBorderLeft[X] * BLOCK_WIDTH)
        elif (self.rect.x > (GRID_WIDTH * BLOCK_WIDTH) - (controller.gridBorderRight[X] * BLOCK_WIDTH) - self.width and self.direction == RIGHT):
            self.rect.x = (GRID_WIDTH * BLOCK_WIDTH) - (controller.gridBorderRight[X] * BLOCK_WIDTH) - self.width
        elif (self.rect.y < controller.topBorderRect.x + (controller.gridBorderTop[Y] * BLOCK_HEIGHT) and self.direction == UP):
            self.rect.y = controller.topBorderRect.x + (controller.gridBorderTop[Y] * BLOCK_HEIGHT)
        elif (self.rect.y > (GRID_HEIGHT * BLOCK_HEIGHT) - (controller.gridBorderBottom[Y] * BLOCK_HEIGHT) - self.height and self.direction == DOWN):
            self.rect.y = (GRID_HEIGHT * BLOCK_HEIGHT) - (controller.gridBorderBottom[Y] * BLOCK_HEIGHT) - self.height
    def draw(self):
        display.blit(self.image, (self.rect.x, self.rect.y))
    def updateTopDown(self):
        if (controller.challengeIndex > 1):
            self.dx = 0
            self.dy = 0
            key = pygame.key.get_pressed()
            if 1 in key: #CPU ontlasten door alleen de loop te doen wanneer daadwerkelijk een toets ingedrukt wordt
                if key[pygame.K_UP]:
                    self.direction = UP
                    self.dy = -SPEED
                elif key[pygame.K_DOWN]:
                    self.direction = DOWN
                    self.dy = SPEED
                elif key[pygame.K_LEFT]:
                    self.direction = LEFT
                    self.dx = -SPEED
                elif key[pygame.K_RIGHT]:
                    self.direction = RIGHT
                    self.dx = SPEED
            self.rect.x += self.dx
            self.rect.y += self.dy
            self.checkCollision()
        self.draw()
    def updatePlatformer(self):
        self.dx = 0
        self.dy = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and (not self.hasJumped):
            self.jumpSpeed = JUMP_SPEED
            self.hasJumped = True
        if key[pygame.K_LEFT]:
            self.dx -= SPEED
            self.direction = -1
        if key[pygame.K_RIGHT]:
            self.dx += SPEED
            self.direction = 1
        self.jumpSpeed += GRAVITY
        if self.jumpSpeed > 10:
            self.jumpSpeed = 10
        self.dy += self.jumpSpeed
        for n in range(controller.totalBlocks):
            if block[n].rect.colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height):
                self.dx = 0
            if block[n].rect.colliderect(self.rect.x, self.rect.y + self.dy, self.width, self.height):
                if self.jumpSpeed < 0:
                    self.dy = block[n].rect.bottom - self.rect.top
                    self.jumpSpeed = 0
                    self.hasJumped = False
                elif self.jumpSpeed >= 0:
                    self.dy = block[n].rect.top - self.rect.bottom
                    self.jumpSpeed = 0
                    self.hasJumped = False
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.dy = 0
        if self.rect.left < 0:
            self.rect.left = 0
            self.dx = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.dx = 0
        self.draw()



class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, spriteIndex):
        super().__init__()
        self.spriteIndex = spriteIndex
        self.image = sprites[self.spriteIndex]
        self.rect = self.image.get_rect(topleft=(x, y))
    def draw(self):
        display.blit(self.image, (self.rect.x, self.rect.y))
    def update(self):
        self.draw()



class Cursor():
    def __init__(self):
        self.currentItemIndex = 1 #Correspondeert met blok
    def setItem(self, direction):
        self.currentItemIndex += direction
        if (self.currentItemIndex < 0):
            self.currentItemIndex = len(items) - 1
        elif (self.currentItemIndex > (len(items) - 1)):
            self.currentItemIndex = 0
    def draw(self): #Voor het tekenen van het huidige item, onderin beeld
        display.blit(sprites[self.currentItemIndex], (428, 474))



class Item(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.index = 0
        self.image = sprites[self.index]
        self.rect = self.image.get_rect()
        self.isVisible = False
    def spawn(self, x, y, index):
        self.rect.x = x
        self.rect.y = y
        self.index = index
        self.image = sprites[self.index]
        self.isVisible = True
    def setVisible(self, visible):
        self.isVisible = visible
    def draw(self):
        if (self.isVisible):
            display.blit(self.image, (self.rect.x, self.rect.y))




#Objecten aanmaken
controller = Controller()

Menu = GM_MainMenu()
Challenges = GM_ChallengesMenu()
Instructions = GM_Instructions()
Bibber = GM_Bibber()
AssignMovement = GM_AssignMovement()
GridEditor = GM_GridEditor()
LevelEditor = GM_LevelEditor()
Ending = GM_Ending()

buttonPlay = Button("assets/sprites/buttonPlay.png", 375, 250)
buttonBackToMenu = Button("assets/sprites/buttonBackToMenu.png", 20, 470)
buttonGridEditor = Button("assets/sprites/buttonGridEditor.png", 240, 470)
buttonLevelEditor = Button("assets/sprites/buttonLevelEditor.png", 720, 470)
buttonInstructions = Button("assets/sprites/buttonInstructions.png", 615, 470)
buttonSaveAndExit_GE = Button("assets/sprites/buttonSaveAndExit.png", 825, 470) #Grid Editor
buttonSaveAndExit_LE = Button("assets/sprites/buttonSaveAndExit.png", 825, 470) #Level Editor
buttonSaveAndExit_CE = Button("assets/sprites/buttonSaveAndExit.png", 825, 470) #Code Editor
buttonItemPrevious = Button("assets/sprites/buttonItemPrevious.png", 372, 481)
buttonItemNext = Button("assets/sprites/buttonItemNext.png", 497, 481)
buttonBack = Button("assets/sprites/buttonBack.png", 90, 470)
buttonNext = Button("assets/sprites/buttonNext.png", 825, 470)
buttonIncreaseGridX = Button("assets/sprites/buttonIncrease.png", 300, 470)
buttonDecreaseGridX = Button("assets/sprites/buttonDecrease.png", 200, 470)
buttonIncreaseGridY = Button("assets/sprites/buttonIncrease.png", 650, 470)
buttonDecreaseGridY = Button("assets/sprites/buttonDecrease.png", 550, 470)


player = Player()
cursor = Cursor()

buttonNextMovement = []
buttonPreviousMovement = []
buttonChallenge = []
challenge = []
block = []
item = []

challenge.append(Challenge([3, 2], #De afmetingen van het speelvlak
                           [GRID_WIDTH * GRID_HEIGHT, 0, 0, 0, 0, 0], #Het maximaal aantal items dat beschikbaar is, zie de items[] array
                           1, #Moeilijkheidsgraad (1-5)
                           BIBBER)) #De volgende GameMode na GRID_EDITOR
challenge.append(Challenge([4, 3], 
                           [GRID_WIDTH * GRID_HEIGHT, 0, 0, 0, 0, 1],
                           1,
                           LEVEL_EDITOR))
challenge.append(Challenge([5, 4], 
                           [GRID_WIDTH * GRID_HEIGHT, 0, 0, 0, 0, 1],
                           5,
                           ASSIGN_MOVEMENT))
challenge.append(Challenge([7, 3], 
                           [GRID_WIDTH * GRID_HEIGHT, 0, 1, 0, 0, 1],
                           2,
                           LEVEL_EDITOR))
challenge.append(Challenge([10, 5], 
                           [GRID_WIDTH * GRID_HEIGHT, 0, 1, 1, 0, 1],
                           2,
                           LEVEL_EDITOR))
challenge.append(Challenge([5, 5], 
                           [GRID_WIDTH * GRID_HEIGHT, 0, 1, 0, 1, 1],
                           2,
                           LEVEL_EDITOR))
challenge.append(Challenge([3, 7], 
                           [GRID_WIDTH * GRID_HEIGHT, 2, 1, 1, 0, 1],
                           3,
                           LEVEL_EDITOR))
challenge.append(Challenge([7, 3], 
                           [GRID_WIDTH * GRID_HEIGHT, 5, 1, 0, 0, 1],
                           3,
                           LEVEL_EDITOR))
challenge.append(Challenge([10, 10], 
                           [GRID_WIDTH * GRID_HEIGHT, 5, 1, 1, 1, 1],
                           4,
                           LEVEL_EDITOR))
challenge.append(Challenge([20, 10], 
                           [GRID_WIDTH * GRID_HEIGHT, 99, 1, 10, 10, 1],
                           1,
                           LEVEL_EDITOR))

multiplierX = 0
changeMultiplier = True
for n in range(len(challenge)):
    if (n > 4):
        buttonY = 320
        if (changeMultiplier):
            multiplierX = 0
            changeMultiplier = False
    else:
        buttonY = 200
    buttonChallenge.append(Button("assets/sprites/buttonChallenge.png", 20 + (multiplierX * 175), buttonY))
    multiplierX += 1

for n in range(GRID_WIDTH * GRID_HEIGHT):
    item.append(Item())

for n in range(len(AssignMovement.movements)):
    buttonPreviousMovement.append(Button("assets/sprites/buttonPreviousSmall.png", 250, 35 + (n * 90)))
    buttonNextMovement.append(Button("assets/sprites/buttonNextSmall.png", 575, 35 + (n * 90)))




#Hoofdfunctie
async def main():
    #Muziek
    pygame.mixer.music.load("assets/sound/main_loop.mp3") #Inladen
    pygame.mixer.music.set_volume(0.5) #Volume verlagen
    pygame.mixer.music.play(-1) #Spelen op loop

    controller.resetGame()

    #Main loop
    while 1:
        if (controller.isGameFinished):
            break

        controller.update()

        pygame.display.flip()
        clock.tick(FPS)

        await asyncio.sleep(0)




#Game runnen
asyncio.run(main())