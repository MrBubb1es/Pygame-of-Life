import pygame, random
import concurrent.futures

from config import *
from graphics import *
from math import floor
from pygame.locals import *

pygame.init()

screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(screen_size, RESIZABLE)
clock = pygame.time.Clock()

paused = True

def newBoard():
    return [[random.randint(0,1) for x in range(BOARD_SIZE[0])] for y in range(BOARD_SIZE[1])]

def main():
    board = newBoard()

    running = True
    while running:
        drawScreen(board, screen)
        board = update(board)
        clock.tick(HZ)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == VIDEORESIZE:
                screen_size = (event.w, event.h)


    pygame.quit()

def countNeighbors(board, x, y):
    aliveNeighbors = 0
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if i < 0 or i >= BOARD_SIZE[0]:
                continue
            elif j < 0 or j >= BOARD_SIZE[1]:
                continue
            elif i == x and y == j:
                continue
            else:
                aliveNeighbors += board[j][i]
    return aliveNeighbors


def updateRow(board, y):
    for i in range(BOARD_SIZE[0]):
        neighbors = countNeighbors(board, i, j)
        if neighbors < 2 or neighbors >= 4: # under- or over-population
            new[j][i] = 0 # update the back board
        elif neighbors == 3:
            new[j][i] = 1
        else:
            new[j][i] = board[j][i]

def update(board):
    new = newBoard()

    with concurrent.futures.ThreadPoolExecutable() as executor:
        executor.map(updateRow, board, args=[board, ])

    return new

main()
