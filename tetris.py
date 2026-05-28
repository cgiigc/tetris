import pygame
import sys
from pygame.locals import *

import random
import math

import copy

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

tiles = ["redtile.png", "orangetile.png", "yellowtile.png", "greentile.png", "darkbluetile.png", "lightbluetile.png", "purpletile.png"]

pieces = [[[0,0,0],[0,1,1],[1,1,0],[1,1]], [[0,0,0],[2,2,2],[0,0,2],[1,1]], [[0,0,0,0],[0,3,3,0],[0,3,3,0],[1.5, 1.5]], [[0,0,0],[4,4,0],[0,4,4],[1,1]], [[0,0,0],[5,5,5],[5,0,0],[1,1]], [[0,0,0,0],[0,0,0,0],[6,6,6,6],[0,0,0,0],[1.5,1.5]], [[0,0,0],[7,7,7],[0,7,0],[1,1]]]
wallKicks = [[[0,0],[+1,0],[+1,-1],[0,+2],[+1,+2]],[[0,0],[+1,0],[+1,-1],[0,+2],[+1,+2]],[],[[0,0],[+1,0],[+1,-1],[0,+2],[+1,+2]],[[0,0],[+1,0],[+1,-1],[0,+2],[+1,+2]],[[[0,0],[+2,0],[-1,0],[+2,+1],[-1,-2]],[[0,0],[+1,0],[-2,0],[+1,-2],[-2,+1]]],[[0,0],[+1,0],[+1,-1],[0,+2],[+1,+2]]]

rotated = False

leftmostTileArray = []
rightmostTileArray = []
bottommostTileArray = []
topmostTileArray = []

# 10 board tiles, 1 board tile = 34x34, so multiply by 10 = 340
# + 11, to account for the gaps between each tile, gives us 351

# The process is the same for the height, 20 board tiles, 1 board tile = 34x34, so multiply by 20 = 680
# + 21, to account for the gaps between each tile, gives us 701

# Divide both these values by 2, so we can centre it

boardSpawnX = 148.5
boardSpawnY = 313.5

DISPLAYSURF = pygame.display.set_mode((0, 0))
DISPLAYSURF.fill((50, 50, 50))
pygame.display.set_caption("Tetris")

