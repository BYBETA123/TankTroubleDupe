import pygame
import random
import math
import time
import os, sys
from ColorDictionary import ColourDictionary as c # colors
from enum import Enum
from UIUtility import Button, ButtonSlider, TextBox
from music import Music
import copy
from tanks import *
# from main import Tempest, Silencer, Watcher, Chamber, Huntsman, Judge, Sidewinder
import constants as const

class SharedVolumeScreen:
    _instance = None
    # This class is to exclusively hold the mute and sfx buttons
    mute = ButtonSlider(c.geT("BLACK"), c.geT("BLUE"), const.MAZE_X * 2.5, const.WINDOW_HEIGHT/8*3, const.TILE_SIZE, const.TILE_SIZE, const.TILE_SIZE*8,
                        const.TILE_SIZE*2, 'mute', c.geT("WHITE"), c.geT("BLACK"), c.geT("RED"))
    sfx = ButtonSlider(c.geT("BLACK"), c.geT("BLUE"), const.MAZE_X * 2.5, const.WINDOW_HEIGHT/8*5 - const.TILE_SIZE, const.TILE_SIZE, const.TILE_SIZE,
                    const.TILE_SIZE*8, const.TILE_SIZE*2, 'SFX', c.geT("WHITE"), c.geT("BLACK"), c.geT("RED"))

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SharedVolumeScreen, cls).__new__(cls)
        return cls._instance

    def updateMute(self, mouse):
        self.mute.updateSlider(mouse[0], mouse[1])
    
    def updateSFX(self, mouse):
        self.sfx.updateSlider(mouse[0], mouse[1])

    def isWithinVolumeButton(self, mousePos):
        return self.volumeButton.is_hovered(mousePos)

class SettingsScreen:

    creditButton = Button(c.geT("GREEN"), c.geT("WHITE"), const.WINDOW_WIDTH/2 - 200, 0.8 * const.WINDOW_HEIGHT, 400, const.TILE_SIZE, 'Credits')
    homeButton = Button(c.geT("GREEN"), c.geT("WHITE"),const.MAZE_X * 1.5 , const.MAZE_Y * 1.8, const.TILE_SIZE, const.TILE_SIZE, 'Home')
    quitButton = Button(c.geT("GREEN"), c.geT("WHITE"), const.WINDOW_WIDTH - const.MAZE_X * 2.5, const.MAZE_Y * 1.8, const.TILE_SIZE, const.TILE_SIZE, 'Quit')

    def __init__(self):
        self.volume = SharedVolumeScreen() # Accessing the singleton version of the volume

    def draw(self, screen):
        pygame.draw.rect(screen, c.geT("OFF_WHITE"), [const.MAZE_X, const.MAZE_Y, const.WINDOW_WIDTH - const.MAZE_X * 2, const.WINDOW_HEIGHT - const.MAZE_Y * 2])
        pygame.draw.rect(screen, c.geT("BLACK"), [const.MAZE_X, const.MAZE_Y, const.WINDOW_WIDTH - const.MAZE_X * 2, const.WINDOW_HEIGHT - const.MAZE_Y * 2], 5)

        #Buttons
        self.creditButton.draw(screen, outline = True)
            
        self.homeButton.draw(screen, outline = True)
        self.quitButton.draw(screen, outline = True)
        self.volume.mute.draw(screen, outline = False)
        self.volume.sfx.draw(screen, outline = False)

    def updateMute(self, mouse):
        self.volume.mute.updateSlider(mouse[0], mouse[1])

    def updateSFX(self, mouse):
        self.volume.sfx.updateSlider(mouse[0], mouse[1])

    def getSFXValue(self):
        return self.volume.sfx.getValue()
    
    def isWithinCreditButton(self, mousePos):
        return self.creditButton.is_hovered(mousePos)
    
    def isWithinHomeButton(self, mousePos):
        return self.homeButton.is_hovered(mousePos)

    def isWithinQuitButton(self, mousePos):
        return self.quitButton.is_hovered(mousePos)

    def isWithinMuteButton(self, mousePos):
        return self.volume.mute.checkButtonClick(mousePos[0], mousePos[1])

    def isWithinSFXButton(self, mousePos):
        return self.volume.sfx.checkButtonClick(mousePos[0], mousePos[1])

    def getMuteValue(self):
        return self.volume.mute.getValue()

