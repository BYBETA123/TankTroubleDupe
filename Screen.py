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
from Players import PlayerInformation
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
    
    homeButtonNameArray = ["1P Yard", "1P Scrapyard", "2P Yard", "2P Scrapyard", "1p Brawl", "1P DeathMatch", "2P Brawl", "2P DeathMatch", "1P TDM", "2P TDM", "1P CTF", "2P CTF"] #<!>
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

    lArrowP1Turret = Button(c.geT("BLACK"), c.geT("BLACK"), 70, 420, 30, 30, '<', c.geT("WHITE"), 30)
    lArrowP1Turret.selectable(False)
    buttonList.append(lArrowP1Turret)
    textP1Turret = TextBox(100, 420, font=const.MONO_FONT,fontSize=26, text="", textColor=c.geT("WHITE"))
    textP1Turret.setBoxColor(c.geT("GREY"))
    textP1Turret.selectable(False)
    textP1Turret.setPaddingHeight(0)
    buttonList.append(textP1Turret)
    rArrowP1Turret = Button(c.geT("BLACK"), c.geT("BLACK"), 280, 420, 30, 30, '>', c.geT("WHITE"), 30)
    rArrowP1Turret.selectable(False)
    buttonList.append(rArrowP1Turret)

    lArrowP1Hull = Button(c.geT("BLACK"), c.geT("BLACK"), 70, 460, 30, 30, '<', c.geT("WHITE"), 30)
    lArrowP1Hull.selectable(False)
    buttonList.append(lArrowP1Hull)
    textP1Hull = TextBox(100, 460, font=const.MONO_FONT,fontSize=26, text="", textColor=c.geT("WHITE"))
    textP1Hull.setBoxColor(c.geT("GREY"))
    textP1Hull.selectable(False)
    textP1Hull.setPaddingHeight(0)
    buttonList.append(textP1Hull)
    rArrowP1Hull = Button(c.geT("BLACK"), c.geT("BLACK"), 280, 460, 30, 30, '>', c.geT("WHITE"), 30)
    rArrowP1Hull.selectable(False)
    buttonList.append(rArrowP1Hull)

    lArrowP1Colour = Button(c.geT("BLACK"), c.geT("BLACK"), 70, 500, 30, 30, '<', c.geT("WHITE"), 30)
    lArrowP1Colour.selectable(False)
    buttonList.append(lArrowP1Colour)
    textP1Colour = TextBox(100, 500, font=const.MONO_FONT,fontSize=26, text="", textColor=c.geT("WHITE"))
    textP1Colour.setBoxColor(c.geT("BLACK"))
    textP1Colour.selectable(False)
    textP1Colour.setPaddingHeight(0)
    buttonList.append(textP1Colour)
    rArrowP1Colour = Button(c.geT("BLACK"), c.geT("BLACK"), 280, 500, 30, 30, '>', c.geT("WHITE"), 30)
    rArrowP1Colour.selectable(False)
    buttonList.append(rArrowP1Colour)

    lArrowP1Colour2 = Button(c.geT("BLACK"), c.geT("BLACK"), 70, 540, 30, 30, '<', c.geT("WHITE"), 30)
    lArrowP1Colour2.selectable(False)
    buttonList.append(lArrowP1Colour2)
    textP1Colour2 = TextBox(100, 540, font=const.MONO_FONT,fontSize=26, text="", textColor=c.geT("WHITE"))
    textP1Colour2.setBoxColor(c.geT("BLACK"))
    textP1Colour2.selectable(False)
    textP1Colour2.setPaddingHeight(0)
    buttonList.append(textP1Colour2)
    rArrowP1Colour2 = Button(c.geT("BLACK"), c.geT("BLACK"), 280, 540, 30, 30, '>', c.geT("WHITE"), 30)
    rArrowP1Colour2.selectable(False)
    buttonList.append(rArrowP1Colour2)

    lArrowP2Turret = Button(c.geT("BLACK"), c.geT("BLACK"), 493, 420, 30, 30, '<', c.geT("WHITE"), 30)
    lArrowP2Turret.selectable(False)
    buttonList.append(lArrowP2Turret)
    textP2Turret = TextBox(523, 420, font=const.MONO_FONT,fontSize=26, text="", textColor=c.geT("WHITE"))
    textP2Turret.setBoxColor(c.geT("GREY"))
    textP2Turret.selectable(False)
    textP2Turret.setPaddingHeight(0)
    buttonList.append(textP2Turret)
    rArrowP2Turret = Button(c.geT("BLACK"), c.geT("BLACK"),703, 420, 30, 30, '>', c.geT("WHITE"), 30)
    rArrowP2Turret.selectable(False)
    buttonList.append(rArrowP2Turret)

    lArrowP2Hull = Button(c.geT("BLACK"), c.geT("BLACK"), 493, 460, 30, 30, '<', c.geT("WHITE"), 30)
    lArrowP2Hull.selectable(False)
    buttonList.append(lArrowP2Hull)
    textP2Hull = TextBox(523, 460, font=const.MONO_FONT,fontSize=26, text="", textColor=c.geT("WHITE"))
    textP2Hull.setBoxColor(c.geT("GREY"))
    textP2Hull.selectable(False)
    textP2Hull.setPaddingHeight(0)
    buttonList.append(textP2Hull)
    rArrowP2Hull = Button(c.geT("BLACK"), c.geT("BLACK"),  703, 460, 30, 30, '>', c.geT("WHITE"), 30)
    rArrowP2Hull.selectable(False)
    buttonList.append(rArrowP2Hull)

    lArrowP2Colour = Button(c.geT("BLACK"), c.geT("BLACK"), 493, 500, 30, 30, '<', c.geT("WHITE"), 30)
    lArrowP2Colour.selectable(False)
    buttonList.append(lArrowP2Colour)
    textP2Colour = TextBox(523, 500, font=const.MONO_FONT,fontSize=26, text="", textColor=c.geT("WHITE"))
    textP2Colour.setBoxColor(c.geT("BLACK"))
    textP2Colour.selectable(False)
    textP2Colour.setPaddingHeight(0)
    buttonList.append(textP2Colour)
    rArrowP2Colour = Button(c.geT("BLACK"), c.geT("BLACK"),  703, 500, 30, 30, '>', c.geT("WHITE"), 30)
    rArrowP2Colour.selectable(False)
    buttonList.append(rArrowP2Colour)

    lArrowP2Colour2 = Button(c.geT("BLACK"), c.geT("BLACK"), 493, 540, 30, 30, '<', c.geT("WHITE"), 30)
    lArrowP2Colour2.selectable(False)
    buttonList.append(lArrowP2Colour2)
    textP2Colour2 = TextBox(523, 540, font=const.MONO_FONT,fontSize=26, text="", textColor=c.geT("WHITE"))
    textP2Colour2.setBoxColor(c.geT("BLACK"))
    textP2Colour2.selectable(False)
    textP2Colour2.setPaddingHeight(0)
    buttonList.append(textP2Colour2)
    rArrowP2Colour2 = Button(c.geT("BLACK"), c.geT("BLACK"),  703, 540, 30, 30, '>', c.geT("WHITE"), 30)
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

    speedText = TextBox(50, 320, font=const.SELECTION_FONT,fontSize=36, text="SPEED", textColor=c.geT("BLACK"))
    speedText.setPaddingHeight(0)
    speedText.setPaddingWidth(0)
    speedText.setCharacterPad(7)
    speedText.setBoxColor(const.SELECTION_BACKGROUND)
    speedText.setText("SPEED", 'right')
    buttonList.append(speedText)

    healthText = TextBox(42, 355, font=const.SELECTION_FONT,fontSize=36, text="Health", textColor=c.geT("BLACK"))
    healthText.setPaddingHeight(0)
    healthText.setPaddingWidth(0)
    healthText.setCharacterPad(7)
    healthText.setBoxColor(const.SELECTION_BACKGROUND)
    healthText.setText("HEALTH", "right")
    buttonList.append(healthText)

    damageBar = TextBox(31, 250, font=const.SELECTION_FONT,fontSize=36, text="Damage", textColor=c.geT("BLACK"))
    damageBar.setPaddingHeight(0)
    damageBar.setPaddingWidth(0)
    damageBar.setCharacterPad(7)
    damageBar.setBoxColor(const.SELECTION_BACKGROUND)
    damageBar.setText("DAMAGE", "right")
    buttonList.append(damageBar)

    reloadBar = TextBox(37, 285, font=const.SELECTION_FONT,fontSize=36, text="Reload", textColor=c.geT("BLACK"))
    reloadBar.setPaddingHeight(0)
    reloadBar.setPaddingWidth(0)
    reloadBar.setCharacterPad(7)
    reloadBar.setBoxColor(const.SELECTION_BACKGROUND)
    reloadBar.setText("RELOAD", "right")
    buttonList.append(reloadBar)

    speedText2 = TextBox(650, 320, font=const.SELECTION_FONT,fontSize=36, text="Speed", textColor=c.geT("BLACK"))
    speedText2.setPaddingHeight(0)
    speedText2.setPaddingWidth(0)
    speedText2.setCharacterPad(7)
    speedText2.setBoxColor(const.SELECTION_BACKGROUND)
    speedText2.setText("SPEED", "left")
    buttonList.append(speedText2)

    healthText2 = TextBox(650, 355, font=const.SELECTION_FONT,fontSize=36, text="Health", textColor=c.geT("BLACK"))
    healthText2.setPaddingHeight(0)
    healthText2.setPaddingWidth(0)
    healthText2.setCharacterPad(7)
    healthText2.setBoxColor(const.SELECTION_BACKGROUND)
    healthText2.setText("HEALTH", "left")
    buttonList.append(healthText2)

    damageBar2 = TextBox(650, 250, font=const.SELECTION_FONT,fontSize=36, text="Damage", textColor=c.geT("BLACK"))
    damageBar2.setPaddingHeight(0)
    damageBar2.setPaddingWidth(0)
    damageBar2.setCharacterPad(7)
    damageBar2.setBoxColor(const.SELECTION_BACKGROUND)
    damageBar2.setText("DAMAGE", "left")
    buttonList.append(damageBar2)

    reloadBar2 = TextBox(650, 285, font=const.SELECTION_FONT,fontSize=36, text="Reload", textColor=c.geT("BLACK"))
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
        self.setAll()

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

    def draw(self, screen, mouse):

        screen.fill(const.SELECTION_BACKGROUND) # This is the first line when drawing a new frame

        for button in self.buttonList:
            button.update_display(mouse)
            button.draw(screen, outline = False)

        # Draw the green bars
        pygame.draw.rect(screen, c.geT("GREEN"), (157, 320, 50 * self.playerInformation.getPlayer1Hull().getSpeedStatistic(), 25)) # Green bar
        pygame.draw.rect(screen, c.geT("GREEN"), (157, 355, 50 * self.playerInformation.getPlayer1Hull().getHealthStatistic(), 25)) # Green bar
        pygame.draw.rect(screen, c.geT("GREEN"), (157, 250, 50 * self.playerInformation.getPlayer1Turret().getDamageStatistic(), 25)) # Green bar
        pygame.draw.rect(screen, c.geT("GREEN"), (157, 285, 50 * self.playerInformation.getPlayer1Turret().getReloadStatistic(), 25)) # Green bar
        pygame.draw.rect(screen, c.geT("GREEN"), (493, 320, 50 * self.playerInformation.getPlayer2Hull().getSpeedStatistic(), 25)) # Green bar
        pygame.draw.rect(screen, c.geT("GREEN"), (493, 355, 50 * self.playerInformation.getPlayer2Hull().getHealthStatistic(), 25)) # Green bar
        pygame.draw.rect(screen, c.geT("GREEN"), (493, 250,50 * self.playerInformation.getPlayer2Turret().getDamageStatistic(), 25)) # Green bar
        pygame.draw.rect(screen, c.geT("GREEN"), (493, 285, 50 * self.playerInformation.getPlayer2Turret().getReloadStatistic(), 25)) # Green bar

        # Player 1 Speed
        #Outlines
        pygame.draw.rect(screen, c.geT("BLACK"), (157, 250, 150, 25), 3) # Green bar outline
        pygame.draw.rect(screen, c.geT("BLACK"), (207, 250, 50, 25), 3) # Thirding

        #Player 1 Health
        #Outlines
        pygame.draw.rect(screen, c.geT("BLACK"), (157, 285, 150, 25), 3) # Green bar outline
        pygame.draw.rect(screen, c.geT("BLACK"), (207, 285, 50,25), 3) # Thirding

        # Player 1 damage
        #Outlines
        pygame.draw.rect(screen, c.geT("BLACK"), (157, 320, 150, 25), 3) # Green bar outline
        pygame.draw.rect(screen, c.geT("BLACK"), (207, 320, 50,25), 3) # Thirding

        # Player 1 reload
        #Outlines
        pygame.draw.rect(screen, c.geT("BLACK"), (157, 355, 150, 25), 3) # Green bar outline
        pygame.draw.rect(screen, c.geT("BLACK"), (207, 355, 50,25), 3) # Thirding

        #Player 2 Speed
        #Outlines
        pygame.draw.rect(screen, c.geT("BLACK"), (493, 250, 50 * 3, 25), 3) # Green bar outline
        pygame.draw.rect(screen, c.geT("BLACK"), (543, 250, 50,25), 3) # Thirding

        # Player 2 Health
        #Outlines
        pygame.draw.rect(screen, c.geT("BLACK"), (493, 285, 150, 25), 3) # Green bar outline
        pygame.draw.rect(screen, c.geT("BLACK"), (543, 285, 50,25), 3) # Thirding

        # Player 2 Damage
        #Outlines
        pygame.draw.rect(screen, c.geT("BLACK"), (493, 320, 150, 25), 3) # Green bar outline
        pygame.draw.rect(screen, c.geT("BLACK"), (543, 320, 50, 25), 3) # Thirding

        # Player 2 Reload
        #Outlines
        pygame.draw.rect(screen, c.geT("BLACK"), (493, 355, 150, 25), 3) # Green bar outline
        pygame.draw.rect(screen, c.geT("BLACK"), (543, 355, 50,25), 3) # Thirding


        #Draw the tank image
        tankPath = os.path.join(const.BASE_PATH, 'Sprites', self.playerInformation.getPlayer1Hull().getTankName() + str(self.playerInformation.Player1HullColourIndex() + 1) + '.png')
        originalTankImage = pygame.image.load(tankPath).convert_alpha()
        tankImage = pygame.transform.scale(originalTankImage, (20*4, 13*4))
        screen.blit(tankImage, (130, 174))

        gunPath = os.path.join(const.BASE_PATH, 'Sprites', self.playerInformation.getPlayer1Turret().getGunName() + str(self.playerInformation.Player1TurretColourIndex()+1) + '.png')
        originalGunImage = pygame.image.load(gunPath).convert_alpha()
        centerX, centerY = self.playerInformation.getPlayer1Hull().getGunCenter()
        gX, _ = self.playerInformation.getPlayer1Turret().getGunCenter()
        gunImage = pygame.transform.scale(originalGunImage, (15*5, 15*5))
        screen.blit(gunImage, (170 + (centerX - gX) * 5, 194 - (centerY + 6) * 5))
        
        tankPath2 = os.path.join(const.BASE_PATH, 'Sprites', self.playerInformation.getPlayer2Hull().getTankName() + str(self.playerInformation.Player2HullColourIndex() + 1) + '.png')
        originalTankImage2 = pygame.image.load(tankPath2).convert_alpha()
        tankImage2 = pygame.transform.scale(originalTankImage2, (20*4, 13*4))
        tankImage2 = pygame.transform.flip(tankImage2, True, False) # Flipped    
        screen.blit(tankImage2, (const.WINDOW_WIDTH - 130 - 4 * 20, 174))

        gunPath2 = os.path.join(const.BASE_PATH, 'Sprites', self.playerInformation.getPlayer2Turret().getGunName() + str(self.playerInformation.Player2TurretColourIndex()+1) + '.png')
        originalGunImage2 = pygame.image.load(gunPath2).convert_alpha()
        centerX, centerY = self.playerInformation.getPlayer2Hull().getGunCenter()
        gX, _ = self.playerInformation.getPlayer2Turret().getGunCenter()

        gunImage2 = pygame.transform.scale(originalGunImage2, (15*5, 15*5))
        gunImage2 = pygame.transform.flip(gunImage2, True, False) # Flipped
        screen.blit(gunImage2, (const.WINDOW_WIDTH - 170 - 5 * 15 - (centerX - gX)*5, 194 + centerY*5 - 6*5))

    def isWithinPlayButton(self, mousePos):
        return self.playButton.buttonClick(mousePos)
    
    def isWithinHowToPlayButton(self, mousePos):
        return self.howToPlayButton.buttonClick(mousePos)
    
    def isWithinHomeButton(self, mousePos):
        return self.homeButton.buttonClick(mousePos)
    
    def setAll(self):
        # set all the text boxes
        self.textP1Turret.setText(self.playerInformation.getPlayer1Turret().getGunName())
        self.textP1Hull.setText(self.playerInformation.getPlayer1Hull().getTankName())
        self.textP1Colour.setBoxColor(c.geT(self.playerInformation.getPlayer1TurretColour()))
        self.textP1Colour2.setBoxColor(c.geT(self.playerInformation.getPlayer1HullColour()))
        self.textP2Turret.setText(self.playerInformation.getPlayer2Turret().getGunName())
        self.textP2Hull.setText(self.playerInformation.getPlayer2Hull().getTankName())
        self.textP2Colour.setBoxColor(c.geT(self.playerInformation.getPlayer2TurretColour()))
        self.textP2Colour2.setBoxColor(c.geT(self.playerInformation.getPlayer2HullColour()))

    def isWithinLArrowP1Turret(self, mousePos):
        if self.lArrowP1Turret.is_hovered(mousePos):
            self.playerInformation.movePlayer1TurretIndex(-1)
            self.textP1Turret.setText(self.playerInformation.getPlayer1Turret().getGunName())
    
    def isWithinRArrowP1Turret(self, mousePos):
        if self.rArrowP1Turret.is_hovered(mousePos):
            self.playerInformation.movePlayer1TurretIndex(1)
            self.textP1Turret.setText(self.playerInformation.getPlayer1Turret().getGunName())
    
    def isWithinLArrowP1Hull(self, mousePos):
        if self.lArrowP1Hull.is_hovered(mousePos):
            self.playerInformation.movePlayer1HullIndex(-1)
            self.textP1Hull.setText(self.playerInformation.getPlayer1Hull().getTankName())
    
    def isWithinRArrowP1Hull(self, mousePos):
        if self.rArrowP1Hull.is_hovered(mousePos):
            self.playerInformation.movePlayer1HullIndex(1)
            self.textP1Hull.setText(self.playerInformation.getPlayer1Hull().getTankName())
    
    def isWithinLArrowP1Colour(self, mousePos):
        if self.lArrowP1Colour.is_hovered(mousePos):
            self.playerInformation.movePlayer1TurretColourIndex(-1)
            self.textP1Colour.setBoxColor(c.geT(self.playerInformation.getPlayer1TurretColour()))

    def isWithinRArrowP1Colour(self, mousePos):
        if self.rArrowP1Colour.is_hovered(mousePos):
            self.playerInformation.movePlayer1TurretColourIndex(1)
            self.textP1Colour.setBoxColor(c.geT(self.playerInformation.getPlayer1TurretColour()))
    
    def isWithinLArrowP1Colour2(self, mousePos):
        if self.lArrowP1Colour2.is_hovered(mousePos):
            self.playerInformation.movePlayer1HullColourIndex(-1)
            self.textP1Colour2.setBoxColor(c.geT(self.playerInformation.getPlayer1HullColour()))
    
    def isWithinRArrowP1Colour2(self, mousePos):
        if self.rArrowP1Colour2.is_hovered(mousePos):
            self.playerInformation.movePlayer1HullColourIndex(1)
            self.textP1Colour2.setBoxColor(c.geT(self.playerInformation.getPlayer1HullColour()))

    def isWithinLArrowP2Turret(self, mousePos):
        if self.lArrowP2Turret.is_hovered(mousePos):
            self.playerInformation.movePlayer2TurretIndex(-1)
            self.textP2Turret.setText(self.playerInformation.getPlayer2Turret().getGunName())
    
    def isWithinRArrowP2Turret(self, mousePos):
        if self.rArrowP2Turret.is_hovered(mousePos):
            self.playerInformation.movePlayer2TurretIndex(1)
            self.textP2Turret.setText(self.playerInformation.getPlayer2Turret().getGunName())

    def isWithinLArrowP2Hull(self, mousePos):
        if self.lArrowP2Hull.is_hovered(mousePos):
            self.playerInformation.movePlayer2HullIndex(-1)
            self.textP2Hull.setText(self.playerInformation.getPlayer2Hull().getTankName())

    def isWithinRArrowP2Hull(self, mousePos):
        if self.rArrowP2Hull.is_hovered(mousePos):
            self.playerInformation.movePlayer2HullIndex(1)
            self.textP2Hull.setText(self.playerInformation.getPlayer2Hull().getTankName())
    
    def isWithinLArrowP2Colour(self, mousePos):
        if self.lArrowP2Colour.is_hovered(mousePos):
            self.playerInformation.movePlayer2TurretColourIndex(-1)
            self.textP2Colour.setBoxColor(c.geT(self.playerInformation.getPlayer2TurretColour()))


    def isWithinRArrowP2Colour(self, mousePos):
        if self.rArrowP2Colour.is_hovered(mousePos):
            self.playerInformation.movePlayer2TurretColourIndex(1)
            self.textP2Colour.setBoxColor(c.geT(self.playerInformation.getPlayer2TurretColour()))

    def isWithinLArrowP2Colour2(self, mousePos):
        if self.lArrowP2Colour2.is_hovered(mousePos):
            self.playerInformation.movePlayer2HullColourIndex(-1)
            self.textP2Colour2.setBoxColor(c.geT(self.playerInformation.getPlayer2HullColour()))
    
    def isWithinRArrowP2Colour2(self, mousePos):
        if self.rArrowP2Colour2.is_hovered(mousePos):
            self.playerInformation.movePlayer2HullColourIndex(1)
            self.textP2Colour2.setBoxColor(c.geT(self.playerInformation.getPlayer2HullColour()))

    def getPlayerInformation(self):
        return self.playerInformation # returns the PlayerInformation Class
    
