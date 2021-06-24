from config import *
import pygame
from graphics import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)

paused = True

def main():
    board = [[0 for x in range(BOARD_SIZE[0])] for y in range(BOARD_SIZE[1])]
    back = board.copy() # we have two boards so we can update without destroying the old one

    board[0][1] = 1
    board[1][2] = 1
    board[2][0] = 1
    board[2][1] = 1
    board[2][2] = 1

    for i in range(1):
        drawScreen(board, screen)
        update(board, back)

        #pygame.time.wait(1000)



def countNeighbors(board, x, y):
    print(x, y)
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
                aliveNeighbors += board[i][j]
    print("{} live neighbor(s)".format(aliveNeighbors))
    return aliveNeighbors

def update(board, back):
    for j in range(BOARD_SIZE[1]):
        for i in range(BOARD_SIZE[0]):
            neighbors = countNeighbors(board, i, j)
            if neighbors < 2 or neighbors >= 4: # under- or over-population
                back[j][i] = 0 # update the back board
            elif neighbors == 3:
                back[j][i] = 1
            else:
                back[j][i] = board[j][i]

    board = back.copy() # update board to the new (back) board

main()
