import pygame
import os
import sys
from ColorDictionary import ColourDictionary as c # colors
pygame.init() # all init
### Game Constants
MAZE_X = 50
MAZE_Y = 50
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TILE_SIZE = 50
TPS = 30 # ticks per second
SCREEN = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))  # Windowed (safer/ superior)

###  fonts
SELECTION_FONT = 'Londrina Solid'

# setup font dictionary
if getattr(sys, 'frozen', False):  # Running as an .exe
    BASE_PATH = sys._MEIPASS
else:  # Running as a .py script
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_PATH, 'fonts', 'LondrinaSolid-Regular.otf')

FONT_DICTIONARY = {"tileFont":pygame.font.SysFont('Calibri', 25, True, False),
                  "playerStringFont": pygame.font.Font(FONT_PATH, 30),
                    "ctrlFont": pygame.font.SysFont('Courier New', 20, True, False),
                    "scoreFont": pygame.font.SysFont('Londrina', 60, True, False),
                    "playerScore" : pygame.font.Font(FONT_PATH, 70),
                    "cFont" : pygame.font.SysFont('Courier New', 36),
                    "iFont" : pygame.font.SysFont('Courier New', 20),
                    "titleFont" : pygame.font.SysFont('Arial', 60),
                  }

BACKGROUND_COLOR = c.geT('SOFT_WHITE')

SELECTION_BACKGROUND = c.geT('SOFT_WHITE')

MONO_FONT = 'Courier New'

