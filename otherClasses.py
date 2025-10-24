import pygame
import os, sys
import constants as const
import globalVariables as g
import random
from ColorDictionary import ColourDictionary as c # colors
from DifficultyTypes import *

class Explosion(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.images = []
        # Determine the correct base path
        if getattr(sys, 'frozen', False):  # Running as an .exe
            base_path = sys._MEIPASS
        else:  # Running as a .py script
            base_path = os.path.dirname(os.path.abspath(__file__))

        # Construct the correct path for the sprite sheet
        sprite_sheet_path = os.path.join(base_path, "Assets", "explosion.png")

        # Load the sprite sheet
        SpriteSheetImage = pygame.image.load(sprite_sheet_path).convert_alpha()
        for i in range(48):
            self.images.append(self.getImage(SpriteSheetImage, i, 128, 128, 0.5))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.lastUpdate = pygame.time.get_ticks()
        self.animationCooldown = 12

    def getImage(self, sheet, frame, width, height, scale):
        # This function will use the spritesheet to get the respective image from the sprite sheet
        # Inputs: Sheet: The required sprite sheet for the animation
        # Inputs: Frame: The frame index of the animation
        # Inputs: Width: The width of the frame
        # Inputs: Height: The height of the frame
        # Inputs: Scale: The scale of which to scale the image to
        # Outputs: The image of the frame
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0, 0), ((frame*width%1024), (frame//8 * width), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey((0, 0, 0)) # Black
        return image

    def update(self):
        # This function will update the explosion animation every frame
        # Inputs: None
        # Outputs: None
        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastUpdate >= self.animationCooldown:
            self.lastUpdate = currentTime
            self.index += 1
        if self.index >= len(self.images):
            self.kill()
        else:
            self.image = self.images[self.index]

    def setCooldown(self, num):
        self.animationCooldown = num

    def getCooldown(self):
        return self.animationCooldown


class Flag():
    def __init__(self, team, coords):
        self.team = team
        self.dropped = False
        self.returnTimer = 1400
        self.xy = coords
        self.homexy = coords
        self.tank = None
        self.score = 0
    def update(self):
        if self.dropped:
            self.returnTimer -= 1
        if self.returnTimer < 0:
            self.returnTimer = 0
            # return the flag
            self.returnFlag()
        for i in range(g.difficultyType.playerCount):
            if not g.tankDead[i]:
                if self.isWithin(g.tankList[i].getCenter()):
                    # if we are within, award the flag
                    # if the tank is on the same team as the flag, then auto return
                    # if not, then give the flag

                    if g.tankList[i].getTeam() != (self.team): # if they are not the same team
                        if not self.isHome() and self.dropped:
                            self.returnFlag()
                        # if the tank has a flag, return the flag
                        elif g.tankList[i].flag != None:
                            # if one of the two flags is not home, return the flag
                            if g.flag[0].isHome() or g.flag[1].isHome(): # if one is home
                                g.flag[0].returnFlag()
                                g.flag[1].returnFlag()
                                g.flag[0].setTank(None)
                                g.flag[1].setTank(None)
                                g.tankList[i].setFlag(None)
                                # we need to update the score
                                self.score += 1
                    else:
                        if self.dropped or self.isHome():
                            self.dropped = False
                            self.returnTimer = 1400
                            g.flag[self.team].setTank(g.tankList[i])
                            g.tankList[i].setFlag(self.team) # give the tank the flag property
        if self.tank is not None: # if we have been picked up
            self.xy = self.tank.getCenter()
        else: # if it is none
            if self.xy != self.homexy:
                self.dropped = True # it's been dropped somewhere
                self.tank = None

    def isWithin(self, coords):
        cX, cY = coords[0], coords[1]
        if cX >= self.xy[0] and cX <= self.xy[0] + const.TILE_SIZE_X and cY >= self.xy[1] and cY <= self.xy[1] + const.TILE_SIZE_Y:
            return True
        return False

    def isHome(self):
        return self.xy == self.homexy # if these are equal we are at the spawn location of the flag

    def draw(self, screen):
        if self.isHome():
            # if we are at home, don't draw the flag
            return
        size = const.TILE_SIZE_Y // 8 # <! Update with new code>
        triangle = [
            [self.xy[0], self.xy[1] - size],
            [self.xy[0] - size, self.xy[1] + size],
            [self.xy[0] + size, self.xy[1] + size]
        ]
        if self.team == 1:
            pygame.draw.polygon(screen, c.geT("BLUE"), triangle)
        else:
            pygame.draw.polygon(screen, c.geT("RED"), triangle)

    def returnFlag(self):
        self.xy = self.homexy
        self.returnTimer = 1400
        self.dropped = False
        self.tank = None # remove the tank

    def getTeam(self):
        return self.team

    def setxy(self, xy):
        self.xy = xy
    
    def setHome(self, home):
        self.homexy = home

    def setTank(self, tank):
        self.tank = tank

    def drop(self):
        self.dropped = True

    def getScore(self):
        return self.score

    def getxy(self):
        return self.xy
    
    def isDropped(self):
        return self.dropped
    
    def getTileIndex(self):
        # This function will return the tile index of the flag
        # Inputs: None
        # Outputs: The tile index of the flag
        return ((self.xy[0]-const.MAZE_X) // const.TILE_SIZE_X) + ((self.xy[1]-const.MAZE_Y) // const.TILE_SIZE_Y) * const.COLUMN_AMOUNT + 1
    
    def getTileHomeIndex(self):
        # This function will return the tile index of the flag home
        # Inputs: None
        # Outputs: The tile index of the flag home
        return ((self.homexy[0]-const.MAZE_X) // const.TILE_SIZE_X) + ((self.homexy[1]-const.MAZE_Y) // const.TILE_SIZE_Y) * const.COLUMN_AMOUNT + 1