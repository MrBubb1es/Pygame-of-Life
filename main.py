from config import *
from graphics import *
from math import floor
import pygame

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)
clock = pygame.time.Clock()

paused = True

def newBoard():
    return [[0 for x in range(BOARD_SIZE[0])] for y in range(BOARD_SIZE[1])]

def main():
    board = newBoard()

    board[0][1] = 1
    board[1][2] = 1
    board[2][0] = 1
    board[2][1] = 1
    board[2][2] = 1

    running = True
    while running:
        drawScreen(board, screen)
        board = update(board)

        drawScreen(board, screen)
        clock.tick(HZ)

        running = not checkBlank()

# Check if the board is blank
def checkBlank(board):
    blank = True

    for y in board:
        for x in y:
            if x == 1:
                blank = False

    return blank

def countNeighbors(board, x, y):
    aliveNeighbors = 0
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if i < 0 or i >= BOARD_SIZE[0]:
                print("i < 0 or i >= BOARD_SIZE[0] : i,j = ({}, {}), x,y = ({}, {}), BS[0],BS[1] = ({}, {})".format(i,j,x,y,BOARD_SIZE[0],BOARD_SIZE[1]))
                continue
            elif j < 0 or j >= BOARD_SIZE[1]:
                print("j < 0 or j >= BOARD_SIZE[1] : i,j = ({}, {}), x,y = ({}, {}), BS[0],BS[1] = ({}, {})".format(i,j,x,y,BOARD_SIZE[0],BOARD_SIZE[1]))
                continue
            elif i == x and y == j:
                print("i == x and j == y : i,j = ({}, {}), x,y = ({}, {}), BS[0],BS[1] = ({}, {})".format(i,j,x,y,BOARD_SIZE[0],BOARD_SIZE[1]))
                continue
            else:
                print("Neighbor is {} : i,j = ({}, {}), x,y = ({}, {}), BS[0],BS[1] = ({}, {}) board = {}".format(("alive" if board[i][j] == 1 else "dead"),i,j,x,y,BOARD_SIZE[0],BOARD_SIZE[1], board))
                aliveNeighbors += board[j][i]
    print("{} live neighbor(s)".format(aliveNeighbors))
    return aliveNeighbors

def update(board):
    new = newBoard()
    for j in range(BOARD_SIZE[1]):
        for i in range(BOARD_SIZE[0]):
            neighbors = countNeighbors(board, i, j)
            if neighbors < 2 or neighbors >= 4: # under- or over-population
                new[j][i] = 0 # update the back board
                pass
            elif neighbors == 3:
                new[j][i] = 1
                pass
            else:
                new[j][i] = board[j][i]
                pass

    return new # update board to the new (back) board

main()