class PauseScreen:

    #Buttons
    homeButton = Button(c.geT("GREEN"), c.geT("WHITE"),const.MAZE_X * 1.5 , const.MAZE_Y * 1.8, const.TILE_SIZE, const.TILE_SIZE, 'Home')
    quitButton = Button(c.geT("GREEN"), c.geT("WHITE"), const.WINDOW_WIDTH - const.MAZE_X * 2.5, const.MAZE_Y * 1.8, const.TILE_SIZE, const.TILE_SIZE, 'Quit')
    unPauseButton = Button(c.geT("GREEN"), c.geT("WHITE"), const.WINDOW_WIDTH/2 - 200, 0.8 * const.WINDOW_HEIGHT, 400, const.TILE_SIZE, 'Return to Game')

    def __init__(self):
        self.volume = SharedVolumeScreen() # Accessing the singleton version of the volume

    def draw(self, screen):
        # This function will draw the pause screen
        # Inputs: None
        # Outputs: None
        pygame.draw.rect(screen, c.geT("OFF_WHITE"), [const.MAZE_X, const.MAZE_Y, const.WINDOW_WIDTH - const.MAZE_X * 2, const.WINDOW_HEIGHT - const.MAZE_Y * 2])
        pygame.draw.rect(screen, c.geT("BLACK"), [const.MAZE_X, const.MAZE_Y, const.WINDOW_WIDTH - const.MAZE_X * 2, const.WINDOW_HEIGHT - const.MAZE_Y * 2], 5)

        self.homeButton.draw(screen, outline = True)
        self.quitButton.draw(screen, outline = True)
        self.unPauseButton.draw(screen, outline = True)
        self.volume.mute.draw(screen, outline = False)
        self.volume.sfx.draw(screen, outline = False)

    def updateMute(self, mouse):
        self.volume.mute.updateSlider(mouse[0], mouse[1])

    def updateSFX(self, mouse):
        self.volume.sfx.updateSlider(mouse[0], mouse[1])

    def getSFXValue(self):
        return self.volume.sfx.getValue()
    
    def isWithinUnpauseButton(self, mousePos):
        return self.unPauseButton.is_hovered(mousePos)
    
    def isWithinHomeButton(self, mousePos):
        return self.homeButton.is_hovered(mousePos)

    def isWithinQuitButton(self, mousePos):
        return self.quitButton.is_hovered(mousePos)

    def isWithinMuteButton(self, mousePos):
        return self.volume.mute.checkButtonClick(mousePos[0], mousePos[1])

    def isWithinSFXButton(self, mousePos):
        return self.volume.sfx.checkButtonClick(mousePos[0], mousePos[1])

    def getMuteValue(self):
        return self.volume.mute.getValue()

