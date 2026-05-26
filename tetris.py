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
        self.permState = [[0 for _ in range(10)] for _ in range(20)]
        self.currentPiece = []
        self.piecePos = []
        self.rotatedTiles = []
        self.heights = [0 for _ in range(10)]

    def renderPiece(self):
        for i in range(len(self.currentPiece)-1):
            for j in range(len(self.currentPiece[0])):
                if self.currentPiece[i][j] > 0:
                    self.permState[self.piecePos[1]+i][self.piecePos[0]+j] = self.currentPiece[i][j]
                if i == 0:
                    self.heights[self.piecePos[0]+j] = self.heights[self.piecePos[0]+min(j, rightmostTileArray[j])] + topmostTileArray[j] + 1

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

    print(rotated)
    
    if not [x, y] == pivotValues and not [x, y] in board.rotatedTiles and not board.pieceIndex == 2:

        if board.currentPiece[rotated[1]][rotated[0]] > 0:
            print(board.currentPiece)

            print(rotated[0], rotated[1], board.currentPiece)
            print("Yes")
            rotate(rotated[0], rotated[1], pivotValues)
        
        board.currentPiece[y][x] = 0

        board.currentPiece[rotated[1]][rotated[0]] = board.pieceIndex+1
        board.rotatedTiles.append([rotated[0], rotated[1]])
        print(board.currentPiece)

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

board = Board()
currentTile = Tile(0)
permTile = Tile(0)

tileSelected = False

gravity = pygame.USEREVENT+1

deltaTime = 0
debounce = False
debounceHD = False

lastDtMove = 0

pygame.time.set_timer(gravity, 1000)

while True:
    for event in pygame.event.get():
        if event.type == gravity:
            if board.piecePos[1] + min(bottommostTileArray) > 0:
                board.piecePos[1] = board.piecePos[1]-1
                print(bottommostTileArray)
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

                print("VALUE:", value)
                
                if value > 0:
                    pivotValues = board.currentPiece[len(board.currentPiece)-1]

                    rotate(j, i, pivotValues)
                    
        leftmostTileArray, rightmostTileArray, bottommostTileArray, topmostTileArray = leftmostTile(), rightmostTile(), bottommostTile(), topmostTile()

        if board.piecePos[0] + min(leftmostTileArray) < 0:
            board.piecePos[0] = 0
        elif board.piecePos[0] + max(rightmostTileArray) > 9:
            board.piecePos[0] = 10 - len(board.currentPiece[0])
        
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
    if keys[K_RIGHT]:
        if (deltaTime < 0.02 or (deltaTime > 0.15 and lastDtMove > 0.025)) and board.piecePos[0] + max(rightmostTileArray) < 9:
            lastDtMove = 0
            if not keys[K_LEFT]:
                board.piecePos = [board.piecePos[0]+1, board.piecePos[1]]
    if keys[K_DOWN]:
        if not debounce and board.piecePos[1] + min(bottommostTileArray) > 0:
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
            print(board.heights[board.piecePos[0]+min(leftmostTileArray):board.piecePos[0]+max(rightmostTileArray)+1], "heights")
            board.piecePos[1] = 0 - min(bottommostTileArray) + max(board.heights[board.piecePos[0]+min(leftmostTileArray):board.piecePos[0]+max(rightmostTileArray)+1])
            board.renderPiece()

            debounceHD = True

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
        for j in range(20):
            if board.permState[j][i] == 0:
                continue

            permTile = Tile(board.permState[j][i])
            permTile.draw(DISPLAYSURF, j, i)

    deltaTime = deltaTime + FramePerSec.get_time()/1000
    lastDtMove = lastDtMove + FramePerSec.get_time()/1000
    
    pygame.display.update()
    FramePerSec.tick(FPS)