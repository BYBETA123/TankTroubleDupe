import pygame
import os
import sys
import math
from ColorDictionary import ColourDictionary as c # colors


pygame.init() # all init
pygame.mixer.set_num_channels(64) # set it here to
### Game Constants
MAZE_X = 50
MAZE_Y = 50
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TILE_SIZE = 50



MAZE_WIDTH = WINDOW_WIDTH - MAZE_X*2 # We want it to span most of the screen
MAZE_HEIGHT = WINDOW_HEIGHT - MAZE_Y*4

HYPOTENUSE = math.hypot(MAZE_WIDTH, MAZE_HEIGHT) # the maximum distance between two points in the maze
ROW_AMOUNT = MAZE_HEIGHT//TILE_SIZE # Assigning the amount of rows
COLUMN_AMOUNT = MAZE_WIDTH//TILE_SIZE # Assigning the amount of columns

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

SUPPLY_ASSETS = [[None]*11 for _ in range(3)] # 3 for the supply, 3 for the picked up supply

names = ["Damage", "Armor", "Speed"]
for i in range(3):
    for j in range(11): # each version of the supply
        SUPPLY_ASSETS[i][j] = pygame.image.load(os.path.join(BASE_PATH, 'Assets', f"{names[i]}_{j}.png")).convert_alpha()
        SUPPLY_ASSETS[i][j] = pygame.transform.scale(SUPPLY_ASSETS[i][j], (20, 20))

SOUND_DICTIONARY = {
    'tankDeath' : pygame.mixer.Sound(os.path.join(BASE_PATH, "Sounds", "tank_dead.wav")),
    'tankHurt' : pygame.mixer.Sound(os.path.join(BASE_PATH, "Sounds", "tank_dead.wav")), # replace
    'tankMove' : pygame.mixer.Sound(os.path.join(BASE_PATH, "Sounds", "tank_moving.wav")),
    'tankShoot' : pygame.mixer.Sound(os.path.join(BASE_PATH, "Sounds", "tank_shoot.wav")),
    'turretRotate' : pygame.mixer.Sound(os.path.join(BASE_PATH, "Sounds", "tank_turret_rotate.wav")),
    'Chamber' : pygame.mixer.Sound(os.path.join(BASE_PATH, "Sounds", "Chamber.wav")),
    'Empty' : pygame.mixer.Sound(os.path.join(BASE_PATH, "Sounds", "Empty.wav")),
    'Huntsman' : pygame.mixer.Sound(os.path.join(BASE_PATH, "Sounds", "Huntsman.wav")),
    'Judge' : pygame.mixer.Sound(os.path.join(BASE_PATH, "Sounds", "Judge.wav")),
    'Reload' : pygame.mixer.Sound(os.path.join(BASE_PATH, "Sounds", "Reload.wav")),
    'Silencer' : pygame.mixer.Sound(os.path.join(BASE_PATH, "Sounds", "Silencer.wav")),
    'Sidewinder' : pygame.mixer.Sound(os.path.join(BASE_PATH, "Sounds", "Sidewinder.wav")), # replace
    'Tempest' : pygame.mixer.Sound(os.path.join(BASE_PATH, "Sounds", "Tempest.wav")),
    'Watcher' : pygame.mixer.Sound(os.path.join(BASE_PATH, "Sounds", "Watcher.wav")),
}

# Controls for the first tank
CONTROLS_TANK1 = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d,
    'rotate_left': pygame.K_r,
    'rotate_right': pygame.K_t,
    'fire': pygame.K_y
}

# Controls for the second tank
CONTROLS_TANK2 = {
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'rotate_left': pygame.K_COMMA,
    'rotate_right': pygame.K_PERIOD,
    'fire': pygame.K_SLASH
}

VOLUME = {
    'lobby': 0.2,
    'selection': 1,
    'game': 0.2,
    'tankShoot': 0.5,
    'tankDeath': 0.5,
    'tankHurt': 0.5,
    'turretRotate': 0.2,
    'tankMove': 0.05,
    'Chamber': 0.5,
    'Empty': 1,
    'Huntsman': 1,
    'Judge': 0.38,
    'Reload': 0.2,
    'Silencer': 0.25,
    'Sidewinder': 1,
    'Tempest': 1,
    'Watcher': 0.5
}

PLAYER_1_TANK_NAME = "Plwasd1"
PLAYER_2_TANK_NAME = "Plarro2"
PLAYER_3_TANK_NAME = "PlAI3"
PLAYER_4_TANK_NAME = "PlAI4"
PLAYER_5_TANK_NAME = "PlAI5"
PLAYER_6_TANK_NAME = "PlAI6"
PLAYER_7_TANK_NAME = "PlAI7"
PLAYER_8_TANK_NAME = "PlAI8"

