from config import *
import pygame

# Size as a percentage of the display size
toolbar_size = .07
scale_x, scale_y = BOARD_SIZE

def drawToolbar(toolbar_surface):
    pass

def drawGame(board, game_surface):
    board_surface = pygame.Surface(BOARD_SIZE)

    for k, y in enumerate(board):
        for l, x in enumerate(y):
            board_surface.set_at((k, l), (x*255, x*255, x*255))

    # Scale board_surface to fit the window
    board_surface = pygame.transform.scale(board_surface, game_surface.get_size())
    game_surface.blit(board_surface, (0,0))




def drawScreen(board, screen):
    screen_width, screen_height = pygame.display.get_surface().get_size()
    toolbar_height = max(round(screen_height * toolbar_size), MIN_TB_HEIGHT)
    toolbar_surface = pygame.Surface((screen_width, toolbar_height))
    game_surface = pygame.Surface((screen_width, screen_height - toolbar_height))

    drawToolbar(toolbar_surface)
    drawGame(board, game_surface)

    screen.blit(toolbar_surface, (0,0))
    screen.blit(game_surface, (0,toolbar_height))


def printGame(board):
    for y in board:
        for x in y:
            print("#" if x == 1 else ".", end=" ")
        print()
    print()