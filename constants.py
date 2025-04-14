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

TITLE_TEXT = FONT_DICTIONARY["titleFont"].render('FLANKI', True, (0, 0, 0))  # Render the title text
BACKGROUND_COLOR = c.geT('SOFT_WHITE')

LOGO_PNG = pygame.image.load(os.path.join(BASE_PATH, "Assets", "logo.png")).convert_alpha()
LOGO_PNG = pygame.transform.scale(LOGO_PNG, (LOGO_PNG.get_size()[0]//15, LOGO_PNG.get_size()[1]//15))

ORIGINAL_TANK_IMAGE = pygame.image.load(os.path.join(BASE_PATH, './Assets/tank_menu_logo.png')).convert_alpha()
ORIGINAL_TANK_IMAGE = pygame.transform.scale(ORIGINAL_TANK_IMAGE, (ORIGINAL_TANK_IMAGE.get_size()[0]/2.25, ORIGINAL_TANK_IMAGE.get_size()[1]//2.25))
