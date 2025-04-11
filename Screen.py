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

    infoButtons = []
    iIndex = 0
    infoLArrow = Button(c.geT("BLACK"), c.geT("BLACK"), 100, 200, 100, 100, '<', c.geT("WHITE"), 100, c.geT("BLACK"))
    infoButtons.append(infoLArrow)
    infoText = TextBox(const.WINDOW_WIDTH//2 - 125, 75, font="Courier New",fontSize=30, text="Information", textColor=c.geT("BLACK"))
    infoText.selectable(False)
    infoText.setBoxColor(c.geT("OFF_WHITE"))
    infoButtons.append(infoText)
    iBox = TextBox(200, 201, font="Courier New",fontSize=46, text=const.INFOLIST[iIndex], textColor=c.geT("BLACK"))
    iBox.selectable(False)
    iBox.setCharacterPad(14)
    iBox.setPaddingHeight(23)
    iBox.setText(const.INFOLIST[iIndex])
    iBox.setBoxColor(c.geT("OFF_WHITE"))
    infoButtons.append(iBox)
    infoRArrow = Button(c.geT("BLACK"), c.geT("BLACK"), const.WINDOW_WIDTH - 200, 200, 100, 100, '>', c.geT("WHITE"), 100, c.geT("BLACK"))
    infoButtons.append(infoRArrow)
    infoBackButton = Button(c.geT("GREEN"), c.geT("WHITE"), const.WINDOW_WIDTH - 175, 75, 100, const.TILE_SIZE, 'Back', c.geT("BLACK"), 20, (100, 100, 255))
    infoButtons.append(infoBackButton)

    def draw(self, screen):
        pygame.draw.rect(screen, (240, 240, 240), [const.MAZE_X, const.MAZE_Y, const.WINDOW_WIDTH - const.MAZE_X * 2, const.WINDOW_HEIGHT - const.MAZE_Y * 2])
        pygame.draw.rect(screen, (0,0,0), [const.MAZE_X, const.MAZE_Y, const.WINDOW_WIDTH - const.MAZE_X * 2, const.WINDOW_HEIGHT - const.MAZE_Y * 2], 5)

        for i in self.infoButtons:
            i.draw(screen = screen, outline = True)
        
        startY = 325
        gap = 25
        for i in range(len(const.INFORENDER[self.iIndex])):
            screen.blit(const.INFORENDER[self.iIndex][i], (const.MAZE_X + 50, startY + i*gap))

    def isWithinBackButton(self, mousePos):
        return self.infoBackButton.is_hovered(mousePos)
    
    def isWithinLArrowButton(self, mousePos):
        return self.infoLArrow.is_hovered(mousePos)
    
    def isWithinRArrowButton(self, mousePos):
        return self.infoRArrow.is_hovered(mousePos)
    
    def updateBox(self, index):
        self.iIndex = (self.iIndex + index) % len(const.INFOLIST)
        self.iBox.setText(const.INFOLIST[self.iIndex])

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
        screen.blit(const.titleText, (const.WINDOW_WIDTH // 2 - const.titleText.get_width() // 2, 110))  # Centered horizontally, 50 pixels from top

        # Handle hover effect and draw buttons
        for button in self.homeButtonList:
            button.update_display(mouse)
            button.draw(screen, outline=True)