import pygame, random
import concurrent.futures
import numpy as np
from numba import jit

from config import *
from graphics import *
from math import floor
from pygame.locals import *

pygame.init()

screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(screen_size, RESIZABLE)
clock = pygame.time.Clock()

paused = True

def randomizeBoard(board):
    for row in board:
        for x in range(len(row)):
            row[x] = random.randint(0,1)

    return board


def newBoard():
    return np.array([[0 for _ in range(BOARD_SIZE[0])] for _ in range(BOARD_SIZE[1])])


def main():
    board = randomizeBoard(newBoard())
    back = newBoard()

    running = True
    while running:
        drawScreen(board, screen)
        back = update(board, back)
        board, back = back, board
        #clock.tick(HZ)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == VIDEORESIZE:
                screen_size = (event.w, event.h)

    pygame.quit()

@jit(nopython=True)
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

@jit(nopython=True)
def updateRow(board, back, j):
    for i in range(BOARD_SIZE[0]):
        neighbors = countNeighbors(board, i, j)
        if neighbors < 2 or neighbors >= 4: # under- or over-population
            back[j][i] = 0 # update the back board
        elif neighbors == 3:
            back[j][i] = 1
        else:
            back[j][i] = board[j][i]

    return (j, back[j])

def update(board, back):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(updateRow, board, back, j) for j in range(BOARD_SIZE[1])]

        for f in concurrent.futures.as_completed(results):
            result = f.result()
            back[result[0]] = result[1]

    return back


main()
