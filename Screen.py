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

    def draw(self, screen, mouse):

        screen.fill(const.BACKGROUND_COLOR) # This is the first line when drawing a new frame
        screen.blit(const.LOGO_PNG, (const.WINDOW_WIDTH // 2 - const.LOGO_PNG.get_width() // 2, 15))
        # Draw the tank image
        screen.blit(const.ORIGINAL_TANK_IMAGE, (const.WINDOW_WIDTH//2 - const.ORIGINAL_TANK_IMAGE.get_width()//2, const.WINDOW_HEIGHT//2 - const.ORIGINAL_TANK_IMAGE.get_height()//2))  # Centered horizontally

        # Draw the title text
        screen.blit(const.TITLE_TEXT, (const.WINDOW_WIDTH // 2 - const.TITLE_TEXT.get_width() // 2, 110))  # Centered horizontally, 50 pixels from top

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