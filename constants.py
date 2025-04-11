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

titleText = FONT_DICTIONARY["titleFont"].render('FLANKI', True, (0, 0, 0))  # Render the title text
BACKGROUND_COLOR = c.geT('SOFT_WHITE')

LOGO_PNG = pygame.image.load(os.path.join(BASE_PATH, "Assets", "logo.png")).convert_alpha()
LOGO_PNG = pygame.transform.scale(LOGO_PNG, (LOGO_PNG.get_size()[0]//15, LOGO_PNG.get_size()[1]//15))

ORIGINAL_TANK_IMAGE = pygame.image.load(os.path.join(BASE_PATH, './Assets/tank_menu_logo.png')).convert_alpha()
ORIGINAL_TANK_IMAGE = pygame.transform.scale(ORIGINAL_TANK_IMAGE, (ORIGINAL_TANK_IMAGE.get_size()[0]/2.25, ORIGINAL_TANK_IMAGE.get_size()[1]//2.25))

    # info screen
INFOLIST = ["Controls", "Tempest", "Silencer", "Watcher", "Chamber", "Huntsman", "Judge", "Sidewinder", "Panther", "Cicada", "Gater", "Bonsai", "Fossil"] # This list contains all the changing elements
INFODESCRIPTION = [["Player 1 Movement: WASD", "Player 1 Turret: RT", "Player 1 Shoot: Y", "", "Player 2 Movement: Arrow Keys", "Player 2 Turret: ,.", "Player 2 Shoot: /"],
["Type: TURRET",
"The Tempest is a single-barreled turret with infinite",
"range, perfect for aggressive, close-quarters combat.",
"It’s not a sniper but a relentless pressure tool,",
"firing steady, low-damage shots while you charge at",
"enemies. The Tempest thrives in high-paced",
"engagements, wearing opponents down through sheer",
"volume rather than precision."],
["Type: TURRET",
"The Silencer is a sniper turret built for precision",
"strikes, delivering devastating high-damage shots.",
"Its powerful rounds come with a noticeable wind-up",
"time and lengthy reload, making it crucial to choose",
"your shots wisely. Patience and timing are key, as",
"this turret rewards those who can strike with",
"pinpoint accuracy in the heat of battle."],
["Type: TURRET",
"The Watcher is a precision sniper turret with a laser",
"scope that grows more lethal the longer you maintain",
"your aim. While charging, your tank becomes immobile,",
"allowing you to focus on lining up the perfect shot.",
"Patience is crucial, as the longer you hold your aim,",
"the more devastating the damage—but staying too long",
"may expose you to enemy fire."],
["Type: TURRET",
"The Chamber is a medium-range turret with explosive",
"rounds that deal splash damage, making it perfect for",
"applying pressure in one-on-one duels. With medium",
"damage and a balanced reload speed, it’s a versatile",
"tool for controlling space. Just be cautious in close",
"quarters—your own explosive shots can easily backfire",
"on you if you’re too close to your target."],
["Type: TURRET",
"The Huntsman is a versatile, beginner-friendly turret",
"that performs decently in any situation. Its fast",
"reload and balanced stats make it reliable, while the",
"chance for a random critical shot adds some",
"unpredictability. Perfect for those learning the",
"ropes, it’s a solid all-rounder with a bit of extra",
"punch when luck is on your side."],
["Type: TURRET",
"The Judge is a close-range shotgun turret with a",
"medium-sized cone spread, perfect for punishing",
"enemies in tight spaces. Its shrapnel rounds can hit",
"multiple targets or ricochet around corners, but be",
"careful—those bouncing shots can also come back to",
"haunt you. With just two players on the map, it",
"excels in fast, decisive confrontations where",
"positioning is everything."],
["Type: TURRET",
"The Sidewinder is a short-range turret with plasma",
"rounds that can bounce off surfaces, hitting enemies",
"even outside your line of sight. While great for",
"creative tactics and surprising foes, its ricocheting",
"shots can also backfire and damage you if you’re not",
"careful. With limited energy that recharges over time,",
"mastering this turret is all about timing and smart",
"positioning."],
["Type: HULL",
"The Panther is a lightweight, high-speed hull built",
"for those who prioritize agility over durability. Its",
"incredible speed makes it perfect for quick strikes",
"and evasive maneuvers, though its low health leaves",
"little room for error. With the Panther, it’s all",
"about outpacing your opponents while avoiding direct",
"hits."],
["Type: HULL",
"The Cicada is a nimble, fast-moving hull with just",
"enough health to handle quick engagements. Its",
"responsive handling makes it ideal for weaving",
"through tight spots and quickly repositioning.",
"The Cicada strikes a balance between speed and",
"survivability, perfect for those who want agility",
"without feeling too fragile."],
["Type: HULL",
"The Gater is a wide, medium-class hull that offers",
"solid speed without sacrificing too much durability.",
"With its balanced movement and health, it’s versatile",
"enough for various tactics while leaning toward",
"faster, aggressive plays. The Gater’s broad base",
"provides stability, making it a reliable choice for",
"those who like a mix of power and mobility."],
["Type: HULL",
"The Bonsai is a tall hull with robust health and",
"medium movement, offering excellent protection in",
"battles. Its sturdy design makes it a reliable",
"frontline tank, absorbing damage while still",
"maintaining reasonable agility. The Bonsai is",
"perfect for players who need a durable tank that",
"can withstand heavy hits while keeping up with the",
"pace of the fight."],
["Type: HULL",
"The Fossil is an incredibly tanky hull built to",
"endure heavy assaults with minimal speed. Its",
"formidable armor allows it to absorb significant",
"damage, making it a fortress on the battlefield.",
"Though slow-moving, the Fossil’s resilience ensures",
"it can withstand even the toughest enemy fire,",
"crushing anything that stands in its way."]] # Description of all the elements

INFORENDER = [[FONT_DICTIONARY["iFont"].render(line, True, c.geT("BLACk")) for line in INFODESCRIPTION[i]] for i in range(len(INFODESCRIPTION))]