class Board(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("boardtile.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.pieceIndex = 0
        self.permState = [[0 for _ in range(10)] for _ in range(25)]
        self.currentPiece = []
        self.piecePos = []
        self.rotatedTiles = []
        self.topmostTilePermArray = [0 for _ in range(10)]
        self.rotationCount = 0

    def renderPiece(self):
        for i in range(len(self.currentPiece)-1):
            for j in range(len(self.currentPiece[0])):
                if self.currentPiece[i][j] > 0:
                    self.permState[self.piecePos[1]+i][self.piecePos[0]+j] = self.currentPiece[i][j]

        self.topmostTilePermArray = topmostTilePerm()

    def draw(self, surface):
        for w in range(10):
            for h in range(20):
                self.rect = self.image.get_rect()
                self.rect.center = (DISPLAYSURF.get_width()/2-boardSpawnX+33*w, DISPLAYSURF.get_height()/2-boardSpawnY+33*h)
                surface.blit(self.image, self.rect)

class Tile(pygame.sprite.Sprite):
    def __init__(self, tileValue):
        super().__init__()
        self.image = pygame.image.load(tiles[tileValue-1]).convert()
        self.rect = self.image.get_rect()
    
    def draw(self, surface, j, i):
        self.rect.center = (DISPLAYSURF.get_width()/2-boardSpawnX+33*i, DISPLAYSURF.get_height()/2+boardSpawnY-33*j)
        surface.blit(self.image, self.rect)

def rotate(x, y, pivotValues):
    rotated = [int((round((x-pivotValues[0])*math.cos(math.radians(-90))-(y-pivotValues[1])*math.sin(math.radians(-90))+pivotValues[0], 10))), int((round((x-pivotValues[0])*math.sin(math.radians(-90))+(y-pivotValues[1])*math.cos(math.radians(-90)), 10))+pivotValues[1])]
    
    if not [x, y] == pivotValues and not [x, y] in board.rotatedTiles and not board.pieceIndex == 2:

        if board.currentPiece[rotated[1]][rotated[0]] > 0:
            rotate(rotated[0], rotated[1], pivotValues)
        
        board.currentPiece[y][x] = 0

        board.currentPiece[rotated[1]][rotated[0]] = board.pieceIndex+1
        board.rotatedTiles.append([rotated[0], rotated[1]])

def leftmostTile():
    array = []
    leftmostPiece = 999

    for i in range(len(board.currentPiece)-1):
        for j in range(len(board.currentPiece[i])):
            if board.currentPiece[i][j] > 0:
                leftmostPiece = j
                break
        array.append(leftmostPiece)
        leftmostPiece = 999

    return array

def rightmostTile():
    array = []
    rightmostPiece = -999

    for i in range(len(board.currentPiece)-1):
        for j in range(len(board.currentPiece[i])):
            if board.currentPiece[i][j] > 0:
                rightmostPiece = j
        array.append(rightmostPiece)
        rightmostPiece = -999

    return array

def bottommostTile():
    array = []
    bottommostPiece = 999

    for j in range(len(board.currentPiece[0])):
        for i in range(len(board.currentPiece)-1):
            if board.currentPiece[i][j] > 0:
                bottommostPiece = i
                break
            
        array.append(bottommostPiece)
        bottommostPiece = 999

    return array

def topmostTile():
    array = []
    topmostPiece = -999

    for j in range(len(board.currentPiece[0])):
        for i in range(len(board.currentPiece)-1):
            if board.currentPiece[i][j] > 0:
                topmostPiece = i
            
        array.append(topmostPiece)
        topmostPiece = -999

    return array

def topmostTilePerm():
    array = []

    for j in range(10):

        topmostPiece = -999

        for i in range(25):
            if board.permState[i][j] > 0:
                topmostPiece = i

        array.append(topmostPiece)

    return array

def checkCollision():
    canDrop = True
                
    # Check if the piece is already at the bottom floor
    if board.piecePos[1] + min(bottommostTileArray) <= 0:
        canDrop = False
    else:
        # Check for collision with tiles already on the board
        # We check every active tile in the current piece
        for i in range(len(board.currentPiece) - 1):
            for j in range(len(board.currentPiece[i])):
                if board.currentPiece[i][j] > 0:
                    boardX = board.piecePos[0] + j
                    # Check the tile exactly below this one (-1)
                    boardY = board.piecePos[1] + i - 1
                    
                    if boardY < 25 and board.permState[boardY][boardX] > 0:
                        canDrop = False
                        break
            if not canDrop:
                break
    
    return canDrop

board = Board()
currentTile = Tile(0)
permTile = Tile(0)

tileSelected = False

gravity = pygame.USEREVENT+1

deltaTime = 0
debounce = False
debounceHD = False

lastDtMove = 0
lastDtRotate = 0

gameOver = False
count = 0

highest = 20
linesCleared = 0

font = pygame.font.SysFont('Arial',100)

pygame.time.set_timer(gravity, 1000)

while True:
    if gameOver == False:
        for event in pygame.event.get():
            if event.type == gravity:
                if board.piecePos[1] + min(bottommostTileArray) > 0:
                    canDrop = checkCollision()

                    if canDrop:
                        board.piecePos[1] = board.piecePos[1]-1
                        
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill((50, 50, 50))

        board.draw(DISPLAYSURF)

        if tileSelected == False:
            randIndex = random.randint(0, len(tiles)-1)
            tempArray = pieces[randIndex]
            board.currentPiece = copy.deepcopy(tempArray)
            board.pieceIndex = randIndex
            board.piecePos = [len(board.currentPiece)-math.floor(len(board.currentPiece)%4)-1, 21-math.floor(len(board.currentPiece)%4)]

            currentTile = Tile(randIndex+1)
            tileSelected = True

            leftmostTileArray, rightmostTileArray, bottommostTileArray, topmostTileArray = leftmostTile(), rightmostTile(), bottommostTile(), topmostTile()

        keys = pygame.key.get_pressed()
        
        if keys[K_UP] and not rotated:
            rotated = True
            for i in range(len(board.currentPiece)-1):
                for j in range(len(board.currentPiece[i])):
                    value = board.currentPiece[i][j]
                    
                    if value > 0:
                        pivotValues = board.currentPiece[len(board.currentPiece)-1]

                        rotate(j, i, pivotValues)

            collision = False

            for i in range(len(board.currentPiece) - 1):
                for j in range(len(board.currentPiece[i])):
                    if board.currentPiece[i][j] > 0:
                        boardX = board.piecePos[0] + j
                        boardY = board.piecePos[1] + i

                        if boardX > 9:
                            break
                        
                        if boardY < 25 and board.permState[boardY][boardX] > 0:
                            collision = True
                            break
                    
            while collision:
                collision = False
                board.piecePos[1] = board.piecePos[1]+1
                for i in range(len(board.currentPiece) - 1):
                    for j in range(len(board.currentPiece[i])):
                        if board.currentPiece[i][j] > 0:
                            boardX = board.piecePos[0] + j
                            boardY = board.piecePos[1] + i
                            
                            if boardY < 25 and board.permState[boardY][boardX] > 0:
                                collision = True
                                break
                        
            leftmostTileArray, rightmostTileArray, bottommostTileArray, topmostTileArray = leftmostTile(), rightmostTile(), bottommostTile(), topmostTile()

            lastDtRotate = 0

            if board.piecePos[0] + min(leftmostTileArray) < 0:
                board.piecePos[0] = 0
            elif board.piecePos[0] + max(rightmostTileArray) > 9:
                board.piecePos[0] = 9 - len(board.currentPiece[0])
            
            if board.piecePos[1] + min(bottommostTileArray) < 0:
                board.piecePos[1] = 0 + min(bottommostTileArray)
            
        elif not keys[K_UP]:
            rotated = False

            board.rotatedTiles = []

        if keys[K_LEFT]:
            if (deltaTime < 0.02 or (deltaTime > 0.15 and lastDtMove > 0.025)) and board.piecePos[0] + min(leftmostTileArray) > 0:
                lastDtMove = 0
                if not keys[K_RIGHT]:
                    board.piecePos = [board.piecePos[0]-1, board.piecePos[1]]
                    for i in range(len(board.currentPiece)-1):
                        for j in range(len(board.currentPiece[0])):
                            if board.piecePos[1] <= 25:
                                if board.currentPiece[i][j] > 0 and board.permState[board.piecePos[1]+i][board.piecePos[0]+j] > 0:
                                    board.piecePos = [board.piecePos[0]+1, board.piecePos[1]]
        if keys[K_RIGHT]:
            if (deltaTime < 0.02 or (deltaTime > 0.15 and lastDtMove > 0.025)) and board.piecePos[0] + max(rightmostTileArray) < 9:
                lastDtMove = 0
                if not keys[K_LEFT]:
                    board.piecePos = [board.piecePos[0]+1, board.piecePos[1]]
                    for i in range(len(board.currentPiece)-1):
                        for j in range(len(board.currentPiece[0])):
                            if board.piecePos[1] <= 25:
                                if board.currentPiece[i][j] > 0 and board.permState[board.piecePos[1]+i][board.piecePos[0]+j] > 0:
                                    board.piecePos = [board.piecePos[0]-1, board.piecePos[1]]
        if keys[K_DOWN]:
            if not debounce and board.piecePos[1] + min(bottommostTileArray) > 0:
                canDrop = checkCollision()

                if canDrop:
                    board.piecePos = [board.piecePos[0], board.piecePos[1]-1]

                pygame.time.set_timer(gravity, 100)
                debounce = True
        elif debounce:
            pygame.time.set_timer(gravity, 1000)
            debounce = False

        if (not keys[K_LEFT]) and (not keys[K_RIGHT]):
            deltaTime = 0

        if keys[K_SPACE]:
            if not debounceHD:
                debounceHD = True
                
                # Keep moving the piece down until it hits something
                while True:
                    canDrop = checkCollision()

                    if canDrop:
                        board.piecePos[1] -= 1
                    else:
                        break # Hit the floor or a piece

                # Lock the piece and reset
                board.renderPiece()
                tileSelected = False
        else:
            debounceHD = False

        if tileSelected:
            for i in range(len(board.currentPiece)-1):
                for j in range(len(board.currentPiece[i])):
                    if board.currentPiece[i][j] == 0:
                        continue

                    currentTile.draw(DISPLAYSURF, i+board.piecePos[1], j+board.piecePos[0])

        for i in range(10):
            for j in range(25):
                if board.permState[j][i] == 0:
                    continue

                permTile = Tile(board.permState[j][i])
                permTile.draw(DISPLAYSURF, j, i)

        deltaTime = deltaTime + FramePerSec.get_time()/1000
        lastDtMove = lastDtMove + FramePerSec.get_time()/1000
        lastDtRotate = lastDtRotate + FramePerSec.get_time()/1000

        if max(board.topmostTilePermArray) > 20:
            gameOver = True

        text = font.render(str(max(40-linesCleared, 0)),True,(255,255,255))
        textrect = text.get_rect()

        if linesCleared > 39:
            gameOver = True

        textrect.center = (DISPLAYSURF.get_width()/2, DISPLAYSURF.get_height()/2+375)

        if highest > board.piecePos[1]:
            count = 0
            lastDtRotate = 0
            lastDtMove = 0

        canDrop = checkCollision()

        if not canDrop:
            if lastDtMove > 0.5 or lastDtRotate > 0.5 or count > 14:
                board.renderPiece()
                tileSelected = False

        lines = []

        for i in range(len(board.permState)):
            if min(board.permState[i]) > 0:
                lines.append(i)

        for row in reversed(lines):
            del board.permState[row]
            board.permState.append([0 for _ in range(10)])
            linesCleared += 1

        highest = board.piecePos[1]
    else:
        if max(board.topmostTilePermArray) > 20:
            image = pygame.image.load("gameover.png").convert_alpha()
            rectImage = image.get_rect()
            image = pygame.transform.scale(image, (1000, 1000))
            
            rectImage.center = (DISPLAYSURF.get_width()/2-500, DISPLAYSURF.get_height()/2-500)
            DISPLAYSURF.blit(image, rectImage)
    
            deltaTime = deltaTime + FramePerSec.get_time()/1000

            if deltaTime > 3:
                break
        else:
            image = pygame.image.load("gamewin.png").convert_alpha()
            rectImage = image.get_rect()
            image = pygame.transform.scale(image, (1000, 1000))
            
            rectImage.center = (DISPLAYSURF.get_width()/2-500, DISPLAYSURF.get_height()/2-500)
            DISPLAYSURF.blit(image, rectImage)
    
            deltaTime = deltaTime + FramePerSec.get_time()/1000

            if deltaTime > 3:
                break

    DISPLAYSURF.blit(text, textrect)
    
    pygame.display.update()
    FramePerSec.tick(FPS)