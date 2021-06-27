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

def randomizeBoard(board):
    for row in board:
        for x in range(len(row)):
            row[x] = random.randint(0,1)

    return board

def newBoard(val):
    return np.array([[val for _ in range(BOARD_SIZE[0])] for _ in range(BOARD_SIZE[1])])

def main():
    board = randomizeBoard(newBoard(0))
    back = newBoard(0)
    screen_size = pygame.display.get_surface().get_size()
    paused = True

    running = True
    while running:
        drawScreen(board, screen)

        if not paused:
            back = update(board, back)
            board, back = back, board

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == VIDEORESIZE:
                screen_size = (event.w, event.h)

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    paused = not paused

        mouse_state = pygame.mouse.get_pressed()
        # If left mouse clicked then fill the cell where the mouse is
        if mouse_state[0]:
            # If shift is held
            if pygame.key.get_mods() & KMOD_SHIFT:
                # Reset board
                board = newBoard(1)

            # Clear the cell where the mouse is
            else:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Clamp mouse
                mouse_x = max(min(mouse_x, screen_size[0]), 0)
                mouse_y = max(min(mouse_y, screen_size[1]), 0)
                board[floor(mouse_x / screen_size[0] * BOARD_SIZE[0])][floor(mouse_y / screen_size[1] * BOARD_SIZE[1])] = 1

        # If right mouse clicked
        if mouse_state[2]:
            # If shift is held
            if pygame.key.get_mods() & KMOD_SHIFT:
                # Reset board
                board = newBoard(0)

            # Clear the cell where the mouse is
            else:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Clamp mouse
                mouse_x = max(min(mouse_x, screen_size[0]), 0)
                mouse_y = max(min(mouse_y, screen_size[1]), 0)
                board[floor(mouse_x / screen_size[0] * BOARD_SIZE[0])][floor(mouse_y / screen_size[1] * BOARD_SIZE[1])] = 0

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