class EndScreen:

    class TableRow:
        # 4 text boxes
        def __init__(self, height = 370, boxHeight = 60):
            self.text1 = Button(c.geT("GREY"), c.geT("GREY"), 124, height, 138, boxHeight, 'Player', c.geT("WHITE"), 26, c.geT("GREY"))
            self.text2 = Button(c.geT("GREY"), c.geT("GREY"), 262, height, 138, boxHeight, 'Kills', c.geT("WHITE"), 26, c.geT("GREY"))
            self.text3 = Button(c.geT("GREY"), c.geT("GREY"), 400, height, 138, boxHeight, 'Deaths', c.geT("WHITE"), 26, c.geT("GREY"))
            self.text4 = Button(c.geT("GREY"), c.geT("GREY"), 538, height, 138, boxHeight, 'Ratio', c.geT("WHITE"), 26, c.geT("GREY"))
            self.text1.setOutline(True, 5)
            self.text2.setOutline(True, 5)
            self.text3.setOutline(True, 5)
            self.text4.setOutline(True, 5)
            self.text1.selectable(False)
            self.text2.selectable(False)
            self.text3.selectable(False)
            self.text4.selectable(False)
            self.drawMe = False

        def draw(self, screen):
            if self.drawMe:
                self.text1.draw(screen, outline = True)
                self.text2.draw(screen, outline = True)
                self.text3.draw(screen, outline = True)
                self.text4.draw(screen, outline = True)
            return

        def setPlayerName(self, playerName):
            self.text1.setText(playerName)

        def setPlayerKills(self, playerKills):
            self.text2.setText(str(playerKills))

        def setPlayerDeaths(self, playerDeaths):
            self.text3.setText(str(playerDeaths))

        def setPlayerRatio(self, playerRatio):
            self.text4.setText(str(playerRatio))

        def setDraw(self, draw):
            self.drawMe = draw

    blist = []
    font_size = 30
    width = 255
    height = 70
    playAgainButton = Button(c.geT("BLACK"), c.geT("BLACK"), 115, 455, width, height, "Play Again", c.geT("WHITE"), font_size, c.geT("BLACK"))
    blist.append(playAgainButton)
    backToHomeButton = Button(c.geT("BLACK"), c.geT("BLACK"), 430, 455, width, height, "Back to Home", c.geT("WHITE"), font_size, c.geT("BLACK"))
    blist.append(backToHomeButton)


    TableInfo = []

    def __init__(self):
        a = 72
        b = 40
        self.tableRow1 = self.TableRow(a, b)
        self.tableRow1.setDraw(True)
        self.tableRow2 = self.TableRow(a+b, b)
        self.tableRow3 = self.TableRow(a + 2*b, b)
        self.tableRow4 = self.TableRow(a + 3*b, b)
        self.tableRow5 = self.TableRow(a + 4*b, b)
        self.tableRow6 = self.TableRow(a + 5*b, b)
        self.tableRow7 = self.TableRow(a + 6*b, b)
        self.tableRow8 = self.TableRow(a + 7*b, b)
        self.tableRow9 = self.TableRow(a + 8*b, b)
        self.TableInfo.append(self.tableRow1)
        self.TableInfo.append(self.tableRow2)
        self.TableInfo.append(self.tableRow3)
        self.TableInfo.append(self.tableRow4)
        self.TableInfo.append(self.tableRow5)
        self.TableInfo.append(self.tableRow6)
        self.TableInfo.append(self.tableRow7)
        self.TableInfo.append(self.tableRow8)
        self.TableInfo.append(self.tableRow9)

        # self.makeTable(["Player 1", "0", "0", "0"],["Player 2", "0", "0", "0"],["Player 3", "0", "0", "0"])

    def draw(self, screen):
        pygame.draw.rect(screen, (240, 240, 240), [const.MAZE_X, const.MAZE_Y, const.WINDOW_WIDTH - const.MAZE_X * 2, const.WINDOW_HEIGHT - const.MAZE_Y * 2])
        pygame.draw.rect(screen, (0,0,0), [const.MAZE_X, const.MAZE_Y, const.WINDOW_WIDTH - const.MAZE_X * 2, const.WINDOW_HEIGHT - const.MAZE_Y * 2], 5)

        for button in self.blist:
            button.draw(screen, outline = True)

        # Draw the table rows
        for row in self.TableInfo:
            row.draw(screen)

    def isWithinPlayAgainButton(self, mousePos):
        return self.playAgainButton.is_hovered(mousePos)
    
    def isWithinHomeButton(self, mousePos):
        return self.backToHomeButton.is_hovered(mousePos)

    def makeTable(self, *rows):
        # set all table rows to not draw
        # make all 0 except for the first one
        rows = list(zip(*rows))
        rows = list(zip(*rows))
        rows.sort(key=lambda x: x[3], reverse=True)
        for row in self.TableInfo:
            row.setDraw(False)
        # set the first row to draw
        self.TableInfo[0].setDraw(True)
        for idx, r in enumerate(rows):
            self.TableInfo[idx+1].setDraw(True)
            self.TableInfo[idx+1].setPlayerName(r[0])
            self.TableInfo[idx+1].setPlayerKills(r[1])
            self.TableInfo[idx+1].setPlayerDeaths(r[2])
            self.TableInfo[idx+1].setPlayerRatio(f"{r[3]:.2f}")

class NotImplmented:

    backButton = Button(c.geT("BLACK"), c.geT("BLACK"), 630, 175, 100, 50, "Back", c.geT("WHITE"), 30, c.geT("BLACK"))

    txtBox = TextBox(100, 180, font=const.SELECTION_FONT,fontSize=30, text="This feature has not been implemented yet", textColor=c.geT("BLACK"))
    txtBox.setBoxColor(const.SELECTION_BACKGROUND)

    def draw(self, screen):

        pygame.draw.rect(screen, const.SELECTION_BACKGROUND, [40, 160, 740, 80])
        pygame.draw.rect(screen, c.geT("BLACK"), [40, 160, 740, 80], width = 5)
        self.backButton.draw(screen, outline = True)
        self.txtBox.draw(screen, outline = True)

    def isWithinBackButton(self, mousePos):
        return self.backButton.is_hovered(mousePos)