class CreditScreen:

    creditsBackButton = Button(c.geT("GREEN"), c.geT("WHITE"), const.WINDOW_WIDTH - 175, 75, 100, const.TILE_SIZE, 'Back', c.geT("BLACK"), 20, (100, 100, 255))
    creditsTitle = TextBox(const.WINDOW_WIDTH//2 - 175, 100, font=const.SELECTION_FONT,fontSize=104, text="Credits", textColor=c.geT("BLACK"))
    creditsTitle.selectable(False)
    creditsTitle.setBoxColor(c.geT("OFF_WHITE"))

    disclaimer = TextBox(57, const.WINDOW_HEIGHT - 110, font=const.SELECTION_FONT,fontSize=35, text="ALL RIGHTS BELONG TO THEIR RESPECTIVE OWNERS", textColor=c.geT("BLACK"))
    disclaimer.selectable(False)
    disclaimer.setBoxColor(c.geT("OFF_WHITE"))

    creditbox = [
        "Lead Developer: Beta",
        "UI Design: Bin-Coder14, Beta",
        "Sounds: Beta",
        "Music: Beta, Goodnews888",
        "Art: Beta, Goodnews888, Ekiel",
    ]

    creditsurfaces = [const.FONT_DICTIONARY["cFont"].render(line, True, c.geT("BLACk")) for line in creditbox]

    def draw(self, screen):
        pygame.draw.rect(screen, (240, 240, 240), [const.MAZE_X, const.MAZE_Y, const.WINDOW_WIDTH - const.MAZE_X * 2, const.WINDOW_HEIGHT - const.MAZE_Y * 2])
        pygame.draw.rect(screen, (0,0,0), [const.MAZE_X, const.MAZE_Y, const.WINDOW_WIDTH - const.MAZE_X * 2, const.WINDOW_HEIGHT - const.MAZE_Y * 2], 5) # outline
        self.creditsBackButton.draw(screen = screen, outline = True)
        self.creditsTitle.draw(screen = screen, outline= True)
        self.disclaimer.draw(screen = screen, outline = True)

        for idx, c in enumerate(self.creditsurfaces):
            screen.blit(c, (const.MAZE_X + 50, 200 + idx * 50))

    def isWithinBackButton(self, mousePos):
        return self.creditsBackButton.is_hovered(mousePos)
    
class InfoScreen:

    INFOLIST = ["Controls", "Tempest", "Silencer", "Watcher", "Chamber", "Huntsman", "Judge", "Sidewinder", "Panther", "Cicada", "Gater", "Bonsai", "Fossil"] # This list contains all the changing elements
    infoButtons = []
    iIndex = 0
    infoLArrow = Button(c.geT("BLACK"), c.geT("BLACK"), 100, 200, 100, 100, '<', c.geT("WHITE"), 100, c.geT("BLACK"))
    infoButtons.append(infoLArrow)
    infoText = TextBox(const.WINDOW_WIDTH//2 - 125, 75, font="Courier New",fontSize=30, text="Information", textColor=c.geT("BLACK"))
    infoText.selectable(False)
    infoText.setBoxColor(c.geT("OFF_WHITE"))
    infoButtons.append(infoText)
    iBox = TextBox(200, 201, font="Courier New",fontSize=46, text=INFOLIST[iIndex], textColor=c.geT("BLACK"))
    iBox.selectable(False)
    iBox.setCharacterPad(14)
    iBox.setPaddingHeight(23)
    iBox.setText(INFOLIST[iIndex])
    iBox.setBoxColor(c.geT("OFF_WHITE"))
    infoButtons.append(iBox)
    infoRArrow = Button(c.geT("BLACK"), c.geT("BLACK"), const.WINDOW_WIDTH - 200, 200, 100, 100, '>', c.geT("WHITE"), 100, c.geT("BLACK"))
    infoButtons.append(infoRArrow)
    infoBackButton = Button(c.geT("GREEN"), c.geT("WHITE"), const.WINDOW_WIDTH - 175, 75, 100, const.TILE_SIZE, 'Back', c.geT("BLACK"), 20, (100, 100, 255))
    infoButtons.append(infoBackButton)

    # info screen
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

    def __init__(self):
        self.INFORENDER = [[const.FONT_DICTIONARY["iFont"].render(line, True, c.geT("BLACk")) for line in self.INFODESCRIPTION[i]] for i in range(len(self.INFODESCRIPTION))]

    def draw(self, screen):
        pygame.draw.rect(screen, (240, 240, 240), [const.MAZE_X, const.MAZE_Y, const.WINDOW_WIDTH - const.MAZE_X * 2, const.WINDOW_HEIGHT - const.MAZE_Y * 2])
        pygame.draw.rect(screen, (0,0,0), [const.MAZE_X, const.MAZE_Y, const.WINDOW_WIDTH - const.MAZE_X * 2, const.WINDOW_HEIGHT - const.MAZE_Y * 2], 5)

        for i in self.infoButtons:
            i.draw(screen = screen, outline = True)
        
        startY = 325
        gap = 25
        for i in range(len(self.INFORENDER[self.iIndex])):
            screen.blit(self.INFORENDER[self.iIndex][i], (const.MAZE_X + 50, startY + i*gap))

    def isWithinBackButton(self, mousePos):
        return self.infoBackButton.is_hovered(mousePos)
    
    def isWithinLArrowButton(self, mousePos):
        return self.infoLArrow.is_hovered(mousePos)
    
    def isWithinRArrowButton(self, mousePos):
        return self.infoRArrow.is_hovered(mousePos)
    
    def updateBox(self, index):
        self.iIndex = (self.iIndex + index) % len(self.INFOLIST)
        self.iBox.setText(self.INFOLIST[self.iIndex])

class HomeScreen:
    
    homeButtonNameArray = ["1P Yard", "1P Scrapyard", "2P Yard", "2P Scrapyard", "1p Brawl", "1P DeathMatch", "2P Brawl", "2P DeathMatch"] #<!>
    homeButtonList = []

    # Create buttons with specified positions and text
    homeLeftButton = Button(c.geT("BLACK"), c.geT("BLACK"), 30, 490, 40, 80, '←', (255, 255, 255), 25, hoverColor=(100, 100, 255))
    HomeButton1 = Button(c.geT("BLACK"),c.geT("BLACK"), 106, 490, 120, 80, homeButtonNameArray[0], (255, 255, 255), 15, hoverColor=(100, 100, 255))
    HomeButton2 = Button(c.geT("BLACK"),c.geT("BLACK"), 262, 490, 120, 80, homeButtonNameArray[1], (255, 255, 255), 15, hoverColor=(100, 100, 255))
    HomeButton3 = Button(c.geT("BLACK"),c.geT("BLACK"), 418, 490, 120, 80, homeButtonNameArray[2], (255, 255, 255), 15, hoverColor=(100, 100, 255))
    HomeButton4 = Button(c.geT("BLACK"),c.geT("BLACK"), 574, 490, 120, 80, homeButtonNameArray[3], (255, 255, 255), 15, hoverColor=(100, 100, 255))
    homeRightButton = Button(c.geT("BLACK"), c.geT("BLACK"), 730, 490, 40, 80, '→', (255, 255, 255), 25, hoverColor=(100, 100, 255))

    quitButtonHome = Button(c.geT("BLACK"), c.geT("BLACK"), 30, 30, 140, 80, 'Quit', (255, 255, 255), 25, hoverColor=(100, 100, 255))
    settingsButton = Button(c.geT("BLACK"), c.geT("BLACK"), 570, 30, 210, 80, 'Settings', (255, 255, 255), 25, hoverColor=(100, 100, 255))

    homeButtonList.append(homeLeftButton)
    homeButtonList.append(HomeButton1)
    homeButtonList.append(HomeButton3)
    homeButtonList.append(HomeButton2)
    homeButtonList.append(HomeButton4)
    homeButtonList.append(homeRightButton)
    homeButtonList.append(settingsButton)
    homeButtonList.append(quitButtonHome)

    LOGO_PNG = pygame.image.load(os.path.join(const.BASE_PATH, "Assets", "logo.png")).convert_alpha()
    LOGO_PNG = pygame.transform.scale(LOGO_PNG, (LOGO_PNG.get_size()[0]//15, LOGO_PNG.get_size()[1]//15))

    ORIGINAL_TANK_IMAGE = pygame.image.load(os.path.join(const.BASE_PATH, './Assets/tank_menu_logo.png')).convert_alpha()
    ORIGINAL_TANK_IMAGE = pygame.transform.scale(ORIGINAL_TANK_IMAGE, (ORIGINAL_TANK_IMAGE.get_size()[0]/2.25, ORIGINAL_TANK_IMAGE.get_size()[1]//2.25))

    TITLE_TEXT = const.FONT_DICTIONARY["titleFont"].render('FLANKI', True, (0, 0, 0))  # Render the title text

    def draw(self, screen, mouse):

        screen.fill(const.BACKGROUND_COLOR) # This is the first line when drawing a new frame
        screen.blit(self.LOGO_PNG, (const.WINDOW_WIDTH // 2 - self.LOGO_PNG.get_width() // 2, 15))
        # Draw the tank image
        screen.blit(self.ORIGINAL_TANK_IMAGE, (const.WINDOW_WIDTH//2 - self.ORIGINAL_TANK_IMAGE.get_width()//2, const.WINDOW_HEIGHT//2 - self.ORIGINAL_TANK_IMAGE.get_height()//2))  # Centered horizontally

        # Draw the title text
        screen.blit(self.TITLE_TEXT, (const.WINDOW_WIDTH // 2 - self.TITLE_TEXT.get_width() // 2, 110))  # Centered horizontally, 50 pixels from top

        # Handle hover effect and draw buttons
        for button in self.homeButtonList:
            button.update_display(mouse)
            button.draw(screen, outline=True)

    def isWithinHomeButton1(self, mousePos):
        return self.HomeButton1.is_hovered(mousePos)
    
    def isWithinHomeButton2(self, mousePos):
        return self.HomeButton2.is_hovered(mousePos)
    
    def isWithinHomeButton3(self, mousePos):
        return self.HomeButton3.is_hovered(mousePos)
    
    def isWithinHomeButton4(self, mousePos):
        return self.HomeButton4.is_hovered(mousePos)
    
    def isWithinHomeLeftButton(self, mousePos):
        return self.homeLeftButton.is_hovered(mousePos)
    
    def isWithinHomeRightButton(self, mousePos):
        return self.homeRightButton.is_hovered(mousePos)
    
    def isWithinSettingsButton(self, mousePos):
        return self.settingsButton.is_hovered(mousePos)
    
    def isWithinQuitButton(self, mousePos):
        return self.quitButtonHome.is_hovered(mousePos)
    
    def getLenNameArray(self):
        return len(self.homeButtonNameArray)
    
    def setTextHomeButton1(self, text):
        self.HomeButton1.setText(self.homeButtonNameArray[text % len(self.homeButtonNameArray)])
    
    def setTextHomeButton2(self, text):
        self.HomeButton2.setText(self.homeButtonNameArray[text % len(self.homeButtonNameArray)])
    
    def setTextHomeButton3(self, text):
        self.HomeButton3.setText(self.homeButtonNameArray[text % len(self.homeButtonNameArray)])

    def setTextHomeButton4(self, text):
        self.HomeButton4.setText(self.homeButtonNameArray[text % len(self.homeButtonNameArray)])

class SelectionScreen:

    #Selection Screen
    buttonList = []

    homeButton = TextBox(const.TILE_SIZE//4, const.TILE_SIZE//4, font=const.SELECTION_FONT,fontSize=26, text="BACK", textColor=c.geT("BLACK"))
    homeButton.setBoxColor(const.SELECTION_BACKGROUND)
    homeButton.setOutline(True, 5)
    homeButton.selectable(True)
    buttonList.append(homeButton)

    #How to play button
    howToPlayButton = TextBox(const.WINDOW_WIDTH - 150, const.TILE_SIZE//4, font=const.SELECTION_FONT,fontSize=26, text="HOW TO PLAY", textColor=c.geT("BLACK"))
    howToPlayButton.setBoxColor(const.SELECTION_BACKGROUND)
    howToPlayButton.setOutline(True, 5)
    howToPlayButton.selectable(True)
    buttonList.append(howToPlayButton)

    playButton = TextBox(const.WINDOW_WIDTH//2-84, 95, font=const.SELECTION_FONT,fontSize=52, text="PLAY", textColor=c.geT("BLACK"))
    playButton.setBoxColor(const.SELECTION_BACKGROUND)
    playButton.setOutline(True, 5)
    playButton.selectable(True)
    buttonList.append(playButton)

    buttonPrimary = c.geT("BLACK")
    buttonSecondary = c.geT("WHITE")
    buttonText = c.geT("WHITE")
    optionText = c.geT("GREY")




    ColorIndex = ["TANK_GREEN", "BURGUNDY", "ORANGE", "YELLOW", "SKY_BLUE", "LIGHT_BROWN", "DARK_LILAC", "BRIGHT_PINK"]
    hullColors = ColorIndex
    gunColors = ColorIndex # ???

    #List indexes for player selection
    #Turret index
    p1I = 0
    p2I = 0
    #Hull index
    p1J = 0
    p2J = 0
    #Colour index
    p1K = 0
    p2K = 1

    p1L = 1
    p2L = 0

    lArrowP1Turret = Button(buttonPrimary, buttonPrimary, 70, 420, 30, 30, '<', buttonText, 30)
    lArrowP1Turret.selectable(False)
    buttonList.append(lArrowP1Turret)
    textP1Turret = TextBox(100, 420, font=const.MONO_FONT,fontSize=26, text="", textColor=buttonText)
    textP1Turret.setBoxColor(optionText)
    textP1Turret.selectable(False)
    textP1Turret.setPaddingHeight(0)
    buttonList.append(textP1Turret)
    rArrowP1Turret = Button(buttonPrimary, buttonPrimary, 280, 420, 30, 30, '>', buttonText, 30)
    rArrowP1Turret.selectable(False)
    buttonList.append(rArrowP1Turret)

    lArrowP1Hull = Button(buttonPrimary, buttonPrimary, 70, 460, 30, 30, '<', buttonText, 30)
    lArrowP1Hull.selectable(False)
    buttonList.append(lArrowP1Hull)
    textP1Hull = TextBox(100, 460, font=const.MONO_FONT,fontSize=26, text="", textColor=buttonText)
    textP1Hull.setBoxColor(optionText)
    textP1Hull.selectable(False)
    textP1Hull.setPaddingHeight(0)
    buttonList.append(textP1Hull)
    rArrowP1Hull = Button(buttonPrimary, buttonPrimary, 280, 460, 30, 30, '>', buttonText, 30)
    rArrowP1Hull.selectable(False)
    buttonList.append(rArrowP1Hull)

    lArrowP1Colour = Button(buttonPrimary, buttonPrimary, 70, 500, 30, 30, '<', buttonText, 30)
    lArrowP1Colour.selectable(False)
    buttonList.append(lArrowP1Colour)
    textP1Colour = TextBox(100, 500, font=const.MONO_FONT,fontSize=26, text="", textColor=buttonText)
    textP1Colour.setBoxColor(c.geT(ColorIndex[p1K]))
    textP1Colour.selectable(False)
    textP1Colour.setPaddingHeight(0)
    buttonList.append(textP1Colour)
    rArrowP1Colour = Button(buttonPrimary, buttonPrimary, 280, 500, 30, 30, '>', buttonText, 30)
    rArrowP1Colour.selectable(False)
    buttonList.append(rArrowP1Colour)

    lArrowP1Colour2 = Button(buttonPrimary, buttonPrimary, 70, 540, 30, 30, '<', buttonText, 30)
    lArrowP1Colour2.selectable(False)
    buttonList.append(lArrowP1Colour2)
    textP1Colour2 = TextBox(100, 540, font=const.MONO_FONT,fontSize=26, text="", textColor=buttonText)
    textP1Colour2.setBoxColor(c.geT(ColorIndex[p1L]))
    textP1Colour2.selectable(False)
    textP1Colour2.setPaddingHeight(0)
    buttonList.append(textP1Colour2)
    rArrowP1Colour2 = Button(buttonPrimary, buttonPrimary, 280, 540, 30, 30, '>', buttonText, 30)
    rArrowP1Colour2.selectable(False)
    buttonList.append(rArrowP1Colour2)

    lArrowP2Turret = Button(buttonPrimary, buttonPrimary, 493, 420, 30, 30, '<', buttonText, 30)
    lArrowP2Turret.selectable(False)
    buttonList.append(lArrowP2Turret)
    textP2Turret = TextBox(523, 420, font=const.MONO_FONT,fontSize=26, text="", textColor=buttonText)
    textP2Turret.setBoxColor(optionText)
    textP2Turret.selectable(False)
    textP2Turret.setPaddingHeight(0)
    buttonList.append(textP2Turret)
    rArrowP2Turret = Button(buttonPrimary, buttonPrimary,703, 420, 30, 30, '>', buttonText, 30)
    rArrowP2Turret.selectable(False)
    buttonList.append(rArrowP2Turret)

    lArrowP2Hull = Button(buttonPrimary, buttonPrimary, 493, 460, 30, 30, '<', buttonText, 30)
    lArrowP2Hull.selectable(False)
    buttonList.append(lArrowP2Hull)
    textP2Hull = TextBox(523, 460, font=const.MONO_FONT,fontSize=26, text="", textColor=buttonText)
    textP2Hull.setBoxColor(optionText)
    textP2Hull.selectable(False)
    textP2Hull.setPaddingHeight(0)
    buttonList.append(textP2Hull)
    rArrowP2Hull = Button(buttonPrimary, buttonPrimary,  703, 460, 30, 30, '>', buttonText, 30)
    rArrowP2Hull.selectable(False)
    buttonList.append(rArrowP2Hull)

    lArrowP2Colour = Button(buttonPrimary, buttonPrimary, 493, 500, 30, 30, '<', buttonText, 30)
    lArrowP2Colour.selectable(False)
    buttonList.append(lArrowP2Colour)
    textP2Colour = TextBox(523, 500, font=const.MONO_FONT,fontSize=26, text="", textColor=buttonText)
    textP2Colour.setBoxColor(c.geT(ColorIndex[p2K]))
    textP2Colour.selectable(False)
    textP2Colour.setPaddingHeight(0)
    buttonList.append(textP2Colour)
    rArrowP2Colour = Button(buttonPrimary, buttonPrimary,  703, 500, 30, 30, '>', buttonText, 30)
    rArrowP2Colour.selectable(False)
    buttonList.append(rArrowP2Colour)

    lArrowP2Colour2 = Button(buttonPrimary, buttonPrimary, 493, 540, 30, 30, '<', buttonText, 30)
    lArrowP2Colour2.selectable(False)
    buttonList.append(lArrowP2Colour2)
    textP2Colour2 = TextBox(523, 540, font=const.MONO_FONT,fontSize=26, text="", textColor=buttonText)
    textP2Colour2.setBoxColor(c.geT(ColorIndex[p2L]))
    textP2Colour2.selectable(False)
    textP2Colour2.setPaddingHeight(0)
    buttonList.append(textP2Colour2)
    rArrowP2Colour2 = Button(buttonPrimary, buttonPrimary,  703, 540, 30, 30, '>', buttonText, 30)
    rArrowP2Colour2.selectable(False)
    buttonList.append(rArrowP2Colour2)

    textP1 = TextBox(100, 100, font=const.SELECTION_FONT,fontSize=38, text="PLAYER 1", textColor=c.geT("BLACK"))
    textP1.setBoxColor(const.SELECTION_BACKGROUND)
    textP1.setOutline(True, outlineWidth = 5)
    buttonList.append(textP1)

    textP2 = TextBox(const.WINDOW_WIDTH - 250, 100, font=const.SELECTION_FONT,fontSize=38, text="PLAYER 2", textColor=c.geT("BLACK"))
    textP2.setBoxColor(const.SELECTION_BACKGROUND)
    textP2.setOutline(True, outlineWidth = 5)
    buttonList.append(textP2)

    speedText = TextBox(50, 250, font=const.SELECTION_FONT,fontSize=36, text="SPEED", textColor=c.geT("BLACK"))
    speedText.setPaddingHeight(0)
    speedText.setPaddingWidth(0)
    speedText.setCharacterPad(7)
    speedText.setBoxColor(const.SELECTION_BACKGROUND)
    speedText.setText("SPEED", 'right')
    buttonList.append(speedText)

    healthText = TextBox(42, 285, font=const.SELECTION_FONT,fontSize=36, text="Health", textColor=c.geT("BLACK"))
    healthText.setPaddingHeight(0)
    healthText.setPaddingWidth(0)
    healthText.setCharacterPad(7)
    healthText.setBoxColor(const.SELECTION_BACKGROUND)
    healthText.setText("HEALTH", "right")
    buttonList.append(healthText)

    damageBar = TextBox(31, 320, font=const.SELECTION_FONT,fontSize=36, text="Damage", textColor=c.geT("BLACK"))
    damageBar.setPaddingHeight(0)
    damageBar.setPaddingWidth(0)
    damageBar.setCharacterPad(7)
    damageBar.setBoxColor(const.SELECTION_BACKGROUND)
    damageBar.setText("DAMAGE", "right")
    buttonList.append(damageBar)

    reloadBar = TextBox(37, 355, font=const.SELECTION_FONT,fontSize=36, text="Reload", textColor=c.geT("BLACK"))
    reloadBar.setPaddingHeight(0)
    reloadBar.setPaddingWidth(0)
    reloadBar.setCharacterPad(7)
    reloadBar.setBoxColor(const.SELECTION_BACKGROUND)
    reloadBar.setText("RELOAD", "right")
    buttonList.append(reloadBar)

    speedText2 = TextBox(650, 250, font=const.SELECTION_FONT,fontSize=36, text="Speed", textColor=c.geT("BLACK"))
    speedText2.setPaddingHeight(0)
    speedText2.setPaddingWidth(0)
    speedText2.setCharacterPad(7)
    speedText2.setBoxColor(const.SELECTION_BACKGROUND)
    speedText2.setText("SPEED", "left")
    buttonList.append(speedText2)

    healthText2 = TextBox(650, 285, font=const.SELECTION_FONT,fontSize=36, text="Health", textColor=c.geT("BLACK"))
    healthText2.setPaddingHeight(0)
    healthText2.setPaddingWidth(0)
    healthText2.setCharacterPad(7)
    healthText2.setBoxColor(const.SELECTION_BACKGROUND)
    healthText2.setText("HEALTH", "left")
    buttonList.append(healthText2)

    damageBar2 = TextBox(650, 320, font=const.SELECTION_FONT,fontSize=36, text="Damage", textColor=c.geT("BLACK"))
    damageBar2.setPaddingHeight(0)
    damageBar2.setPaddingWidth(0)
    damageBar2.setCharacterPad(7)
    damageBar2.setBoxColor(const.SELECTION_BACKGROUND)
    damageBar2.setText("DAMAGE", "left")
    buttonList.append(damageBar2)

    reloadBar2 = TextBox(650, 355, font=const.SELECTION_FONT,fontSize=36, text="Reload", textColor=c.geT("BLACK"))
    reloadBar2.setPaddingHeight(0)
    reloadBar2.setPaddingWidth(0)
    reloadBar2.setCharacterPad(7)
    reloadBar2.setBoxColor(const.SELECTION_BACKGROUND)
    reloadBar2.setText("RELOAD", "left")
    buttonList.append(reloadBar2)

    def __init__(self, turretList, hullList, mousePos):
        self.playerInformation = PlayerInformation(turretList, hullList)
        self.turretList = self.playerInformation.getTurretList()
        self.hullList = self.playerInformation.getHullList()
        self.turretListLength = len(self.turretList)
        self.hullListLength = len(self.hullList)
        self.update(mousePos)

    def update(self, mousePos):
        # do all the buttons
        self.isWithinLArrowP1Turret(mousePos)
        self.isWithinRArrowP1Turret(mousePos)
        self.isWithinLArrowP1Hull(mousePos)
        self.isWithinRArrowP1Hull(mousePos)
        self.isWithinLArrowP1Colour(mousePos)
        self.isWithinRArrowP1Colour(mousePos)
        self.isWithinLArrowP1Colour2(mousePos)
        self.isWithinRArrowP1Colour2(mousePos)
        self.isWithinLArrowP2Turret(mousePos)
        self.isWithinRArrowP2Turret(mousePos)
        self.isWithinLArrowP2Hull(mousePos)
        self.isWithinRArrowP2Hull(mousePos)
        self.isWithinLArrowP2Colour(mousePos)
        self.isWithinRArrowP2Colour(mousePos)
        self.isWithinRArrowP2Colour2(mousePos)
        self.isWithinLArrowP2Colour2(mousePos)


        self.textP1Turret.setText(self.turretList[self.p1I].getGunName())
        self.textP2Turret.setText(self.turretList[self.p2I].getGunName())
        self.textP1Hull.setText(self.hullList[self.p1J].getTankName())
        self.textP2Hull.setText(self.hullList[self.p2J].getTankName())

    def draw(self, screen, mouse):


        screen.fill(const.SELECTION_BACKGROUND) # This is the first line when drawing a new frame

        for button in self.buttonList:
            button.update_display(mouse)
            button.draw(screen, outline = False)

        # Player 1 Speed
        pygame.draw.rect(screen, c.geT("GREEN"), (157, 250, 50 * self.hullList[self.p1J].getSpeedStatistic(), 25)) # Green bar
        #Outlines
        pygame.draw.rect(screen, c.geT("BLACK"), (157, 250, 150, 25), 3) # Green bar outline
        pygame.draw.rect(screen, c.geT("BLACK"), (207, 250, 50, 25), 3) # Thirding

        #Player 1 Health
        pygame.draw.rect(screen, c.geT("GREEN"), (157, 285, 50 * self.hullList[self.p1J].getHealthStatistic(), 25)) # Green bar
        #Outlines
        pygame.draw.rect(screen, c.geT("BLACK"), (157, 285, 150, 25), 3) # Green bar outline
        pygame.draw.rect(screen, c.geT("BLACK"), (207, 285, 50,25), 3) # Thirding

        # Player 1 damage
        pygame.draw.rect(screen, c.geT("GREEN"), (157, 320, 50 * self.turretList[self.p1I].getDamageStatistic(), 25)) # Green bar
        #Outlines
        pygame.draw.rect(screen, c.geT("BLACK"), (157, 320, 150, 25), 3) # Green bar outline
        pygame.draw.rect(screen, c.geT("BLACK"), (207, 320, 50,25), 3) # Thirding

        # Player 1 reload
        pygame.draw.rect(screen, c.geT("GREEN"), (157, 355, 50 * self.turretList[self.p1I].getReloadStatistic(), 25)) # Green bar
        #Outlines
        pygame.draw.rect(screen, c.geT("BLACK"), (157, 355, 150, 25), 3) # Green bar outline
        pygame.draw.rect(screen, c.geT("BLACK"), (207, 355, 50,25), 3) # Thirding

        #Player 2 Speed
        pygame.draw.rect(screen, c.geT("GREEN"), (493, 250, 50 * self.hullList[self.p2J].getSpeedStatistic(), 25)) # Green bar
        #Outlines
        pygame.draw.rect(screen, c.geT("BLACK"), (493, 250, 50 * 3, 25), 3) # Green bar outline
        pygame.draw.rect(screen, c.geT("BLACK"), (543, 250, 50,25), 3) # Thirding

        # Player 2 Health
        pygame.draw.rect(screen, c.geT("GREEN"), (493, 285, 50 * self.hullList[self.p2J].getHealthStatistic(), 25)) # Green bar
        #Outlines
        pygame.draw.rect(screen, c.geT("BLACK"), (493, 285, 150, 25), 3) # Green bar outline
        pygame.draw.rect(screen, c.geT("BLACK"), (543, 285, 50,25), 3) # Thirding

        # Player 2 Damage
        pygame.draw.rect(screen, c.geT("GREEN"), (493, 320,50 * self.turretList[self.p2I].getDamageStatistic(), 25)) # Green bar
        #Outlines
        pygame.draw.rect(screen, c.geT("BLACK"), (493, 320, 150, 25), 3) # Green bar outline
        pygame.draw.rect(screen, c.geT("BLACK"), (543, 320, 50, 25), 3) # Thirding

        # Player 2 Reload
        pygame.draw.rect(screen, c.geT("GREEN"), (493, 355, 50 * self.turretList[self.p2I].getReloadStatistic(), 25)) # Green bar
        #Outlines
        pygame.draw.rect(screen, c.geT("BLACK"), (493, 355, 150, 25), 3) # Green bar outline
        pygame.draw.rect(screen, c.geT("BLACK"), (543, 355, 50,25), 3) # Thirding

        #Draw the tank image

        tankPath = os.path.join(const.BASE_PATH, 'Sprites', self.hullList[self.p1J].getTankName() + str(self.p1L + 1) + '.png')
        originalTankImage = pygame.image.load(tankPath).convert_alpha()
        tankImage = pygame.transform.scale(originalTankImage, (20*4, 13*4))
        screen.blit(tankImage, (130, 174))

        gunPath = os.path.join(const.BASE_PATH, 'Sprites', self.turretList[self.p1I].getGunName() + str(self.p1K+1) + '.png')
        originalGunImage = pygame.image.load(gunPath).convert_alpha()
        centerX, centerY = self.hullList[self.p1J].getGunCenter()
        gX, _ = self.turretList[self.p1I].getGunCenter()
        gunImage = pygame.transform.scale(originalGunImage, (15*5, 15*5))
        screen.blit(gunImage, (170 + (centerX - gX) * 5, 194 - (centerY + 6) * 5))
        
        tankPath2 = os.path.join(const.BASE_PATH, 'Sprites', self.hullList[self.p2J].getTankName() + str(self.p2L + 1) + '.png')
        originalTankImage2 = pygame.image.load(tankPath2).convert_alpha()
        tankImage2 = pygame.transform.scale(originalTankImage2, (20*4, 13*4))
        tankImage2 = pygame.transform.flip(tankImage2, True, False) # Flipped    
        screen.blit(tankImage2, (const.WINDOW_WIDTH - 130 - 4 * 20, 174))

        gunPath2 = os.path.join(const.BASE_PATH, 'Sprites', self.turretList[self.p2I].getGunName() + str(self.p2K+1) + '.png')
        originalGunImage2 = pygame.image.load(gunPath2).convert_alpha()
        centerX, centerY = self.hullList[self.p2J].getGunCenter()
        gX, _ = self.turretList[self.p2I].getGunCenter()

        gunImage2 = pygame.transform.scale(originalGunImage2, (15*5, 15*5))
        gunImage2 = pygame.transform.flip(gunImage2, True, False) # Flipped
        screen.blit(gunImage2, (const.WINDOW_WIDTH - 170 - 5 * 15 - (centerX - gX)*5, 194 + centerY*5 - 6*5))

    def isWithinPlayButton(self, mousePos):
        return self.playButton.buttonClick(mousePos)
    
    def isWithinHowToPlayButton(self, mousePos):
        return self.howToPlayButton.buttonClick(mousePos)
    
    def isWithinHomeButton(self, mousePos):
        return self.homeButton.buttonClick(mousePos)
    
    def isWithinLArrowP1Turret(self, mousePos):
        if self.lArrowP1Turret.is_hovered(mousePos):
            self.p1I = (self.p1I - 1) % self.turretListLength
            self.textP1Turret.setText(self.turretList[self.p1I].getGunName())
    
    def isWithinRArrowP1Turret(self, mousePos):
        if self.rArrowP1Turret.is_hovered(mousePos):
            self.p1I = (self.p1I + 1) % self.turretListLength
            self.textP1Turret.setText(self.turretList[self.p1I].getGunName())
    
    def isWithinLArrowP1Hull(self, mousePos):
        if self.lArrowP1Hull.is_hovered(mousePos):
            self.p1J = (self.p1J - 1) % self.hullListLength
            self.textP1Hull.setText(self.hullList[self.p1J].getTankName())
    
    def isWithinRArrowP1Hull(self, mousePos):
        if self.rArrowP1Hull.is_hovered(mousePos):
            self.p1J = (self.p1J + 1) % self.hullListLength
            self.textP1Hull.setText(self.hullList[self.p1J].getTankName())
    
    def isWithinLArrowP1Colour(self, mousePos):
        if self.lArrowP1Colour.is_hovered(mousePos):
            self.p1K = (self.p1K - 1) % len(self.hullColors)
            if self.p1K == self.p2K:
                self.p1K = (self.p1K - 1) % len(self.hullColors)
            self.textP1Colour.setBoxColor(c.geT(self.ColorIndex[self.p1K]))

    def isWithinRArrowP1Colour(self, mousePos):
        if self.rArrowP1Colour.is_hovered(mousePos):
            self.p1K = (self.p1K + 1) % len(self.hullColors)
            if self.p1K == self.p2K:
                self.p1K = (self.p1K + 1) % len(self.hullColors)
            self.textP1Colour.setBoxColor(c.geT(self.ColorIndex[self.p1K]))
    
    def isWithinLArrowP1Colour2(self, mousePos):
        if self.lArrowP1Colour2.is_hovered(mousePos):
            self.p1L = (self.p1L - 1) % len(self.hullColors)
            if self.p1L == self.p2L:
                self.p1L = (self.p1L - 1) % len(self.hullColors)
            self.textP1Colour2.setBoxColor(c.geT(self.ColorIndex[self.p1L]))
    
    def isWithinRArrowP1Colour2(self, mousePos):
        if self.rArrowP1Colour2.is_hovered(mousePos):
            self.p1L = (self.p1L + 1) % len(self.hullColors)
            if self.p1L == self.p2L:
                self.p1L = (self.p1L + 1) % len(self.hullColors)
            self.textP1Colour2.setBoxColor(c.geT(self.ColorIndex[self.p1L]))

    def isWithinLArrowP2Turret(self, mousePos):
        if self.lArrowP2Turret.is_hovered(mousePos):
            self.p2I = (self.p2I - 1) % self.turretListLength
            self.textP2Turret.setText(self.turretList[self.p2I].getGunName())
    
    def isWithinRArrowP2Turret(self, mousePos):
        if self.rArrowP2Turret.is_hovered(mousePos):
            self.p2I = (self.p2I + 1) % self.turretListLength
            self.textP2Turret.setText(self.turretList[self.p2I].getGunName())
    
    def isWithinLArrowP2Hull(self, mousePos):
        if self.lArrowP2Hull.is_hovered(mousePos):
            self.p2J = (self.p2J - 1) % self.hullListLength
            self.textP2Hull.setText(self.hullList[self.p2J].getTankName())    

    def isWithinRArrowP2Hull(self, mousePos):
        if self.rArrowP2Hull.is_hovered(mousePos):
            self.p2J = (self.p2J + 1) % self.hullListLength
            self.textP2Hull.setText(self.hullList[self.p2J].getTankName())
    
    def isWithinLArrowP2Colour(self, mousePos):
        if self.lArrowP2Colour.is_hovered(mousePos):
            self.p2K = (self.p2K - 1) % len(self.hullColors)
            if self.p2K == self.p1K:
                self.p2K = (self.p2K - 1) % len(self.hullColors)
            self.textP2Colour.setBoxColor(c.geT(self.ColorIndex[self.p2K]))

    def isWithinRArrowP2Colour(self, mousePos):
        if self.rArrowP2Colour.is_hovered(mousePos):
            self.p2K = (self.p2K + 1) % len(self.hullColors)
            if self.p2K == self.p1K:
                self.p2K = (self.p2K + 1) % len(self.hullColors)
            self.textP2Colour.setBoxColor(c.geT(self.ColorIndex[self.p2K]))

    def isWithinLArrowP2Colour2(self, mousePos):
        if self.lArrowP2Colour2.is_hovered(mousePos):
            self.p2L = (self.p2L - 1) % len(self.hullColors)
            if self.p2L == self.p1L:
                self.p2L = (self.p2L - 1) % len(self.hullColors)
            self.textP2Colour2.setBoxColor(c.geT(self.ColorIndex[self.p2L]))

    def isWithinRArrowP2Colour2(self, mousePos):
        if self.rArrowP2Colour2.is_hovered(mousePos):
            self.p2L = (self.p2L + 1) % len(self.hullColors)
            if self.p2L == self.p1L:
                self.p2L = (self.p2L + 1) % len(self.hullColors)
            self.textP2Colour2.setBoxColor(c.geT(self.ColorIndex[self.p2L]))


    #broken list: rArrowP1Color2, lArrowP2Color, rArrowP2Color

class PlayerInformation:
    # This class will hold the turret / hulls for each of the players

    #Hull and turret list

    def __init__(self, tList, hList):
        self.turretList = tList
        self.hullList = hList

    def getTurretList(self):
        return self.turretList
    
    def getHullList(self):
        return self.hullList
    
    def getTurretListLength(self):
        return self.turretListLength
    
    def getHullListLength(self):
        return self.hullListLength