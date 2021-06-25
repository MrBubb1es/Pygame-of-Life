from config import *
import pygame, math

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

# Reusing this from my sprite editor app
def hueToRGB(hue):
    # 0 <= hue < 60: R = 255, B = 0, Solve for G
    # G starts at 0
    if (0 <= hue) and (hue < 60):
        R = 255
        B = 0
        G = round((1 - (60 - hue)/60) * 255)
    # 60 <= hue < 120: G = 255, B = 0, Solve for R
    # R starts at 255
    elif (60 <= hue) and (hue < 120):
        R = round((60 - (hue - 60))/60 * 255)
        B = 0
        G = 255
    # 120 <= hue < 180: G = 255, R = 0, Solve for B
    # B starts at 0
    elif (120 <= hue) and (hue < 180):
        R = 0
        B = round((1 - (60 - (hue - 120))/60) * 255)
        G = 255
    # 180 <= hue < 240: B = 255, R = 0, Solve for G
    # G starts at 255
    elif (180 <= hue) and (hue < 240):
        R = 0
        B = 255
        G = round((60 - (hue - 180))/60 * 255)
    # 240 <= hue < 300: B = 255, G = 0, Solve for R
    # R starts at 0
    elif (240 <= hue) and (hue < 300):
        R = round((1 - (60 - (hue - 240))/60) * 255)
        B = 255
        G = 0
    # 300 <= hue < 360: R = 255, G = 0, Solve for B
    # B starts at 255
    elif (300 <= hue) and (hue < 360):
        R = 255
        B = round((60 - (hue - 300))/60 * 255)
        G = 0
    else:
        print("Hue {} not within acceptable bounds of 0 to 360".format(hue))
        R = 255
        G = 255
        B = 255

    return (R,G,B)

def drawScreen(board, screen):
    screen_width, screen_height = pygame.display.get_surface().get_size()

    """
    toolbar_height = max(round(screen_height * toolbar_size), MIN_TB_HEIGHT)
    toolbar_surface = pygame.Surface((screen_width, toolbar_height))
    """

    #drawToolbar(toolbar_surface)
    #drawGame(board, game_surface)

    board_surface = pygame.Surface(BOARD_SIZE)

    for k, y in enumerate(board):
        for l, x in enumerate(y):
            if (board[k][l] == 1):
                color = hueToRGB(k / BOARD_SIZE[0] * 360)
            else:
                color = (0,0,0)
            board_surface.set_at((k,l), color)


    # Scale board_surface to fit the window
    board_surface = pygame.transform.scale(board_surface, (screen_width, screen_height))

    #screen.blit(toolbar_surface, (0,0))
    screen.blit(board_surface, (0,0))
    pygame.display.update()