PLAYER_1_GUN_NAME = "Gun1"
PLAYER_2_GUN_NAME = "Gun2"
PLAYER_3_GUN_NAME = "Gun3"
PLAYER_4_GUN_NAME = "Gun4"
PLAYER_5_GUN_NAME = "Gun5"
PLAYER_6_GUN_NAME = "Gun6"
PLAYER_7_GUN_NAME = "Gun7"
PLAYER_8_GUN_NAME = "Gun8"

PLAYER_1_CHANNELS = {"move": {"channel": pygame.mixer.Channel(3), "volume": 0.05}, "rotate": {"channel": pygame.mixer.Channel(4), "volume": 0.2}, "death": {"channel" : pygame.mixer.Channel(5), "volume": 0.5}, "fire": {"channel": pygame.mixer.Channel(6), "volume": 1}, "hit": {"channel": pygame.mixer.Channel(7), "volume": 1}, "reload": {"channel": pygame.mixer.Channel(8), "volume": 0.5}}
PLAYER_2_CHANNELS = {"move": {"channel": pygame.mixer.Channel(9), "volume": 0.05}, "rotate": {"channel": pygame.mixer.Channel(10), "volume": 0.3}, "death": {"channel" : pygame.mixer.Channel(11), "volume": 0.5}, "fire": {"channel": pygame.mixer.Channel(12), "volume": 1}, "hit": {"channel": pygame.mixer.Channel(13), "volume": 1}, "reload": {"channel": pygame.mixer.Channel(14), "volume": 0.5}}
PLAYER_3_CHANNELS = {"move": {"channel": pygame.mixer.Channel(15), "volume": 0.05}, "rotate": {"channel": pygame.mixer.Channel(16), "volume": 0.2}, "death": {"channel" : pygame.mixer.Channel(17), "volume": 0.5}, "fire": {"channel": pygame.mixer.Channel(18), "volume": 1}, "hit": {"channel": pygame.mixer.Channel(19), "volume": 1}, "reload": {"channel": pygame.mixer.Channel(20), "volume": 0.5}}
PLAYER_4_CHANNELS = {"move": {"channel": pygame.mixer.Channel(21), "volume": 0.05}, "rotate": {"channel": pygame.mixer.Channel(22), "volume": 0.2}, "death": {"channel" : pygame.mixer.Channel(23), "volume": 0.5}, "fire": {"channel": pygame.mixer.Channel(24), "volume": 1}, "hit": {"channel": pygame.mixer.Channel(25), "volume": 1}, "reload": {"channel": pygame.mixer.Channel(26), "volume": 0.5}}
PLAYER_5_CHANNELS = {"move": {"channel": pygame.mixer.Channel(27), "volume": 0.05}, "rotate": {"channel": pygame.mixer.Channel(28), "volume": 0.2}, "death": {"channel" : pygame.mixer.Channel(29), "volume": 0.5}, "fire": {"channel": pygame.mixer.Channel(30), "volume": 1}, "hit": {"channel": pygame.mixer.Channel(31), "volume": 1}, "reload": {"channel": pygame.mixer.Channel(32), "volume": 0.5}}
PLAYER_6_CHANNELS = {"move": {"channel": pygame.mixer.Channel(33), "volume": 0.05}, "rotate": {"channel": pygame.mixer.Channel(34), "volume": 0.2}, "death": {"channel" : pygame.mixer.Channel(35), "volume": 0.5}, "fire": {"channel": pygame.mixer.Channel(36), "volume": 1}, "hit": {"channel": pygame.mixer.Channel(37), "volume": 1}, "reload": {"channel": pygame.mixer.Channel(38), "volume": 0.5}}
PLAYER_7_CHANNELS = {"move": {"channel": pygame.mixer.Channel(39), "volume": 0.05}, "rotate": {"channel": pygame.mixer.Channel(40), "volume": 0.2}, "death": {"channel" : pygame.mixer.Channel(41), "volume": 0.5}, "fire": {"channel": pygame.mixer.Channel(42), "volume": 1}, "hit": {"channel": pygame.mixer.Channel(43), "volume": 1}, "reload": {"channel": pygame.mixer.Channel(44), "volume": 0.5}}
PLAYER_8_CHANNELS = {"move": {"channel": pygame.mixer.Channel(45), "volume": 0.05}, "rotate": {"channel": pygame.mixer.Channel(46), "volume": 0.2}, "death": {"channel" : pygame.mixer.Channel(47), "volume": 0.5}, "fire": {"channel": pygame.mixer.Channel(48), "volume": 1}, "hit": {"channel": pygame.mixer.Channel(49), "volume": 1}, "reload": {"channel": pygame.mixer.Channel(50), "volume": 0.5}}

